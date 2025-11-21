from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.attractions import Attractions
from app.schemas.attractions import AttractionResponse, AttractionListResponse, AttractionCreate, AttractionRead, AttractionUpdate
from app.db.database import get_db, engine, Base

# สร้าง APIRouter instance
router = APIRouter(
    prefix="/api/attractions",  # กำหนด prefix สำหรับ path ทั้งหมดใน Router นี้
    tags=["Attractions"],   # สำหรับการจัดกลุ่มในเอกสาร OpenAPI/Swagger UI
)

# GET all attractions
@router.get("/", response_model=AttractionListResponse)
async def get_attractions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attractions))
    data = result.scalars().all()
    if not data:
        return {
            "data": None,
            "message": "No attractions found",
            "status": False,
        }
    return {
        "data": data,
        "message": "Attractions retrieved successfully",
        "status": True,
    }


# GET single attraction by id
@router.get("/{attraction_id}", response_model=AttractionResponse)
async def get_attraction(attraction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attractions).where(Attractions.id == attraction_id))
    data = result.scalar_one_or_none()
    if not data:
        return {
            "data": None,
            "message": "No attractions found",
            "status": False,
        }
    return {
        "data": data,
        "message": "Attractions retrieved successfully",
        "status": True,
    }

# CREATE attraction
@router.post("/", response_model=AttractionResponse)
async def create_attraction(attraction: AttractionCreate, db: AsyncSession = Depends(get_db)):
    new_attraction = Attractions(**attraction.dict())
    db.add(new_attraction)
    await db.commit()
    await db.refresh(new_attraction)
    return {
        "data": new_attraction,
        "message": "Attraction created successfully",
        "status": True,
    }

# UPDATE attraction
@router.put("/{attraction_id}", response_model=AttractionResponse)
async def update_attraction(attraction_id: int, attraction: AttractionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attractions).where(Attractions.id == attraction_id))
    existing = result.scalar_one_or_none()
    if not existing:
        return {
            "data": None,
            "message": "Attraction not found",
            "status": False,
        }
    
    for key, value in attraction.dict(exclude_unset=True).items():
        setattr(existing, key, value)
    
    await db.commit()
    await db.refresh(existing)
    return {
        "data": existing,
        "message": "Attraction updated successfully",
        "status": True,
    }

# DELETE attraction
@router.delete("/{attraction_id}", response_model=AttractionResponse)
async def delete_attraction(attraction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attractions).where(Attractions.id == attraction_id))
    existing = result.scalar_one_or_none()
    if not existing:
        return {
            "data": None,
            "message": "Attraction not found",
            "status": False,
        }
    
    await db.delete(existing)
    await db.commit()
    return {
        "data": None,
        "message": "Attraction deleted successfully",
        "status": True,
    }
