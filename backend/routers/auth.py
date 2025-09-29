from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets
import httpx
from pydantic import BaseModel

from ..database import get_db, User
from ..config import get_settings
from ..security import create_refresh_token, rotate_refresh_token, revoke_refresh_token, create_access_token_claims

router = APIRouter()
settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool

class TokenPair(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    existing_email = await db.execute(select(User).where(User.email == user.email))
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = await db.execute(select(User).where(User.username == user.username))
    if existing_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.post("/token", response_model=TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Disable admin login functionality
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin login has been disabled. Please use alternative authentication method.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    claims = create_access_token_claims(user)
    access_token = create_access_token(claims, expires_delta=access_token_expires)
    refresh = await create_refresh_token(db, user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "refresh_token": refresh.token
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    # Attempt rotation
    new_refresh = await rotate_refresh_token(db, payload.refresh_token)
    if not new_refresh:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    result = await db.execute(select(User).where(User.id == new_refresh.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(create_access_token_claims(user), expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "refresh_token": new_refresh.token
    }

class LogoutRequest(BaseModel):
    refresh_token: str

class NeonAuthRequest(BaseModel):
    """Request model for Neon authentication"""
    project_id: str
    api_key: str
    branch: str = "main"

class NeonAuthResponse(BaseModel):
    """Response model for Neon authentication"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    neon_project_id: str
    neon_branch: str

async def authenticate_with_neon(project_id: str, api_key: str, branch: str = "main") -> dict:
    """Authenticate with Neon database API"""
    neon_api_url = f"https://console.neon.tech/api/v2/projects/{project_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(neon_api_url, headers=headers)
            
            if response.status_code == 200:
                project_data = response.json()
                return {
                    "success": True,
                    "project": project_data,
                    "branch": branch
                }
            else:
                return {
                    "success": False,
                    "error": f"Neon API returned status {response.status_code}",
                    "details": response.text
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to connect to Neon API: {str(e)}"
        }

@router.post("/neon-auth", response_model=NeonAuthResponse)
async def neon_authenticate(auth_data: NeonAuthRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate using Neon database credentials
    This replaces admin login functionality with Neon-based authentication
    """
    settings = get_settings()
    
    # Verify Neon authentication
    neon_result = await authenticate_with_neon(
        auth_data.project_id, 
        auth_data.api_key, 
        auth_data.branch
    )
    
    if not neon_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Neon authentication failed: {neon_result['error']}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create or get user for Neon authentication
    # Using project_id as username for Neon auth
    neon_username = f"neon_{auth_data.project_id}"
    
    result = await db.execute(select(User).where(User.username == neon_username))
    user = result.scalar_one_or_none()
    
    # Create Neon user if doesn't exist
    if not user:
        # Create new Neon-authenticated user with admin role
        hashed_api_key = get_password_hash(auth_data.api_key)
        user = User(
            email=f"{neon_username}@neon.tech",
            username=neon_username,
            hashed_password=hashed_api_key,
            full_name=f"Neon Project {auth_data.project_id}",
            role="admin",  # Grant admin role to Neon-authenticated users
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Generate access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    claims = create_access_token_claims(user)
    claims["neon_project_id"] = auth_data.project_id
    claims["neon_branch"] = auth_data.branch
    claims["auth_method"] = "neon"
    
    access_token = create_access_token(claims, expires_delta=access_token_expires)
    
    return NeonAuthResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
        neon_project_id=auth_data.project_id,
        neon_branch=auth_data.branch
    )

@router.post("/logout")
async def logout(payload: LogoutRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await revoke_refresh_token(db, payload.refresh_token)
    return {"message": "Logged out"}
