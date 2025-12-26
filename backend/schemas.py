"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SeasonEnum(str, Enum):
    KHARIF = "Kharif"
    RABI = "Rabi"
    ZAID = "Zaid"


class DataSourceEnum(str, Enum):
    SENSOR = "sensor"
    MANUAL = "manual"
    UPLOAD = "upload"


# ========== Farmer Schemas ==========

class FarmerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    mobile: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    village: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    field_area: float = Field(..., gt=0, description="Field area in acres or hectares")
    crop_name: str = Field(..., min_length=1, max_length=100)
    crop_season: SeasonEnum


class FarmerResponse(BaseModel):
    id: int
    name: str
    mobile: str
    village: str
    district: str
    state: str
    field_area: float
    crop_name: str
    crop_season: str
    created_at: datetime

    class Config:
        orm_mode = True


# ========== Soil Data Schemas ==========

class SoilDataManual(BaseModel):
    """Manual soil data entry"""
    farmer_id: int
    nitrogen: Optional[float] = Field(None, ge=0, description="Nitrogen in mg/kg")
    phosphorus: Optional[float] = Field(None, ge=0, description="Phosphorus in mg/kg")
    potassium: Optional[float] = Field(None, ge=0, le=500, description="Potassium in mg/kg")
    ph: Optional[float] = Field(None, ge=3.5, le=9.5, description="pH value (must be 3.5-9.5)")
    ec: Optional[float] = Field(None, ge=0, le=20, description="Electrical Conductivity in dS/m")
    moisture: Optional[float] = Field(None, ge=0, le=100, description="Soil moisture percentage")
    organic_carbon: Optional[float] = Field(None, ge=0, le=10, description="Organic carbon percentage")


class SoilDataIoT(BaseModel):
    """IoT sensor data from ESP32"""
    device_id: str
    soil_moisture: float = Field(..., ge=0, le=100)
    soil_ph: float = Field(..., ge=3.5, le=9.5, description="pH (3.5-9.5)")
    soil_ec: float = Field(..., ge=0, le=20)
    temperature: float = Field(..., ge=-50, le=100)
    timestamp: str  # Format: "YYYY-MM-DD HH:MM:SS"
    
    # Optional nutrient sensors (if available)
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None


class SoilDataResponse(BaseModel):
    id: int
    farmer_id: int
    nitrogen: Optional[float]
    phosphorus: Optional[float]
    potassium: Optional[float]
    ph: Optional[float]
    ec: Optional[float]
    moisture: Optional[float]
    temperature: Optional[float]
    organic_carbon: Optional[float]
    data_source: str
    sample_id: str
    collection_date: datetime
    
    class Config:
        orm_mode = True


# ========== Recommendation Schemas ==========

class RecommendationCreate(BaseModel):
    """Request to generate fertilizer recommendation"""
    farmer_id: int
    soil_data_id: int


class RecommendationResponse(BaseModel):
    id: int
    farmer_id: int
    soil_data_id: int
    required_nitrogen: float
    required_phosphorus: float
    required_potassium: float
    fertilizer_name: str
    quantity_kg_per_hectare: float
    quantity_kg_per_acre: float
    application_timing: Optional[str]
    application_method: Optional[str]
    estimated_cost: Optional[float]
    reasoning: Optional[str]
    created_at: datetime
    
    class Config:
        orm_mode = True


# ========== Soil Health Card Schemas ==========

class SoilHealthCardCreate(BaseModel):
    """Request to generate Soil Health Card"""
    farmer_id: int
    soil_data_id: int


class SoilHealthCardResponse(BaseModel):
    id: int
    card_id: str
    farmer_id: int
    soil_data_id: int
    nitrogen_status: Optional[str]
    phosphorus_status: Optional[str]
    potassium_status: Optional[str]
    ph_status: Optional[str]
    ec_status: Optional[str]
    issue_date: datetime
    
    class Config:
        orm_mode = True


# ========== Generic Response Schemas ==========

class MessageResponse(BaseModel):
    """Generic success message"""
    message: str
    id: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
