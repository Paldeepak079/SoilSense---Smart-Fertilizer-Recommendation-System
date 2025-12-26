"""
IoT data validation service
"""
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Device
from schemas import SoilDataIoT


def validate_iot_data(iot_data: SoilDataIoT, db: Session) -> Device:
    """
    Validate IoT sensor data from ESP32
    
    Args:
        iot_data: Incoming IoT sensor data
        db: Database session
    
    Returns:
        Device object if valid
    
    Raises:
        HTTPException if validation fails
    """
    # Check if device is registered
    device = db.query(Device).filter(Device.device_id == iot_data.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device {iot_data.device_id} not registered. Please register device first."
        )
    
    # Check if device is active
    if not device.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Device {iot_data.device_id} is inactive"
        )
    
    # Validate sensor value ranges
    errors = []
    
    if not (0 <= iot_data.soil_moisture <= 100):
        errors.append("Soil moisture must be between 0 and 100%")
    
    if not (0 <= iot_data.soil_ph <= 14):
        errors.append("Soil pH must be between 0 and 14")
    
    if iot_data.soil_ec < 0:
        errors.append("Soil EC cannot be negative")
    
    if not (-50 <= iot_data.temperature <= 100):
        errors.append("Temperature must be between -50 and 100°C")
    
    # Validate timestamp format
    try:
        datetime.strptime(iot_data.timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errors.append("Timestamp must be in format: YYYY-MM-DD HH:MM:SS")
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Validation failed", "errors": errors}
        )
    
    # Update device last data received
    device.last_data_received = datetime.utcnow()
    db.commit()
    
    return device


def register_device(device_id: str, name: str, farmer_id: int, location: str, db: Session) -> Device:
    """
    Register a new IoT device
    
    Args:
        device_id: Unique device identifier (e.g., ESP32_001)
        name: Device name
        farmer_id: Associated farmer ID
        location: Device location
        db: Database session
    
    Returns:
        Newly created Device object
    """
    # Check if device already exists
    existing_device = db.query(Device).filter(Device.device_id == device_id).first()
    if existing_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device {device_id} already registered"
        )
    
    # Create new device
    device = Device(
        device_id=device_id,
        name=name,
        farmer_id=farmer_id,
        location=location,
        is_active=1
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    
    return device
