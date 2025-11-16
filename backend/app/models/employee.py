from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    employee_id: int = Field(..., description="Unique ID for employee")
    department: str = Field(..., description="Department of employee")
    region: str = Field(..., description="Region of employment")
    education: str = Field(..., description="Education Level")
    gender: str = Field(..., description="Gender of Employee")
    recruitment_channel: str = Field(..., description="Channel of recruitment")
    no_of_trainings: int = Field(..., description="No of trainings completed in previous year")
    age: int = Field(..., ge=18, le=100, description="Age of Employee")
    previous_year_rating: Optional[float] = Field(None, ge=1, le=5, description="Employee Rating for previous year")
    length_of_service: int = Field(..., ge=0, description="Length of service in years")
    awards_won: int = Field(..., ge=0, le=1, description="If awards won during previous year")
    avg_training_score: float = Field(..., ge=0, le=100, description="Average score in current training evaluations")
    is_promoted: int = Field(..., ge=0, le=1, description="Promoted or not")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    department: Optional[str] = None
    region: Optional[str] = None
    education: Optional[str] = None
    gender: Optional[str] = None
    recruitment_channel: Optional[str] = None
    no_of_trainings: Optional[int] = None
    age: Optional[int] = None
    previous_year_rating: Optional[float] = None
    length_of_service: Optional[int] = None
    awards_won: Optional[int] = None
    avg_training_score: Optional[float] = None
    is_promoted: Optional[int] = None


class EmployeeInDB(EmployeeBase):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "employee_id": 65438,
                "department": "Sales & Marketing",
                "region": "region_7",
                "education": "Master's & above",
                "gender": "f",
                "recruitment_channel": "sourcing",
                "no_of_trainings": 1,
                "age": 35,
                "previous_year_rating": 5.0,
                "length_of_service": 8,
                "awards_won": 0,
                "avg_training_score": 49,
                "is_promoted": 0
            }
        }


class EmployeeResponse(EmployeeInDB):
    pass
