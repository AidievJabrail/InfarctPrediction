from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from catboost import CatBoostClassifier
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CatBoost Prediction API")

# Загрузка модели
try:
    model = CatBoostClassifier()
    model.load_model('/root/Project/catboostApi/catboost.cbm')
    logger.info("CatBoost model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

class HeartData(BaseModel):
    age: int 
    height: int  # в см
    weight: int  # в килограммах
    gender: int  # 1-муж, 2-жен
    angina: int  # 1-да, 2-нет
    stroke: int  # 1-да, 2-нет
    health_status: int  # 1-5
    cholesterol: int  # 1-да, 2-нет
    cigarettes: int  # 1-да, 2-нет
    marital_status: int  # 1-6
    employment: int  # 1-8
    copd: int  # 1-да, 2-нет
    personal_doctor: int  # 1-да, 2-нет
    depression: int  # 1-да, 2-нет
    walking_difficulty: int  # 1-да, 2-нет
    last_checkup: int  # 1-4,8
    hypertension: int  # 1-4
    diabetes: int  # 1-4
    
FEATURE_ORDER = [
    "age",
    "gender",
    "angina",
    "stroke",
    "health_status",
    "cholesterol",
    "cigarettes",
    "marital_status",
    "employment",
    "copd",
    "personal_doctor",
    "depression",
    "walking_difficulty",
    "last_checkup",
    "hypertension",
    "diabetes",
    "height",
    "weight"
]


@app.post("/predict")
async def predict(data: HeartData):
    try:
        input_data = np.array([getattr(data, feature) for feature in FEATURE_ORDER])
        prediction = model.predict(input_data)
        
        return {
            "prediction": int(prediction)
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
