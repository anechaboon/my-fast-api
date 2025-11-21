# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.users import User
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    สร้าง JWT โดยแทรก claim 'exp' เป็น NumericDate (จำนวนเต็ม timestamp วินาที)
    """
    to_encode = data.copy()
    now = datetime.now(tz=timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)

    # RFC ต้องการ NumericDate (UNIX timestamp in seconds)
    to_encode.update({"iat": int(now.timestamp()), "exp": int(expire.timestamp())}) # เพิ่ม claim 'exp' เป็น timestamp

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # สร้าง JWT
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    ถอด JWT และคืน payload หรือ None ถ้าไม่ถูกต้อง/หมดอายุ
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        logger.info("Token expired")
        return None
    except JWTError:
        logger.info("Invalid token")
        return None
    except Exception:
        logger.exception("Unexpected error decoding token")
        return None


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == username))
    user = result.scalar_one_or_none()

    if user and verify_password(password, getattr(user, "hashed_password", None)):
        return user

    return None
