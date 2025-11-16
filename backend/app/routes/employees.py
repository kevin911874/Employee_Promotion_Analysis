from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=dict)
async def create_employee(employee: EmployeeCreate):
    """Create a new employee"""
    db = get_database()
    
    # Check if employee_id already exists
    existing = await db.employees.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    employee_dict = employee.dict()
    employee_dict["created_at"] = datetime.utcnow()
    employee_dict["updated_at"] = datetime.utcnow()
    
    result = await db.employees.insert_one(employee_dict)
    
    return {"id": str(result.inserted_id), "employee_id": employee.employee_id}

@router.get("/", response_model=List[dict])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = None,
    region: Optional[str] = None,
    is_promoted: Optional[int] = None
):
    """Get all employees with filters"""
    db = get_database()
    
    query = {}
    if department:
        query["department"] = department
    if region:
        query["region"] = region
    if is_promoted is not None:
        query["is_promoted"] = is_promoted
    
    cursor = db.employees.find(query).skip(skip).limit(limit)
    employees = await cursor.to_list(length=limit)
    
    for emp in employees:
        emp["_id"] = str(emp["_id"])
    
    return employees

@router.get("/{employee_id}", response_model=dict)
async def get_employee(employee_id: int):
    """Get employee by ID"""
    db = get_database()
    employee = await db.employees.find_one({"employee_id": employee_id})
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee["_id"] = str(employee["_id"])
    return employee

@router.put("/{employee_id}", response_model=dict)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate):
    """Update employee information"""
    db = get_database()
    
    update_data = {k: v for k, v in employee_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.employees.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {"message": "Employee updated successfully"}

@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """Delete an employee"""
    db = get_database()
    
    result = await db.employees.delete_one({"employee_id": employee_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {"message": "Employee deleted successfully"}

@router.post("/bulk-upload")
async def bulk_upload_employees(employees: List[EmployeeCreate]):
    """Bulk upload employees"""
    db = get_database()
    
    employees_data = []
    for emp in employees:
        emp_dict = emp.dict()
        emp_dict["created_at"] = datetime.utcnow()
        emp_dict["updated_at"] = datetime.utcnow()
        employees_data.append(emp_dict)
    
    result = await db.employees.insert_many(employees_data, ordered=False)
    
    return {
        "message": f"Successfully uploaded {len(result.inserted_ids)} employees",
        "count": len(result.inserted_ids)
    }

@router.get("/stats/summary")
async def get_employee_summary():
    """Get employee statistics summary"""
    db = get_database()
    
    total_employees = await db.employees.count_documents({})
    promoted = await db.employees.count_documents({"is_promoted": 1})
    
    pipeline = [
        {"$group": {
            "_id": "$department",
            "count": {"$sum": 1}
        }}
    ]
    dept_stats = await db.employees.aggregate(pipeline).to_list(length=100)
    
    return {
        "total_employees": total_employees,
        "promoted_count": promoted,
        "promotion_rate": round(promoted / total_employees * 100, 2) if total_employees > 0 else 0,
        "by_department": dept_stats
    }
