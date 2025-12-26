"""
CSV and JSON generators for Soil Health Card data export
"""
import csv
import json
import os
from datetime import datetime


class CSVJSONGenerator:
    """Generate CSV and JSON exports of Soil Health Card data"""
    
    @staticmethod
    def generate_csv(
        farmer_data: dict,
        soil_data: dict,
        card_id: str,
        output_path: str = None
    ) -> str:
        """Generate CSV export"""
        if output_path is None:
            os.makedirs("reports/csv", exist_ok=True)
            output_path = f"reports/csv/soil_health_card_{card_id}.csv"
        
        # Prepare data rows
        data = [
            ["SOIL HEALTH CARD"],
            ["Card ID", card_id],
            ["Issue Date", datetime.utcnow().strftime('%Y-%m-%d')],
            [],
            ["FARMER DETAILS"],
            ["Name", farmer_data.get('name', 'N/A')],
            ["Mobile", farmer_data.get('mobile', 'N/A')],
            ["Village", farmer_data.get('village', 'N/A')],
            ["District", farmer_data.get('district', 'N/A')],
            ["State", farmer_data.get('state', 'N/A')],
            ["Field Area (hectares)", farmer_data.get('field_area', 'N/A')],
            ["Crop", farmer_data.get('crop_name', 'N/A')],
            ["Season", farmer_data.get('crop_season', 'N/A')],
            [],
            ["SOIL SAMPLE DETAILS"],
            ["Sample ID", soil_data.get('sample_id', 'N/A')],
            ["Collection Date", soil_data.get('collection_date', 'N/A')],
            ["Data Source", soil_data.get('data_source', 'N/A').upper()],
            [],
            ["SOIL TEST RESULTS"],
            ["Parameter", "Value", "Unit", "Status"],
            ["Nitrogen (N)", 
             f"{soil_data.get('nitrogen'):.1f}" if soil_data.get('nitrogen') is not None else "N/A",
             "mg/kg",
             CSVJSONGenerator._get_nutrient_status(soil_data.get('nitrogen'), 'nitrogen')],
            ["Phosphorus (P)",
             f"{soil_data.get('phosphorus'):.1f}" if soil_data.get('phosphorus') is not None else "N/A",
             "mg/kg",
             CSVJSONGenerator._get_nutrient_status(soil_data.get('phosphorus'), 'phosphorus')],
            ["Potassium (K)",
             f"{soil_data.get('potassium'):.1f}" if soil_data.get('potassium') is not None else "N/A",
             "mg/kg",
             CSVJSONGenerator._get_nutrient_status(soil_data.get('potassium'), 'potassium')],
            ["pH",
             f"{soil_data.get('ph'):.1f}" if soil_data.get('ph') is not None else "N/A",
             "-",
             CSVJSONGenerator._get_ph_status(soil_data.get('ph'))],
            ["EC",
             f"{soil_data.get('ec'):.2f}" if soil_data.get('ec') is not None else "N/A",
             "dS/m",
             CSVJSONGenerator._get_ec_status(soil_data.get('ec'))],
        ]
        
        # Add optional parameters
        if soil_data.get('moisture') is not None:
            data.append([
                "Moisture",
                f"{soil_data.get('moisture'):.1f}",
                "%",
                "Tested"
            ])
        
        if soil_data.get('organic_carbon') is not None:
            oc = soil_data.get('organic_carbon')
            status = "Low" if oc < 0.5 else "Medium" if oc < 0.75 else "High"
            data.append([
                "Organic Carbon",
                f"{oc:.2f}",
                "%",
                status
            ])
        
        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        return output_path
    
    @staticmethod
    def generate_json(
        farmer_data: dict,
        soil_data: dict,
        card_id: str,
        output_path: str = None
    ) -> str:
        """Generate JSON export"""
        if output_path is None:
            os.makedirs("reports/json", exist_ok=True)
            output_path = f"reports/json/soil_health_card_{card_id}.json"
        
        # Prepare JSON structure
        json_data = {
            "soil_health_card": {
                "card_id": card_id,
                "issue_date": datetime.utcnow().strftime('%Y-%m-%d'),
                "farmer_details": {
                    "name": farmer_data.get('name', 'N/A'),
                    "mobile": farmer_data.get('mobile', 'N/A'),
                    "address": {
                        "village": farmer_data.get('village', 'N/A'),
                        "district": farmer_data.get('district', 'N/A'),
                        "state": farmer_data.get('state', 'N/A')
                    },
                    "field_area_hectares": farmer_data.get('field_area', 'N/A'),
                    "crop_name": farmer_data.get('crop_name', 'N/A'),
                    "crop_season": farmer_data.get('crop_season', 'N/A')
                },
                "soil_sample": {
                    "sample_id": soil_data.get('sample_id', 'N/A'),
                    "collection_date": soil_data.get('collection_date', 'N/A'),
                    "data_source": soil_data.get('data_source', 'N/A')
                },
                "soil_test_results": {
                    "nitrogen": {
                        "value": soil_data.get('nitrogen'),
                        "unit": "mg/kg",
                        "status": CSVJSONGenerator._get_nutrient_status(soil_data.get('nitrogen'), 'nitrogen')
                    },
                    "phosphorus": {
                        "value": soil_data.get('phosphorus'),
                        "unit": "mg/kg",
                        "status": CSVJSONGenerator._get_nutrient_status(soil_data.get('phosphorus'), 'phosphorus')
                    },
                    "potassium": {
                        "value": soil_data.get('potassium'),
                        "unit": "mg/kg",
                        "status": CSVJSONGenerator._get_nutrient_status(soil_data.get('potassium'), 'potassium')
                    },
                    "ph": {
                        "value": soil_data.get('ph'),
                        "unit": "-",
                        "status": CSVJSONGenerator._get_ph_status(soil_data.get('ph'))
                    },
                    "ec": {
                        "value": soil_data.get('ec'),
                        "unit": "dS/m",
                        "status": CSVJSONGenerator._get_ec_status(soil_data.get('ec'))
                    }
                }
            }
        }
        
        # Add optional parameters
        if soil_data.get('moisture') is not None:
            json_data["soil_health_card"]["soil_test_results"]["moisture"] = {
                "value": soil_data.get('moisture'),
                "unit": "%",
                "status": "Tested"
            }
        
        if soil_data.get('organic_carbon') is not None:
            oc = soil_data.get('organic_carbon')
            status = "Low" if oc < 0.5 else "Medium" if oc < 0.75 else "High"
            json_data["soil_health_card"]["soil_test_results"]["organic_carbon"] = {
                "value": oc,
                "unit": "%",
                "status": status
            }
        
        # Write JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    @staticmethod
    def _get_nutrient_status(value, param):
        """Get nutrient status classification"""
        if value is None:
            return "Not Tested"
        if param in ['nitrogen', 'phosphorus', 'potassium']:
            if value < 15:
                return "Low"
            elif value < 25:
                return "Medium"
            else:
                return "High"
        return "Tested"
    
    @staticmethod
    def _get_ph_status(ph):
        """Get pH status classification"""
        if ph is None:
            return "Not Tested"
        if ph < 6.5:
            return "Acidic"
        elif ph <= 7.5:
            return "Neutral"
        else:
            return "Alkaline"
    
    @staticmethod
    def _get_ec_status(ec):
        """Get EC status classification"""
        if ec is None:
            return "Not Tested"
        return "Normal" if ec <= 2.0 else "High"
