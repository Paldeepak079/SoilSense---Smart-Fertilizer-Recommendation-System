"""
Soil Health Card generation service
Generates PDF, Excel, and CSV reports
"""
import csv
import io
from datetime import datetime
from typing import Dict

def generate_csv(farmer_data: Dict, soil_data: Dict, recommendation_data: Dict) -> str:
    """
    Generate CSV format Soil Health Card
    Returns CSV content as string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['SOIL HEALTH CARD'])
    writer.writerow(['Government of India - Department of Agriculture'])
    writer.writerow([])
    
    # Farmer Information
    writer.writerow(['FARMER INFORMATION'])
    writer.writerow(['Name', farmer_data.get('name', '')])
    writer.writerow(['Village', farmer_data.get('village', '')])
    writer.writerow(['District', farmer_data.get('district', '')])
    writer.writerow(['State', farmer_data.get('state', '')])
    writer.writerow(['Field Area (hectares)', farmer_data.get('field_area', '')])
    writer.writerow(['Crop', farmer_data.get('crop_name', '')])
    writer.writerow(['Season', farmer_data.get('crop_season', '')])
    writer.writerow([])
    
    # Soil Analysis
    writer.writerow(['SOIL ANALYSIS RESULTS'])
    writer.writerow(['Parameter', 'Value', 'Unit', 'Status'])
    writer.writerow(['Nitrogen (N)', soil_data.get('nitrogen', 'N/A'), 'mg/kg', get_nutrient_status(soil_data.get('nitrogen', 0), 20, 40)])
    writer.writerow(['Phosphorus (P)', soil_data.get('phosphorus', 'N/A'), 'mg/kg', get_nutrient_status(soil_data.get('phosphorus', 0), 15, 35)])
    writer.writerow(['Potassium (K)', soil_data.get('potassium', 'N/A'), 'mg/kg', get_nutrient_status(soil_data.get('potassium', 0), 20, 35)])
    writer.writerow(['pH', soil_data.get('ph', 'N/A'), '', get_ph_status(soil_data.get('ph', 7))])
    if soil_data.get('ec'):
        writer.writerow(['EC', soil_data.get('ec'), 'dS/m', 'Normal' if soil_data.get('ec', 0) < 2 else 'High'])
    if soil_data.get('moisture'):
        writer.writerow(['Moisture', soil_data.get('moisture'), '%', ''])
    if soil_data.get('organic_carbon'):
        writer.writerow(['Organic Carbon', soil_data.get('organic_carbon'), '%', ''])
    writer.writerow([])
    
    # Nutrient Requirements
    writer.writerow(['NUTRIENT REQUIREMENTS'])
    writer.writerow(['Nutrient', 'Required (kg/ha)'])
    writer.writerow(['Nitrogen (N)', f"{recommendation_data.get('required_nitrogen', 0):.2f}"])
    writer.writerow(['Phosphorus (P₂O₅)', f"{recommendation_data.get('required_phosphorus', 0):.2f}"])
    writer.writerow(['Potassium (K₂O)', f"{recommendation_data.get('required_potassium', 0):.2f}"])
    writer.writerow([])
    
    # Fertilizer Recommendations
    writer.writerow(['FERTILIZER RECOMMENDATIONS'])
    writer.writerow(['Fertilizer', 'Quantity (kg/ha)', 'Quantity (kg/acre)', 'Application Timing', 'Application Method'])
    
    # Parse fertilizers
    fertilizers = parse_fertilizers(recommendation_data.get('fertilizer_name', ''))
    qty_per_ha = recommendation_data.get('quantity_kg_per_hectare', 0) / len(fertilizers) if fertilizers else 0
    qty_per_acre = recommendation_data.get('quantity_kg_per_acre', 0) / len(fertilizers) if fertilizers else 0
    
    for fert in fertilizers:
        timing, method = get_fertilizer_application(fert['name'])
        writer.writerow([
            fert['name'],
            f"{qty_per_ha:.2f}",
            f"{qty_per_acre:.2f}",
            timing,
            method
        ])
    
    writer.writerow([])
    writer.writerow(['Total Estimated Cost', f"₹{recommendation_data.get('estimated_cost', 0)}"])
    writer.writerow([])
    
    # Application Schedule (Table 3)
    import json
    additional_data_str = recommendation_data.get('additional_data', '{}')
    try:
        additional_data = json.loads(additional_data_str) if isinstance(additional_data_str, str) else additional_data_str
    except:
        additional_data = {}
    
    application_schedule = additional_data.get('application_schedule', [])
    if application_schedule:
        writer.writerow(['APPLICATION SCHEDULE (Weather-Adjusted)'])
        writer.writerow(['Stage', 'Time', 'Fertilizer', 'Quantity %', 'Note'])
        for stage in application_schedule:
            writer.writerow([
                stage.get('stage', ''),
                stage.get('time', ''),
                stage.get('fertilizer', ''),
                f"{stage.get('quantity_percent', 0)}%",
                stage.get('note', '')
            ])
        writer.writerow([])
    
    # Soil Improvement Advisory (Table 4)
    soil_improvements = additional_data.get('soil_improvements', [])
    if soil_improvements:
        writer.writerow(['SOIL IMPROVEMENT ADVISORY'])
        writer.writerow(['Soil Issue', 'Recommendation', 'Quantity', 'Purpose'])
        for imp in soil_improvements:
            writer.writerow([
                imp.get('issue', ''),
                imp.get('recommendation', ''),
                imp.get('quantity', ''),
                imp.get('purpose', '')
            ])
        writer.writerow([])
    
    # Important Notes
    writer.writerow(['IMPORTANT NOTES'])
    writer.writerow(['• Soil test validity: One cropping season'])
    writer.writerow(['• Follow split application schedules as recommended'])
    writer.writerow(['• Apply during appropriate soil moisture conditions'])
    writer.writerow(['• Use organic manure (FYM/compost) @ 5-10 tonnes/ha'])
    writer.writerow(['• Contact Krishi Vigyan Kendra (KVK) for field-specific guidance'])
    writer.writerow([])
    
    # Footer
    writer.writerow(['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['Sample ID:', soil_data.get('sample_id', '')])
    
    return output.getvalue()


def get_nutrient_status(value: float, low_threshold: float, high_threshold: float) -> str:
    """Get nutrient status based on value"""
    if value < low_threshold:
        return 'Low'
    elif value > high_threshold:
        return 'High'
    return 'Medium'


def get_ph_status(ph: float) -> str:
    """Get pH status"""
    if ph < 5.5:
        return 'Acidic'
    elif ph > 7.5:
        return 'Alkaline'
    return 'Neutral'


def parse_fertilizers(fertilizer_name: str):
    """Parse fertilizer names into list"""
    if not fertilizer_name:
        return []
    
    fertilizers = []
    for f in fertilizer_name.split(','):
        f = f.strip()
        if 'Urea' in f:
            fertilizers.append({'name': 'Urea', 'price': 266})
        elif 'DAP' in f:
            fertilizers.append({'name': 'DAP', 'price': 1350})
        elif 'MOP' in f:
            fertilizers.append({'name': 'MOP', 'price': 1700})
        else:
            fertilizers.append({'name': f, 'price': 1450})
    
    return fertilizers


def get_fertilizer_application(fertilizer_name: str):
    """Get application timing and method for specific fertilizer"""
    applications = {
        'Urea': (
            'Split: 1/3 Basal + 1/3 at 30 days + 1/3 at 60 days',
            'Broadcasting with irrigation'
        ),
        'DAP': (
            '100% at Basal (before sowing)',
            'Deep placement 5-7cm below soil'
        ),
        'MOP': (
            '50% Basal + 50% at flowering',
            'Broadcasting and soil incorporation'
        ),
        'NPK': (
            '100% at Basal',
            'Broadcasting and mixing'
        )
    }
    
    return applications.get(fertilizer_name, ('At Basal', 'Broadcasting'))
