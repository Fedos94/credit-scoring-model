from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.predict_model import load_model

app = FastAPI(
    title="Credit Scoring API",
    description="API for predicting credit default probability",
    version="1.0.0"
)

# Load model
try:
    model = load_model()
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    model_loaded = False

class CreditData(BaseModel):
    LIMIT_BAL: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int
    AGE: int
    PAY_0: int
    PAY_2: int
    PAY_3: int
    PAY_4: int
    PAY_5: int
    PAY_6: int
    BILL_AMT1: float
    BILL_AMT2: float
    BILL_AMT3: float
    BILL_AMT4: float
    BILL_AMT5: float
    BILL_AMT6: float
    PAY_AMT1: float
    PAY_AMT2: float
    PAY_AMT3: float
    PAY_AMT4: float
    PAY_AMT5: float
    PAY_AMT6: float

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str

@app.get("/")
async def root():
    return {"message": "Credit Scoring API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": model_loaded}

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: CreditData):
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([data.dict()])
        
        # Make prediction
        prediction, probabilities = model.predict(input_data), model.predict_proba(input_data)
        probability = probabilities[0, 1]
        prediction_class = int(prediction[0])
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "low"
        elif probability < 0.7:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return PredictionResponse(
            prediction=prediction_class,
            probability=round(probability, 4),
            risk_level=risk_level
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.get("/model-info")
async def model_info():
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "features": model[:-1].get_feature_names_out().tolist() if hasattr(model, 'get_feature_names_out') else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)