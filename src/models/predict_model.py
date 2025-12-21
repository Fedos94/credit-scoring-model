import joblib
import pandas as pd
import numpy as np
import os

def load_model(model_path: str = None):
    """Load trained model"""
    if model_path is None:
        model_path = 'models/best_model.pkl'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    return joblib.load(model_path)

def predict(model, data):
    """Make predictions using trained model"""
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)
    
    return predictions, probabilities

def predict_proba(model, data):
    """Get prediction probabilities"""
    _, probabilities = predict(model, data)
    return probabilities[:, 1]  # Return probabilities for positive class