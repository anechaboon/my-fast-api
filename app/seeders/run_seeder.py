import asyncio

from app.db.database import async_session, engine, Base
from app.seeders.user import seed_user
from app.seeders.attractions import seed_attractions

import logging

logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.ext.asyncio.engine").setLevel(logging.WARNING)

async def run_seeders():
    # สร้างตารางถ้ายังไม่มี (optional)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session() as db:
        await seed_user(db)
        await seed_attractions(db)
        await db.commit()

    print("Seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_seeders())