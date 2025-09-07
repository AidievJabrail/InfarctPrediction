from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from catboost import CatBoostClassifier
import sqlite3
import numpy as np
import logging
import os

MODEL_API_PORT= int(os.getenv('MODEL_API_PORT'))



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/model-api",  
    title="CatBoost Prediction API",
    )

try:
    model = CatBoostClassifier()
    model.load_model('catboost.cbm')
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

def save_prediction_to_db(user_data: dict, prediction_result: int):
    conn = sqlite3.connect('logger.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (
            timestamp, age, height, weight, gender, angina, stroke, 
            health_status, cholesterol, cigarettes, marital_status, 
            employment, copd, personal_doctor, depression, 
            walking_difficulty, last_checkup, hypertension, diabetes, 
            model_prediction
        ) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data.age,
            user_data.height,
            user_data.weight,
            user_data.gender,
            user_data.angina,
            user_data.stroke,
            user_data.health_status,
            user_data.cholesterol,
            user_data.cigarettes,
            user_data.marital_status,
            user_data.employment,
            user_data.copd,
            user_data.personal_doctor,
            user_data.depression,
            user_data.walking_difficulty,
            user_data.last_checkup,
            user_data.hypertension,
            user_data.diabetes,
            prediction_result
        ))
    
    conn.commit()
    conn.close()




@app.post("/predict")
async def predict(data: HeartData):
    try:
        input_data = np.array([getattr(data, feature) for feature in FEATURE_ORDER])
        prediction = model.predict(input_data)
        try:
            save_prediction_to_db(user_data=data,prediction_result=prediction)
            logger.info(f"Успешное сохранение в БД")
        except Exception as db_error:
            logger.error(f"Ошибка сохранения в БД: {db_error}")
        return {
            "predict": int(prediction)
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=MODEL_API_PORT)
