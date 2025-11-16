"""
Load CSV data into MongoDB
"""
import pandas as pd
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import sys

async def load_data():
    """Load train.csv data into MongoDB"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    employees_collection = db.employees
    
    # Clear existing data
    print("Clearing existing employee data...")
    await employees_collection.delete_many({})
    
    # Load CSV
    print("Loading train.csv...")
    df = pd.read_csv('../train.csv')
    
    # Convert DataFrame to list of dictionaries
    employees = df.to_dict('records')
    
    # Clean up data - convert numpy types to Python types
    for emp in employees:
        for key, value in emp.items():
            if pd.isna(value):
                emp[key] = None
            elif isinstance(value, (pd.Int64Dtype, int)):
                emp[key] = int(value) if not pd.isna(value) else None
            elif isinstance(value, (pd.Float64Dtype, float)):
                emp[key] = float(value) if not pd.isna(value) else None
    
    # Insert into MongoDB
    print(f"Inserting {len(employees)} employee records...")
    if employees:
        result = await employees_collection.insert_many(employees)
        print(f"Successfully inserted {len(result.inserted_ids)} records")
    
    # Create indexes
    print("Creating indexes...")
    await employees_collection.create_index("employee_id", unique=True)
    await employees_collection.create_index("department")
    await employees_collection.create_index("is_promoted")
    
    # Print summary
    total = await employees_collection.count_documents({})
    promoted = await employees_collection.count_documents({"is_promoted": 1})
    promotion_rate = (promoted / total * 100) if total > 0 else 0
    
    print("\n=== Data Load Summary ===")
    print(f"Total Employees: {total}")
    print(f"Promoted: {promoted}")
    print(f"Not Promoted: {total - promoted}")
    print(f"Promotion Rate: {promotion_rate:.2f}%")
    
    # Close connection
    client.close()
    print("\nData load complete!")

if __name__ == "__main__":
    try:
        asyncio.run(load_data())
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
