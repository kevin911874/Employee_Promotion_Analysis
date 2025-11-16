"""
Script to fix MongoDB indexes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_indexes():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['employee_promotion_db']
    
    print("Fixing MongoDB indexes...")
    
    try:
        # Drop the users collection to remove old indexes
        await db.users.drop()
        print("✓ Dropped old users collection")
    except Exception as e:
        print(f"Note: {e}")
    
    # Recreate with proper indexes
    await db.users.create_index("email", unique=True)
    print("✓ Created email unique index")
    
    print("✓ Database indexes fixed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_indexes())
