"""
Database models for Smart Fertilizer Recommendation System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class Season(str, enum.Enum):
    """Crop season enumeration"""
    KHARIF = "Kharif"
    RABI = "Rabi"
    ZAID = "Zaid"


class DataSource(str, enum.Enum):
    """Source of soil data"""
    SENSOR = "sensor"
    MANUAL = "manual"
    UPLOAD = "upload"


class NutrientStatus(str, enum.Enum):
    """Nutrient level status"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class PHStatus(str, enum.Enum):
    """pH level status"""
    ACIDIC = "Acidic"
    NEUTRAL = "Neutral"
    ALKALINE = "Alkaline"


class Farmer(Base):
    """Farmer information model"""
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    mobile = Column(String(15), nullable=False, unique=True)
    village = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    field_area = Column(Float, nullable=False)  # in acres or hectares
    crop_name = Column(String(100), nullable=False)
    crop_season = Column(Enum(Season), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    soil_data = relationship("SoilData", back_populates="farmer")
    soil_health_cards = relationship("SoilHealthCard", back_populates="farmer")
    recommendations = relationship("FertilizerRecommendation", back_populates="farmer")


class Device(Base):
    """IoT Device (ESP32) registration"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100))
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=True)
    location = Column(String(200))
    is_active = Column(Integer, default=1)  # 1=active, 0=inactive
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_data_received = Column(DateTime, nullable=True)

    # Relationships
    farmer = relationship("Farmer")
    soil_data = relationship("SoilData", back_populates="device")


class SoilData(Base):
    """Soil measurement data from all sources"""
    __tablename__ = "soil_data"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    
    # Soil parameters
    nitrogen = Column(Float, nullable=True)  # N (mg/kg or ppm)
    phosphorus = Column(Float, nullable=True)  # P (mg/kg or ppm)
    potassium = Column(Float, nullable=True)  # K (mg/kg or ppm)
    ph = Column(Float, nullable=True)  # pH value
    ec = Column(Float, nullable=True)  # Electrical Conductivity (dS/m)
    moisture = Column(Float, nullable=True)  # Soil moisture (%)
    temperature = Column(Float, nullable=True)  # Temperature (°C)
    organic_carbon = Column(Float, nullable=True)  # Optional (%)
    
    # Metadata
    data_source = Column(Enum(DataSource), nullable=False)
    sample_id = Column(String(50), unique=True, nullable=False, index=True)
    collection_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # File upload metadata
    upload_filename = Column(String(255), nullable=True)
    upload_file_type = Column(String(50), nullable=True)

    # Relationships
    farmer = relationship("Farmer", back_populates="soil_data")
    device = relationship("Device", back_populates="soil_data")
    soil_health_card = relationship("SoilHealthCard", back_populates="soil_data", uselist=False)
    recommendation = relationship("FertilizerRecommendation", back_populates="soil_data", uselist=False)


class SoilHealthCard(Base):
    """Soil Health Card generation records"""
    __tablename__ = "soil_health_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String(50), unique=True, nullable=False, index=True)  # Unique card ID
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    soil_data_id = Column(Integer, ForeignKey("soil_data.id"), nullable=False)
    
    # Nutrient status classifications
    nitrogen_status = Column(Enum(NutrientStatus), nullable=True)
    phosphorus_status = Column(Enum(NutrientStatus), nullable=True)
    potassium_status = Column(Enum(NutrientStatus), nullable=True)
    ph_status = Column(Enum(PHStatus), nullable=True)
    ec_status = Column(String(20), nullable=True)  # Normal/High
    
    # Generation metadata
    issue_date = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(50), default="System")
    
    # File paths for generated reports
    pdf_path = Column(String(500), nullable=True)
    excel_path = Column(String(500), nullable=True)

    # Relationships
    farmer = relationship("Farmer", back_populates="soil_health_cards")
    soil_data = relationship("SoilData", back_populates="soil_health_card")


class FertilizerRecommendation(Base):
    """ML-based fertilizer recommendations"""
    __tablename__ = "fertilizer_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    soil_data_id = Column(Integer, ForeignKey("soil_data.id"), nullable=False)
    
    # ML predictions - nutrient requirements (kg/ha)
    required_nitrogen = Column(Float, nullable=False)
    required_phosphorus = Column(Float, nullable=False)
    required_potassium = Column(Float, nullable=False)
    
    # Fertilizer recommendations
    fertilizer_name = Column(String(200), nullable=False)  # Can be multiple, comma-separated
    quantity_kg_per_hectare = Column(Float, nullable=False)
    quantity_kg_per_acre = Column(Float, nullable=False)
    
    # Application details
    application_timing = Column(String(100), nullable=True)  # e.g., "Basal", "Top Dressing - 30 days"
    application_method = Column(Text, nullable=True)  # Detailed application instructions
    
    # Cost and reasoning
    estimated_cost = Column(Float, nullable=True)  # Estimated cost in INR
    reasoning = Column(Text, nullable=True)  # AI-generated explanation
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(50), default="v1.0")

    # Relationships
    farmer = relationship("Farmer", back_populates="recommendations")
    soil_data = relationship("SoilData", back_populates="recommendation")
