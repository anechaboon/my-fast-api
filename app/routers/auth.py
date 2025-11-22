# /app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

# นำเข้าสิ่งที่จำเป็น
from app.db.database import get_db
from app.models.users import User # สมมติว่ามี Model ชื่อ User
from app.schemas.token import Token # Pydantic Schema สำหรับ Token Response
from app.utils.auth import authenticate_user, create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/api/auth", # กำหนด prefix เป็น /auth
    tags=["Authentication"],
)

# ตั้งค่าเวลาหมดอายุของ Token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.email}, access_token_expires)
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/validate")
async def validate_token(token: str = Cookie(None)):
    from jose import jwt, JWTError
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM = "HS256"
    
    if not token:
        raise HTTPException(status_code=401, detail="No token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"email": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
@router.post("/logout")
async def logout(response: Response):
    return {"status": True, "message": "Logout successful"}
