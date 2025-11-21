# /app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

# นำเข้าสิ่งที่จำเป็น
from app.db.database import get_db
from app.models.users import User # สมมติว่ามี Model ชื่อ User
from app.schemas.token import Token # Pydantic Schema สำหรับ Token Response
from app.core.security import authenticate_user, create_access_token

router = APIRouter(
    prefix="/api/auth", # กำหนด prefix เป็น /auth
    tags=["Authentication"],
)

# ตั้งค่าเวลาหมดอายุของ Token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # รับข้อมูลจากฟอร์ม
    db: AsyncSession = Depends(get_db) # รับ session ของฐานข้อมูล
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}