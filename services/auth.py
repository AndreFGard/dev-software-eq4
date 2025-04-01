from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# JWT Configuration
SECRET_KEY = "your-secret-key-keep-it-secret" # In production use proper secret management
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token URL (will be created in main.py)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory storage
users_db = {}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub") or None
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if token_data.username is None:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import auth

from fastapi import APIRouter, Depends, HTTPException, status
router = APIRouter(tags=["authentication"])

@router.post("/register")
async def register(user: auth.UserCreate):
    if auth.get_user(user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    hashed_password = auth.get_password_hash(user.password)
    auth.users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password
    }
    return {"message": "User created successfully"}

from fastapi import Depends, HTTPException, status
@router.post("/token", response_model=auth.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example of protecting an endpoint
@router.get("/protected")
async def protected_route(current_user: auth.UserInDB = Depends(auth.get_current_user)):
    return {"message": f"Hello {current_user.username}"}