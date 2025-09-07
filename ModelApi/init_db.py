import sqlite3
import os

def init_database():
    if os.path.exists('logger.db'):
        os.remove('logger.db')
        
    conn = sqlite3.connect('logger.db')
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
    
    print("✅ Database successfully created at")

init_database()