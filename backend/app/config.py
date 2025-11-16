from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "employee_promotion_db"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Configuration
    APP_NAME: str = "Employee Promotion Analysis API"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Model Configuration
    MODEL_PATH: str = "./models/random_forest_model.joblib"
    SCALER_PATH: str = "./models/scaler.joblib"
    
    # Business Metrics
    AVG_COST_PER_HIRING: float = 4425.0
    HIRING_TARGET_PERCENTAGE: float = 0.02
    TOTAL_NUM_EMPLOYEES: int = 54808
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
