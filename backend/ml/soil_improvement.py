"""
Soil Improvement Recommendation Engine
Provides soil amendment recommendations based on pH, EC, and Organic Carbon
"""
from typing import List, Dict


def get_soil_improvements(
    ph: float,
    ec: float = None,
    organic_carbon: float = None,
    nitrogen: float = None,
    phosphorus: float = None,
    potassium: float = None
) -> List[Dict[str, str]]:
    """
    Generate soil improvement recommendations
    
    Returns:
        List of dicts with: issue, recommendation, quantity, purpose
    """
    improvements = []
    
    # pH-based recommendations
    if ph < 5.5:
        # Acidic soil - needs lime
        lime_qty = calculate_lime_requirement(ph)
        improvements.append({
            'issue': 'Acidic Soil (pH < 5.5)',
            'recommendation': 'Agricultural Lime (CaCO₃)',
            'quantity': f'{lime_qty} kg/ha',
            'purpose': 'Raise pH to neutral range (6.0-7.0), improve nutrient availability'
        })
    elif ph > 7.5:
        # Alkaline soil - needs gypsum or sulfur
        gypsum_qty = calculate_gypsum_requirement(ph)
        improvements.append({
            'issue': 'Alkaline Soil (pH > 7.5)',
            'recommendation': 'Gypsum (CaSO₄·2H₂O)',
            'quantity': f'{gypsum_qty} kg/ha',
            'purpose': 'Lower pH, improve phosphorus availability, reduce sodicity'
        })
    
    # EC-based recommendations (salinity)
    if ec and ec > 2.0:
        improvements.append({
            'issue': 'High Salinity (EC > 2.0 dS/m)',
            'recommendation': 'Gypsum + Leaching',
            'quantity': '500-750 kg/ha + 7.5cm irrigation',
            'purpose': 'Displace sodium, improve soil structure, leach excess salts'
        })
    
    # Organic Carbon recommendations
    if organic_carbon is not None and organic_carbon < 0.5:
        improvements.append({
            'issue': 'Low Organic Matter (OC < 0.5%)',
            'recommendation': 'Farmyard Manure (FYM) or Compost',
            'quantity': '8-10 tonnes/ha',
            'purpose': 'Improve soil structure, water retention, microbial activity'
        })
    elif organic_carbon is not None and 0.5 <= organic_carbon < 0.75:
        improvements.append({
            'issue': 'Moderate Organic Matter',
            'recommendation': 'Farmyard Manure (FYM) or Vermicompost',
            'quantity': '5-7 tonnes/ha',
            'purpose': 'Maintain soil health, enhance nutrient cycling'
        })
    
    # Specific nutrient deficiency amendments
    if phosphorus is not None and phosphorus < 10:
        improvements.append({
            'issue': 'Very Low Phosphorus',
            'recommendation': 'Rock Phosphate or Bone Meal',
            'quantity': '300-400 kg/ha',
            'purpose': 'Long-term P availability, especially in acidic soils'
        })
    
    # Green manure recommendation for overall soil health
    if len(improvements) >= 2:  # Multiple issues
        improvements.append({
            'issue': 'Multiple Soil Health Issues',
            'recommendation': 'Green Manure (Dhaincha/Sunhemp)',
            'quantity': '20-25 kg seed/ha',
            'purpose': 'Add organic matter, fix nitrogen, break pest cycles'
        })
    
    # If no specific issues, still recommend maintenance
    if not improvements:
        improvements.append({
            'issue': 'Soil Health Maintenance',
            'recommendation': 'Farmyard Manure (FYM)',
            'quantity': '3-5 tonnes/ha',
            'purpose': 'Maintain optimal soil conditions, sustained productivity'
        })
    
    return improvements


def calculate_lime_requirement(ph: float) -> int:
    """
    Calculate lime requirement based on pH
    For raising pH by 0.5 units: ~500-600 kg/ha lime needed
    """
    target_ph = 6.5
    ph_increase_needed = target_ph - ph
    
    if ph_increase_needed <= 0:
        return 0
    
    # Approximate: 500 kg lime per 0.5 pH unit increase
    lime_kg = int(ph_increase_needed * 1000)
    
    # Cap at reasonable limits
    return min(max(lime_kg, 500), 3000)


def calculate_gypsum_requirement(ph: float) -> int:
    """
    Calculate gypsum requirement for alkaline soils
    """
    if ph <= 7.5:
        return 0
    
    # Base requirement: 250-500 kg/ha for pH 7.5-8.0
    # Higher for more alkaline soils
    if ph > 8.5:
        return 750
    elif ph > 8.0:
        return 500
    else:
        return 350
