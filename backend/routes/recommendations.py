"""
Recommendations API routes
Generate ML-based fertilizer recommendations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import FertilizerRecommendation, SoilData, Farmer
from schemas import RecommendationCreate, RecommendationResponse
from ml import get_predictor, FertilizerRecommendationEngine, generate_recommendation_summary
from ml.soil_improvement import get_soil_improvements
from ml.crop_schedules import get_application_schedule

router = APIRouter()


@router.post("/recommendations/generate", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
async def generate_recommendation(
    request: RecommendationCreate,
    db: Session = Depends(get_db)
):
    """
    Generate fertilizer recommendation based on soil data
    Uses ML model to predict nutrient requirements and maps to fertilizers
    """
    # Verify farmer exists
    farmer = db.query(Farmer).filter(Farmer.id == request.farmer_id).first()
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Farmer with ID {request.farmer_id} not found"
        )
    
    # Verify soil data exists
    soil_data = db.query(SoilData).filter(SoilData.id == request.soil_data_id).first()
    if not soil_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Soil data with ID {request.soil_data_id} not found"
        )
    
    # Check if soil data has required parameters for ML
    if not all([
        soil_data.nitrogen is not None,
        soil_data.phosphorus is not None,
        soil_data.potassium is not None,
        soil_data.ph is not None
    ]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Soil data must have N, P, K, and pH values for generating recommendations"
        )
    
    # Get ML predictor
    predictor = get_predictor()
    
    # Predict nutrient requirements
    required_n, required_p, required_k = predictor.predict_nutrients(
        nitrogen=soil_data.nitrogen,
        phosphorus=soil_data.phosphorus,
        potassium=soil_data.potassium,
        ph=soil_data.ph,
        ec=soil_data.ec or 1.0,  # Default EC if not available
        moisture=soil_data.moisture or 30.0,  # Default moisture if not available
        crop=farmer.crop_name,
        season=farmer.crop_season.value
    )
    
    # Generate fertilizer recommendations
    field_area_hectares = farmer.field_area  # Assuming field_area is in hectares
    fertilizer_recommendations = FertilizerRecommendationEngine.recommend_fertilizers(
        required_n=required_n,
        required_p=required_p,
        required_k=required_k,
        field_area_hectares=field_area_hectares
    )
    
    # Format fertilizer names and quantities
    fertilizer_names = ", ".join([f['fertilizer'] for f in fertilizer_recommendations['fertilizers']])
    total_quantity_per_hectare = sum([f['quantity_kg_per_hectare'] for f in fertilizer_recommendations['fertilizers']])
    total_quantity_per_acre = total_quantity_per_hectare * 0.4047
    
    # Generate reasoning
    soil_data_dict = {
        'nitrogen': soil_data.nitrogen,
        'phosphorus': soil_data.phosphorus,
        'potassium': soil_data.potassium,
        'ph': soil_data.ph,
        'ec': soil_data.ec
    }
    
    reasoning = predictor.generate_reasoning(
        soil_data=soil_data_dict,
        crop=farmer.crop_name,
        season=farmer.crop_season.value,
        required_n=required_n,
        required_p=required_p,
        required_k=required_k
    )
    
    # Add fertilizer recommendation details to reasoning
    reasoning += "\n\n" + generate_recommendation_summary(fertilizer_recommendations)
    
    # Get weather-based timing advice (non-critical, wrap in try-except)
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from ..services.weather import WeatherService, get_location_coords
        lat, lon = get_location_coords(farmer.district)
        weather_advice = WeatherService.get_fertilizer_timing_advice(lat, lon)
        if weather_advice and weather_advice != "Weather data unavailable":
            reasoning += f"\n\n**Weather Advisory:** {weather_advice}"
    except Exception as e:
        # Weather is optional, don't break if it fails
        print(f"Weather service skipped: {e}")
    
    # Generate soil improvement recommendations
    soil_improvements = get_soil_improvements(
        ph=soil_data.ph,
        ec=soil_data.ec,
        organic_carbon=soil_data.organic_carbon,
        nitrogen=soil_data.nitrogen,
        phosphorus=soil_data.phosphorus,
        potassium=soil_data.potassium
    )
    
    # Generate application schedule
    application_schedule = get_application_schedule(
        crop_name=farmer.crop_name,
        total_n=required_n,
        total_p=required_p,
        total_k=required_k
    )
    
    # Add prices to fertilizer details and Recalculate Total Cost
    from ml.fertilizer_prices import FERTILIZER_PRICES_INR
    import math

    recalculated_total_cost = 0.0
    
    for fert in fertilizer_recommendations['fertilizers']:
        fert_name = fert['fertilizer'].split('(')[0].strip()  # Extract base name
        
        # Calculate quantity total if not present (logic from ML engine might vary)
        if 'quantity_total' not in fert:
            fert['quantity_total'] = fert['quantity_kg_per_hectare'] * farmer.field_area

        bags_required = math.ceil(fert['quantity_total'] / 50)
        
        if fert_name in FERTILIZER_PRICES_INR:
            price = FERTILIZER_PRICES_INR[fert_name]['price_per_50kg']
            fert['price_per_50kg'] = price
            fert['cost'] = bags_required * price
            fert['is_verified'] = True
            recalculated_total_cost += fert['cost']
        else:
            # Mark as unverified or unavailable
            fert['price_per_50kg'] = "Govt. price not available"
            fert['cost'] = 0 # Exclude from total cost
            fert['is_verified'] = False
            fert['note'] = "Price not verified by Govt of India"
    
    # Check if biofertilizer is needed (conditional)
    biofertilizer_needed = False
    if soil_data.organic_carbon is not None and soil_data.organic_carbon < 0.75:
        biofertilizer_needed = True
        # Add biofertilizer recommendation
        bio_qty_total = 2.0 * farmer.field_area
        
        fertilizer_recommendations['fertilizers'].append({
            'fertilizer': 'Biofertilizer (Rhizobium/Azotobacter)',
            'quantity_kg_per_hectare': 2.0,
            'quantity_kg_per_acre': 0.81,
            'quantity_total': bio_qty_total,
            'provides': 'Nitrogen fixing, Organic carbon boost',
            'cost': 0, # Exclude from verified total
            'price_per_50kg': "Govt. price not available", 
            'is_verified': False,
            'application_stage': 'Seed Treatment'
        })
        
    # Update the total cost in the main object
    fertilizer_recommendations['total_cost'] = recalculated_total_cost
    
    # Store additional data in JSON format (for now, until we add dedicated fields)
    import json
    additional_data = {
        'soil_improvements': soil_improvements,
        'application_schedule': application_schedule,
        'fertilizer_details': fertilizer_recommendations['fertilizers'],
        'biofertilizer_recommended': biofertilizer_needed
    }
    
    # Create recommendation record
    recommendation = FertilizerRecommendation(
        farmer_id=request.farmer_id,
        soil_data_id=request.soil_data_id,
        required_nitrogen=required_n,
        required_phosphorus=required_p,
        required_potassium=required_k,
        fertilizer_name=fertilizer_names,
        quantity_kg_per_hectare=round(total_quantity_per_hectare, 2),
        quantity_kg_per_acre=round(total_quantity_per_acre, 2),
        application_timing=fertilizer_recommendations['application_timing'],
        application_method=fertilizer_recommendations['application_method'],
        estimated_cost=fertilizer_recommendations['total_cost'],
        reasoning=reasoning + "\n\n" + json.dumps(additional_data)
    )
    
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    
    return recommendation


@router.get("/recommendations/{recommendation_id}", response_model=RecommendationResponse)
async def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    """
    Get recommendation details by ID
    """
    recommendation = db.query(FertilizerRecommendation).filter(
        FertilizerRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation with ID {recommendation_id} not found"
        )
    
    return recommendation


@router.get("/recommendations/farmer/{farmer_id}", response_model=list[RecommendationResponse])
async def get_farmer_recommendations(farmer_id: int, db: Session = Depends(get_db)):
    """
    Get all recommendations for a farmer
    """
    recommendations = db.query(FertilizerRecommendation).filter(
        FertilizerRecommendation.farmer_id == farmer_id
    ).all()
    
    return recommendations
