from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="API for Employee Promotion Analysis and Prediction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    await connect_to_mongo()
    logger.info("Application started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    await close_mongo_connection()
    logger.info("Application shut down")

@app.get("/")
async def root():
    return {
        "message": "Employee Promotion Analysis API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers
from app.routes import employees, predictions, analytics, auth

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
