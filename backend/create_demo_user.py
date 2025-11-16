"""
Quick script to create test user in MongoDB
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import hashlib
import base64

async def create_test_user():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['employee_promotion_db']
    
    # Check if user exists
    existing = await db.users.find_one({"email": "demo@example.com"})
    if existing:
        print("Demo user already exists")
        client.close()
        return
    
    # Create simple password hash (demo only)
    password = "demo123"
    # Use a simple hash for demo
    hashed = base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()
    
    # Create demo user
    demo_user = {
        "email": "demo@example.com",
        "hashed_password": f"$2b$12$abcdefghijklmnopqrstuvwxyz123456789012", # Mock bcrypt hash
        "full_name": "Demo User",
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.users.insert_one(demo_user)
    print(f"✓ Demo user created: {result.inserted_id}")
    print(f"  Email: demo@example.com")
    print(f"  Password: demo123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_user())
