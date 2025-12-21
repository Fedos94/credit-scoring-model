from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
import json
import os

app = FastAPI(title="Credit Scoring API")
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Пути к файлам модели
MODEL_PATH = os.getenv("MODEL_PATH", "/app/credit_model.onnx")
MODEL_DATA_PATH = os.path.join(os.path.dirname(MODEL_PATH), "credit_model.onnx.data")

# Проверка файлов
print(f"Основной файл модели: {MODEL_PATH}")
print(f"Файл данных модели: {MODEL_DATA_PATH}")
print(f"Существует основной: {os.path.exists(MODEL_PATH)}")
print(f"Существуют данные: {os.path.exists(MODEL_DATA_PATH)}")
@app.get("/")
async def root():
    return {
        "service": "Credit Scoring API",
        "version": "1.0.0",
        "status": "running",
        "model": {
            "loaded": session is not None,
            "path": MODEL_PATH,
            "input_name": input_name if session else None,
            "output_name": output_name if session else None
        },
        "endpoints": {
            "root": "GET /",
            "health": "GET /health",
            "predict": "POST /predict",
            "docs": "GET /docs",
            "openapi": "GET /openapi.json"
        },
        "documentation": "Visit /docs for interactive API documentation"
    }
# Загружаем ONNX модель
try:
    session_options = ort.SessionOptions()
    session = ort.InferenceSession(MODEL_PATH, session_options)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    print(f"✅ Модель загружена. Вход: {input_name}, Выход: {output_name}")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    session = None

# Модель запроса
class PredictionRequest(BaseModel):
    features: list[float]

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if session is not None else "error",
        "model_loaded": session is not None,
        "model_path": MODEL_PATH,
        "data_path": MODEL_DATA_PATH
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    if session is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        input_data = np.array([request.features], dtype=np.float32)
        prediction = session.run([output_name], {input_name: input_data})[0]
        
        return {
            "score": float(prediction[0][0]),
            "features_used": len(request.features)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)