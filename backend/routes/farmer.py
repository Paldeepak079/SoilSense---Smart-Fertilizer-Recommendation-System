"""
Farmer management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Farmer, SoilData, SoilHealthCard, FertilizerRecommendation, Device
from schemas import FarmerCreate, FarmerResponse, MessageResponse

router = APIRouter()


@router.post("/farmers", response_model=FarmerResponse, status_code=status.HTTP_201_CREATED)
async def register_farmer(farmer_data: FarmerCreate, db: Session = Depends(get_db)):
    """
    Register a new farmer
    """
    # Check if mobile already exists
    existing_farmer = db.query(Farmer).filter(Farmer.mobile == farmer_data.mobile).first()
    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Farmer with mobile {farmer_data.mobile} already registered"
        )
    
    # Create new farmer
    new_farmer = Farmer(**farmer_data.dict())
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)
    
    return new_farmer


@router.get("/farmers/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """
    Get farmer details by ID
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {farmer_id} not found"
        )
    return farmer


@router.get("/farmers", response_model=List[FarmerResponse])
async def list_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all farmers with pagination
    """
    farmers = db.query(Farmer).offset(skip).limit(limit).all()
    return farmers


@router.put("/farmers/{farmer_id}", response_model=FarmerResponse)
async def update_farmer(farmer_id: int, farmer_data: FarmerCreate, db: Session = Depends(get_db)):
    """
    Update farmer information
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {farmer_id} not found"
        )
    
    # Update fields
    for key, value in farmer_data.dict().items():
        setattr(farmer, key, value)
    
    db.commit()
    db.refresh(farmer)
    return farmer


@router.delete("/farmers/{farmer_id}", response_model=MessageResponse)
async def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    """
    Delete a farmer
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {farmer_id} not found"
        )
    
    # Delete related records manually (since cascade might not be set in DB)
    
    # 1. Delete Soil Health Cards
    db.query(SoilHealthCard).filter(SoilHealthCard.farmer_id == farmer_id).delete()
    
    # 2. Delete Fertilizer Recommendations
    db.query(FertilizerRecommendation).filter(FertilizerRecommendation.farmer_id == farmer_id).delete()
    
    # 3. Delete Soil Data
    db.query(SoilData).filter(SoilData.farmer_id == farmer_id).delete()
    
    # 4. Unlink Devices (Set farmer_id to NULL)
    devices = db.query(Device).filter(Device.farmer_id == farmer_id).all()
    for device in devices:
        device.farmer_id = None
        device.is_active = 0 # Optional: Deactivate device if owner is deleted
    
    # Now safe to delete farmer
    db.delete(farmer)
    db.commit()
    return MessageResponse(message="Farmer deleted successfully", id=farmer_id)
