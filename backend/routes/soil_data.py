"""
Soil data management API routes
Handles: IoT sensor data, manual entry, and file uploads
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from database import get_db
from models import SoilData, Farmer, DataSource, Device
from schemas import SoilDataManual, SoilDataIoT, SoilDataResponse, MessageResponse
from services.iot_validator import validate_iot_data, register_device
from services.file_parser import FileParser

router = APIRouter()


@router.post("/soil-data/iot", response_model=SoilDataResponse, status_code=status.HTTP_201_CREATED)
async def ingest_iot_data(iot_data: SoilDataIoT, db: Session = Depends(get_db)):
    """
    Ingest soil data from ESP32 IoT device
    """
    # Validate IoT data and get device
    device = validate_iot_data(iot_data, db)
    
    if not device.farmer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device {iot_data.device_id} is not linked to any farmer. Please link device to farmer first."
        )
    
    # Generate unique sample ID
    sample_id = f"IOT_{device.device_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Create soil data record
    soil_data = SoilData(
        farmer_id=device.farmer_id,
        device_id=device.id,
        nitrogen=iot_data.nitrogen,
        phosphorus=iot_data.phosphorus,
        potassium=iot_data.potassium,
        ph=iot_data.soil_ph,
        ec=iot_data.soil_ec,
        moisture=iot_data.soil_moisture,
        temperature=iot_data.temperature,
        data_source=DataSource.SENSOR,
        sample_id=sample_id,
        collection_date=datetime.strptime(iot_data.timestamp, "%Y-%m-%d %H:%M:%S")
    )
    
    db.add(soil_data)
    db.commit()
    db.refresh(soil_data)
    
    return soil_data


@router.post("/soil-data/manual", response_model=SoilDataResponse, status_code=status.HTTP_201_CREATED)
async def manual_soil_entry(soil_data_input: SoilDataManual, db: Session = Depends(get_db)):
    """
    Manual soil data entry via form
    """
    # Verify farmer exists
    farmer = db.query(Farmer).filter(Farmer.id == soil_data_input.farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {soil_data_input.farmer_id} not found"
        )
    
    # ---------------------------------------------------------
    # STRICT VALIDATION Logic
    # ---------------------------------------------------------
    errors = []
    
    # pH Validation (3.5 - 9.0)
    if soil_data_input.ph is not None:
        if not (3.5 <= soil_data_input.ph <= 9.0):
            errors.append(f"pH value {soil_data_input.ph} is out of realistic range (3.5 - 9.0).")

    # EC Validation (<= 4 dS/m for general agriculture)
    if soil_data_input.ec is not None:
        if not (0 <= soil_data_input.ec <= 4.0):
            errors.append(f"EC value {soil_data_input.ec} dS/m is too high (Must be ≤ 4.0).")

    # Moisture Validation (0 - 100%)
    if soil_data_input.moisture is not None:
        if not (0 <= soil_data_input.moisture <= 100.0):
            errors.append(f"Moisture {soil_data_input.moisture}% is invalid (Must be 0-100%).")
            
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=" | ".join(errors)
        )
    # ---------------------------------------------------------
    
    # Generate unique sample ID
    sample_id = f"MANUAL_{farmer.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Create soil data record
    soil_data = SoilData(
        farmer_id=soil_data_input.farmer_id,
        nitrogen=soil_data_input.nitrogen,
        phosphorus=soil_data_input.phosphorus,
        potassium=soil_data_input.potassium,
        ph=soil_data_input.ph,
        ec=soil_data_input.ec,
        moisture=soil_data_input.moisture,
        organic_carbon=soil_data_input.organic_carbon,
        data_source=DataSource.MANUAL,
        sample_id=sample_id
    )
    
    db.add(soil_data)
    db.commit()
    db.refresh(soil_data)
    
    return soil_data


@router.post("/soil-data/upload/{farmer_id}", response_model=SoilDataResponse, status_code=status.HTTP_201_CREATED)
async def upload_soil_data_file(
    farmer_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload soil data file (CSV, Excel, PDF, Word, Image)
    """
    # Verify farmer exists
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {farmer_id} not found"
        )
    
    # Parse file and extract soil data
    extracted_data = await FileParser.parse_file(file)
    
    # Validate that at least some data was extracted
    if all(value is None for value in extracted_data.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract any soil data from the uploaded file. Please check file format and content."
        )
    
    # Generate unique sample ID
    sample_id = f"UPLOAD_{farmer_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Create soil data record
    soil_data = SoilData(
        farmer_id=farmer_id,
        nitrogen=extracted_data.get('nitrogen'),
        phosphorus=extracted_data.get('phosphorus'),
        potassium=extracted_data.get('potassium'),
        ph=extracted_data.get('ph'),
        ec=extracted_data.get('ec'),
        moisture=extracted_data.get('moisture'),
        organic_carbon=extracted_data.get('organic_carbon'),
        data_source=DataSource.UPLOAD,
        sample_id=sample_id,
        upload_filename=file.filename,
        upload_file_type=file.content_type
    )
    
    db.add(soil_data)
    db.commit()
    db.refresh(soil_data)
    
    return soil_data


@router.get("/soil-data/{soil_data_id}", response_model=SoilDataResponse)
async def get_soil_data(soil_data_id: int, db: Session = Depends(get_db)):
    """
    Get soil data by ID
    """
    soil_data = db.query(SoilData).filter(SoilData.id == soil_data_id).first()
    if not soil_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Soil data with ID {soil_data_id} not found"
        )
    return soil_data


@router.get("/soil-data/farmer/{farmer_id}", response_model=List[SoilDataResponse])
async def get_farmer_soil_data(farmer_id: int, db: Session = Depends(get_db)):
    """
    Get all soil data records for a farmer
    """
    soil_data = db.query(SoilData).filter(SoilData.farmer_id == farmer_id).all()
    return soil_data


@router.post("/devices/register", status_code=status.HTTP_201_CREATED)
async def register_new_device(
    device_id: str,
    name: str,
    farmer_id: int,
    location: str,
    db: Session = Depends(get_db)
):
    """
    Register a new IoT device (ESP32)
    """
    device = register_device(device_id, name, farmer_id, location, db)
    return {
        "message": "Device registered successfully",
        "device_id": device.device_id,
        "id": device.id
    }
