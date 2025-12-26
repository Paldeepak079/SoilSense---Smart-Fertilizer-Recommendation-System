"""
ML inference engine for nutrient prediction
"""
import pickle
import numpy as np
import os
from typing import Dict, Tuple


class NutrientPredictor:
    """ML model inference for predicting required nutrients"""
    
    def __init__(self):
        """Load trained model and encoders"""
        model_dir = os.path.dirname(os.path.abspath(__file__))
        
        model_path = os.path.join(model_dir, 'nutrient_model.pkl')
        crop_encoder_path = os.path.join(model_dir, 'crop_encoder.pkl')
        season_encoder_path = os.path.join(model_dir, 'season_encoder.pkl')
        
        # Check if model exists, if not train it
        if not os.path.exists(model_path):
            print("Model not found. Training new model...")
            from .train_model import train_model
            train_model()
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(crop_encoder_path, 'rb') as f:
            self.crop_encoder = pickle.load(f)
        
        with open(season_encoder_path, 'rb') as f:
            self.season_encoder = pickle.load(f)
    
    def predict_nutrients(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float,
        ec: float,
        moisture: float,
        crop: str,
        season: str
    ) -> Tuple[float, float, float]:
        """
        Predict required nutrients (N, P, K) in kg/ha
        
        Args:
            nitrogen: Soil nitrogen (mg/kg)
            phosphorus: Soil phosphorus (mg/kg)
            potassium: Soil potassium (mg/kg)
            ph: Soil pH
            ec: Electrical conductivity (dS/m)
            moisture: Soil moisture (%)
            crop: Crop name
            season: Season (Kharif/Rabi/Zaid)
        
        Returns:
            Tuple of (required_N, required_P, required_K) in kg/ha
        """
        # Handle unknown crops  with default encoding
        try:
            crop_encoded = self.crop_encoder.transform([crop])[0]
        except ValueError:
            # Use most common crop as default
            crop_encoded = self.crop_encoder.transform(['Rice'])[0]
            print(f"Warning: Unknown crop '{crop}', using 'Rice' as default")
        
        # Handle unknown seasons
        try:
            season_encoded = self.season_encoder.transform([season])[0]
        except ValueError:
            season_encoded = self.season_encoder.transform(['Kharif'])[0]
            print(f"Warning: Unknown season '{season}', using 'Kharif' as default")
        
        # Prepare features
        features = np.array([[
            nitrogen,
            phosphorus,
            potassium,
            ph,
            ec,
            moisture,
            crop_encoded,
            season_encoded
        ]])
        
        # Predict
        prediction = self.model.predict(features)[0]
        
        required_n = max(0, prediction[0])  # Ensure non-negative
        required_p = max(0, prediction[1])
        required_k = max(0, prediction[2])
        
        return required_n, required_p, required_k
    
    def generate_reasoning(
        self,
        soil_data: Dict,
        crop: str,
        season: str,
        required_n: float,
        required_p: float,
        required_k: float
    ) -> str:
        """
        Generate human-readable reasoning for nutrient recommendations
        """
        reasoning_parts = []
        
        # Soil analysis
        reasoning_parts.append(f"**Soil Analysis for {crop} ({season} season)**\n")
        
        # Nitrogen assessment
        nitrogen = soil_data.get('nitrogen', 0)
        if nitrogen < 20:
            reasoning_parts.append(f"- Nitrogen level ({nitrogen:.1f} mg/kg) is LOW. Soil requires significant nitrogen supplementation.")
        elif nitrogen < 30:
            reasoning_parts.append(f"- Nitrogen level ({nitrogen:.1f} mg/kg) is MODERATE. Some nitrogen fertilization recommended.")
        else:
            reasoning_parts.append(f"- Nitrogen level ({nitrogen:.1f} mg/kg) is HIGH. Minimal nitrogen needed.")
        
        # Phosphorus assessment
        phosphorus = soil_data.get('phosphorus', 0)
        if phosphorus < 15:
            reasoning_parts.append(f"- Phosphorus level ({phosphorus:.1f} mg/kg) is LOW. Adequate P fertilization is critical.")
        elif phosphorus < 25:
            reasoning_parts.append(f"- Phosphorus level ({phosphorus:.1f} mg/kg) is MODERATE. Balanced P application needed.")
        else:
            reasoning_parts.append(f"- Phosphorus level ({phosphorus:.1f} mg/kg) is HIGH. Maintenance dose sufficient.")
        
        # Potassium assessment
        potassium = soil_data.get('potassium', 0)
        if potassium < 15:
            reasoning_parts.append(f"- Potassium level ({potassium:.1f} mg/kg) is LOW. K fertilizer essential for crop quality.")
        elif potassium < 25:
            reasoning_parts.append(f"- Potassium level ({potassium:.1f} mg/kg) is MODERATE. Standard K dose recommended.")
        else:
            reasoning_parts.append(f"- Potassium level ({potassium:.1f} mg/kg) is HIGH. Reduced K application acceptable.")
        
        # pH considerations
        ph = soil_data.get('ph', 7.0)
        if ph < 5.5:
            reasoning_parts.append(f"- Soil pH ({ph:.1f}) is ACIDIC. Consider liming to improve nutrient availability.")
        elif ph > 7.5:
            reasoning_parts.append(f"- Soil pH ({ph:.1f}) is ALKALINE. May affect phosphorus availability.")
        else:
            reasoning_parts.append(f"- Soil pH ({ph:.1f}) is NEUTRAL. Optimal for nutrient uptake.")
        
        # EC considerations
        ec = soil_data.get('ec', 0)
        if ec and ec > 2.0:
            reasoning_parts.append(f"- Electrical Conductivity ({ec:.1f} dS/m) is HIGH. Saline stress may occur; potassium helps tolerance.")
        
        # Final recommendation summary
        reasoning_parts.append(f"\n**Recommended Nutrients (kg/ha):**")
        reasoning_parts.append(f"- Nitrogen (N): {required_n:.1f} kg/ha")
        reasoning_parts.append(f"- Phosphorus (P₂O₅): {required_p:.1f} kg/ha")
        reasoning_parts.append(f"- Potassium (K₂O): {required_k:.1f} kg/ha")
        
        return "\n".join(reasoning_parts)


# Global predictor instance
_predictor = None

def get_predictor() -> NutrientPredictor:
    """Get or create predictor instance (singleton pattern)"""
    global _predictor
    if _predictor is None:
        _predictor = NutrientPredictor()
    return _predictor
