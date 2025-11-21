from app.models.user import User
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_user(db: AsyncSession):
    hashed_password = bcrypt.hashpw(b"1234", bcrypt.gensalt()).decode("utf-8")
    users = [
        User(username="Admin", password=hashed_password, email="admin@example.com")
    ]

    for u in users:
        # ตรวจสอบว่ามี user อยู่แล้ว
        result = await db.execute(select(User).filter_by(email=u.email))
        exists = result.scalar_one_or_none()
        if not exists:
            db.add(u)
    
    await db.commit()
