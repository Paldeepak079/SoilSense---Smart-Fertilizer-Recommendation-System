"""
Train Random Forest Regressor for nutrient prediction
Generates synthetic training data based on agricultural reference values
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os


def generate_training_data(n_samples=1000):
    """
    Generate synthetic training dataset for nutrient prediction
    Based on standard agricultural reference values for different crops
    """
    np.random.seed(42)
    
    crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Potato', 'Tomato', 'Onion', 'Soybean', 'Groundnut']
    seasons = ['Kharif', 'Rabi', 'Zaid']
    
    data = []
    
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        season = np.random.choice(seasons)
        
        # Generate soil parameters with realistic ranges
        nitrogen = np.random.uniform(5, 45)  # mg/kg
        phosphorus = np.random.uniform(5, 45)  # mg/kg
        potassium = np.random.uniform(5, 45)  # mg/kg
        ph = np.random.uniform(4.5, 8.5)
        ec = np.random.uniform(0.1, 3.0)  # dS/m
        moisture = np.random.uniform(10, 60)  # %
        
        # Calculate required nutrients based on crop needs and soil deficiency
        # These are simplified formulas - in production, use actual crop requirement data
        
        # Nitrogen requirement (kg/ha)
        if crop in ['Rice', 'Wheat', 'Maize']:
            base_n = 120
        elif crop in ['Cotton', 'Sugarcane']:
            base_n = 150
        else:
            base_n = 80
        
        # Adjust based on soil nitrogen level
        n_deficiency = max(0, 40 - nitrogen)
        required_n = base_n * (1 + n_deficiency / 40)
        
        # Phosphorus requirement (kg/ha)
        if crop in ['Cotton', 'Potato', 'Tomato']:
            base_p = 60
        elif crop in ['Sugarcane']:
            base_p = 80
        else:
            base_p = 40
        
        p_deficiency = max(0, 35 - phosphorus)
        required_p = base_p * (1 + p_deficiency / 35)
        
        # Potassium requirement (kg/ha)
        if crop in ['Sugarcane', 'Potato']:
            base_k = 80
        elif crop in ['Cotton', 'Wheat']:
            base_k = 40
        else:
            base_k = 30
        
        k_deficiency = max(0, 35 - potassium)
        required_k = base_k * (1 + k_deficiency / 35)
        
        # Season adjustments
        if season == 'Kharif':  # Monsoon season - more nutrients
            required_n *= 1.1
            required_p *= 1.05
        elif season == 'Rabi':  # Winter season
            required_p *= 1.1  # More P for root development
        
        # pH and EC adjustments
        if ph < 5.5 or ph > 7.5:  # Acidic or alkaline soil
            required_p *= 1.2  # More P needed due to poor availability
        
        if ec > 2.0:  # Saline soil
            required_k *= 1.15  # More K for salt tolerance
        
        data.append({
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'ph': ph,
            'ec': ec,
            'moisture': moisture,
            'crop': crop,
            'season': season,
            'required_nitrogen': required_n,
            'required_phosphorus': required_p,
            'required_potassium': required_k
        })
    
    return pd.DataFrame(data)


def train_model():
    """
    Train Random Forest Regressor model
    """
    print("Generating training data...")
    df = generate_training_data(n_samples=2000)
    
    # Encode categorical variables
    le_crop = LabelEncoder()
    le_season = LabelEncoder()
    
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    df['season_encoded'] = le_season.fit_transform(df['season'])
    
    # Prepare features and targets
    feature_columns = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'ec', 'moisture', 'crop_encoded', 'season_encoded']
    target_columns = ['required_nitrogen', 'required_phosphorus', 'required_potassium']
    
    X = df[feature_columns]
    y = df[target_columns]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training R² score: {train_score:.4f}")
    print(f"Testing R² score: {test_score:.4f}")
    
    # Save model and encoders
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(model_dir, 'nutrient_model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    with open(os.path.join(model_dir, 'crop_encoder.pkl'), 'wb') as f:
        pickle.dump(le_crop, f)
    
    with open(os.path.join(model_dir, 'season_encoder.pkl'), 'wb') as f:
        pickle.dump(le_season, f)
    
    print("Model saved successfully!")
    print(f"Model path: {os.path.join(model_dir, 'nutrient_model.pkl')}")
    
    return model, le_crop, le_season


if __name__ == "__main__":
    train_model()
