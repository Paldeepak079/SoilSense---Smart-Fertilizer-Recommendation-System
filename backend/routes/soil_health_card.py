"""
Soil Health Card API routes
Generate and download soil health cards in various formats
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from database import get_db
from models import FertilizerRecommendation, SoilData, Farmer
from services.soil_health_card import generate_csv
from services.pdf_generator import generate_pdf
from services.excel_generator import generate_excel

router = APIRouter()


@router.get("/soil-health-card/{recommendation_id}/csv")
async def download_csv(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Download Soil Health Card as CSV
    """
    # Get recommendation
    recommendation = db.query(FertilizerRecommendation).filter(
        FertilizerRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with ID {recommendation_id} not found"
        )
    
    # Get associated data
    farmer = db.query(Farmer).filter(Farmer.id == recommendation.farmer_id).first()
    soil_data = db.query(SoilData).filter(SoilData.id == recommendation.soil_data_id).first()
    
    if not farmer or not soil_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associated farmer or soil data not found"
        )
    
    # Prepare data dictionaries
    farmer_dict = {
        'name': farmer.name,
        'village': farmer.village,
        'district': farmer.district,
        'state': farmer.state,
        'field_area': farmer.field_area,
        'crop_name': farmer.crop_name,
        'crop_season': farmer.crop_season.value
    }
    
    soil_dict = {
        'nitrogen': soil_data.nitrogen,
        'phosphorus': soil_data.phosphorus,
        'potassium': soil_data.potassium,
        'ph': soil_data.ph,
        'ec': soil_data.ec,
        'moisture': soil_data.moisture,
        'organic_carbon': soil_data.organic_carbon,
        'sample_id': soil_data.sample_id
    }
    
    recommendation_dict = {
        'required_nitrogen': recommendation.required_nitrogen,
        'required_phosphorus': recommendation.required_phosphorus,
        'required_potassium': recommendation.required_potassium,
        'fertilizer_name': recommendation.fertilizer_name,
        'quantity_kg_per_hectare': recommendation.quantity_kg_per_hectare,
        'quantity_kg_per_acre': recommendation.quantity_kg_per_acre,
        'estimated_cost': recommendation.estimated_cost,
        'additional_data': recommendation.reasoning  # Contains JSON with improvements and schedule
    }
    
    # Generate CSV
    csv_content = generate_csv(farmer_dict, soil_dict, recommendation_dict)
    
    # Create streaming response
    output = io.BytesIO(csv_content.encode('utf-8'))
    
    filename = f"SoilHealthCard_{farmer.name.replace(' ', '_')}_{recommendation_id}.csv"
    
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/soil-health-card/{recommendation_id}/pdf")
async def download_pdf(recommendation_id: int, db: Session = Depends(get_db)):
    recommendation = db.query(FertilizerRecommendation).filter(FertilizerRecommendation.id == recommendation_id).first()
    if not recommendation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recommendation with ID {recommendation_id} not found")
    
    farmer = db.query(Farmer).filter(Farmer.id == recommendation.farmer_id).first()
    soil_data = db.query(SoilData).filter(SoilData.id == recommendation.soil_data_id).first()
    if not farmer or not soil_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated farmer or soil data not found")
    
    farmer_dict = {'name': farmer.name, 'village': farmer.village, 'district': farmer.district, 'state': farmer.state, 'field_area': farmer.field_area, 'crop_name': farmer.crop_name, 'crop_season': farmer.crop_season.value}
    soil_dict = {'nitrogen': soil_data.nitrogen, 'phosphorus': soil_data.phosphorus, 'potassium': soil_data.potassium, 'ph': soil_data.ph, 'ec': soil_data.ec, 'moisture': soil_data.moisture, 'organic_carbon': soil_data.organic_carbon, 'sample_id': soil_data.sample_id}
    recommendation_dict = {'required_nitrogen': recommendation.required_nitrogen, 'required_phosphorus': recommendation.required_phosphorus, 'required_potassium': recommendation.required_potassium, 'fertilizer_name': recommendation.fertilizer_name, 'quantity_kg_per_hectare': recommendation.quantity_kg_per_hectare, 'quantity_kg_per_acre': recommendation.quantity_kg_per_acre, 'estimated_cost': recommendation.estimated_cost, 'additional_data': recommendation.reasoning}
    
    pdf_bytes = generate_pdf(farmer_dict, soil_dict, recommendation_dict)
    output = io.BytesIO(pdf_bytes)
    filename = f"SoilHealthCard_{farmer.name.replace(' ', '_')}_{recommendation_id}.pdf"
    return StreamingResponse(output, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})


@router.get("/soil-health-card/{recommendation_id}/excel")
async def download_excel(recommendation_id: int, db: Session = Depends(get_db)):
    recommendation = db.query(FertilizerRecommendation).filter(FertilizerRecommendation.id == recommendation_id).first()
    if not recommendation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recommendation with ID {recommendation_id} not found")
    
    farmer = db.query(Farmer).filter(Farmer.id == recommendation.farmer_id).first()
    soil_data = db.query(SoilData).filter(SoilData.id == recommendation.soil_data_id).first()
    if not farmer or not soil_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated farmer or soil data not found")
    
    farmer_dict = {'name': farmer.name, 'village': farmer.village, 'district': farmer.district, 'state': farmer.state, 'field_area': farmer.field_area, 'crop_name': farmer.crop_name, 'crop_season': farmer.crop_season.value}
    soil_dict = {'nitrogen': soil_data.nitrogen, 'phosphorus': soil_data.phosphorus, 'potassium': soil_data.potassium, 'ph': soil_data.ph, 'ec': soil_data.ec, 'moisture': soil_data.moisture, 'organic_carbon': soil_data.organic_carbon, 'sample_id': soil_data.sample_id}
    recommendation_dict = {'required_nitrogen': recommendation.required_nitrogen, 'required_phosphorus': recommendation.required_phosphorus, 'required_potassium': recommendation.required_potassium, 'fertilizer_name': recommendation.fertilizer_name, 'quantity_kg_per_hectare': recommendation.quantity_kg_per_hectare, 'quantity_kg_per_acre': recommendation.quantity_kg_per_acre, 'estimated_cost': recommendation.estimated_cost, 'additional_data': recommendation.reasoning}
    
    excel_bytes = generate_excel(farmer_dict, soil_dict, recommendation_dict)
    output = io.BytesIO(excel_bytes)
    filename = f"SoilHealthCard_{farmer.name.replace(' ', '_')}_{recommendation_id}.xlsx"
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})
