import sqlite3
import os
from config import DATABASE_PATH

def init_database():
    db_path = DATABASE_PATH
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("🔄 Creating database tables...")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        age INTEGER,
        height INTEGER,
        weight INTEGER,
        gender INTEGER,
        angina INTEGER,
        stroke INTEGER,
        health_status INTEGER,
        cholesterol INTEGER,
        cigarettes INTEGER,
        marital_status INTEGER,
        employment INTEGER,
        copd INTEGER,
        personal_doctor INTEGER,
        depression INTEGER,
        walking_difficulty INTEGER,
        last_checkup INTEGER,
        hypertension INTEGER,
        diabetes INTEGER,
        model_prediction INTEGER
    )   
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database successfully created at: {db_path}")

init_database()