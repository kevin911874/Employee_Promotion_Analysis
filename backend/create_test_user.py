import asyncio
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_demo_user():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["employee_promotion_db"]
    
    # Demo credentials
    email = "demo@example.com"
    password = "demo123"
    full_name = "Demo User"
    
    try:
        # Check if user exists
        existing = await db.users.find_one({"email": email})
        if existing:
            print(f"✓ Demo user already exists: {email}")
            return
        
        # Hash password
        password_to_hash = password[:72]
        try:
            hashed_password = pwd_context.hash(password_to_hash)
        except:
            hashed_password = hashlib.sha256(password_to_hash.encode()).hexdigest()
        
        # Create user document
        user_doc = {
            "email": email,
            "hashed_password": hashed_password,
            "full_name": full_name,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_doc)
        print("=" * 50)
        print("✓ Demo user created successfully!")
        print("=" * 50)
        print(f"Email:    {email}")
        print(f"Password: {password}")
        print(f"User ID:  {result.inserted_id}")
        print("=" * 50)
        
    finally:
        client.close()

asyncio.run(create_demo_user())
