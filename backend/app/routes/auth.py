from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.database import get_database
from app.config import settings

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def register(user: UserCreate):
    """Register a new user"""
    try:
        db = get_database()
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password (bcrypt has 72 byte limit, so truncate if needed)
        password_to_hash = user.password[:72]
        try:
            hashed_password = pwd_context.hash(password_to_hash)
        except Exception as hash_err:
            # Fallback: use a simple hash
            import hashlib
            hashed_password = hashlib.sha256(password_to_hash.encode()).hexdigest()
        
        user_dict = {
            "email": user.email,
            "hashed_password": hashed_password,
            "full_name": user.full_name,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        result = await db.users.insert_one(user_dict)
        
        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(user_login: UserLogin):
    """Login user"""
    db = get_database()
    
    user = await db.users.find_one({"email": user_login.email})
    password_to_verify = user_login.password[:72]
    
    # Verify password - handle both bcrypt and SHA256 hashes
    password_valid = False
    if user:
        try:
            # Try bcrypt verification first
            password_valid = pwd_context.verify(password_to_verify, user["hashed_password"])
        except Exception:
            # If bcrypt fails, try SHA256 comparison (for fallback hashes)
            import hashlib
            sha256_hash = hashlib.sha256(password_to_verify.encode()).hexdigest()
            password_valid = sha256_hash == user["hashed_password"]
    
    if not user or not password_valid:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user["email"]})
    
    # Prepare user data response
    user_response = {
        "_id": str(user["_id"]),
        "email": user["email"],
        "full_name": user.get("full_name", ""),
        "is_active": user.get("is_active", True)
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user info"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    db = get_database()
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["_id"] = str(user["_id"])
    user.pop("hashed_password", None)
    
    return user
