from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.db = db.client[settings.DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    try:
        if db.client:
            db.client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Employees collection indexes
        await db.db.employees.create_index([("employee_id", ASCENDING)], unique=True)
        await db.db.employees.create_index([("department", ASCENDING)])
        await db.db.employees.create_index([("region", ASCENDING)])
        await db.db.employees.create_index([("is_promoted", ASCENDING)])
        
        # Predictions collection indexes
        await db.db.predictions.create_index([("employee_id", ASCENDING)])
        await db.db.predictions.create_index([("prediction_date", DESCENDING)])
        await db.db.predictions.create_index([("predicted_promotion", ASCENDING)])
        
        # Users collection indexes
        await db.db.users.create_index([("email", ASCENDING)], unique=True)
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")


def get_database():
    """Get database instance"""
    return db.db
