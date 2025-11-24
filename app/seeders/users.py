from app.models.users import User
import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.auth import get_password_hash

async def seed_user(db: AsyncSession):
    hashed_password = get_password_hash("65066506")
    users = [
        User(username="Admin", hashed_password=hashed_password, email="admin@example.com")
    ]

    for u in users:
        result = await db.execute(select(User).filter_by(email=u.email))
        exists = result.scalar_one_or_none()
        if not exists:
            db.add(u)
    
    await db.commit()
