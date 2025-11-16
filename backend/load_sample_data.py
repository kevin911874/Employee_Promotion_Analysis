"""
Script to load sample employee data into MongoDB
"""
import asyncio
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import sys

async def load_data():
    """Load sample data from train.csv"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        db = client['employee_promotion_db']
        
        print("Loading sample data from train.csv...")
        
        # Read CSV
        df = pd.read_csv('train.csv')
        
        # Take only first 1000 rows for quick demo
        df = df.head(1000)
        
        print(f"Processing {len(df)} employees...")
        
        # Convert dataframe to list of dicts
        employees = df.to_dict('records')
        
        # Clean up data - remove rows with all NaN
        employees = [emp for emp in employees if not all(pd.isna(v) for v in emp.values())]
        
        # Insert into database
        if employees:
            result = await db.employees.insert_many(employees)
            print(f"✓ Successfully loaded {len(result.inserted_ids)} employees")
            
            # Show stats
            count = await db.employees.count_documents({})
            promoted_count = await db.employees.count_documents({"is_promoted": 1})
            
            print(f"\nDatabase Stats:")
            print(f"  Total employees: {count}")
            print(f"  Promoted: {promoted_count}")
            print(f"  Promotion rate: {(promoted_count/count*100):.2f}%")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

async def clear_data():
    """Clear existing employee data"""
    try:
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        db = client['employee_promotion_db']
        
        result = await db.employees.delete_many({})
        print(f"Cleared {result.deleted_count} employees from database")
        
        client.close()
        return True
    except Exception as e:
        print(f"Error clearing data: {e}")
        return False

if __name__ == "__main__":
    import os
    os.chdir('d:\\Project\\Employee Promotion Analysis')
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        print("Clearing employee data...")
        asyncio.run(clear_data())
    else:
        print("Starting data load...")
        success = asyncio.run(load_data())
        sys.exit(0 if success else 1)
