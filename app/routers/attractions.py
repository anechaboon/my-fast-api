from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.attractions import Attractions
from app.schemas.attractions import AttractionResponse, AttractionListResponse, AttractionCreate, AttractionRead, AttractionUpdate
from app.db.database import get_db, engine, Base
from app.utils.auth import oauth2_scheme, get_current_user
from datetime import datetime, timezone


# สร้าง APIRouter instance
router = APIRouter(
    prefix="/api/attractions",  # กำหนด prefix สำหรับ path ทั้งหมดใน Router นี้
    tags=["Attractions"],   # สำหรับการจัดกลุ่มในเอกสาร OpenAPI/Swagger UI
)

# GET all attractions
@router.get("/", response_model=AttractionListResponse)
async def get_attractions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attractions)
        .where(Attractions.deleted_at == None)
        .order_by(Attractions.created_at.desc()))
    
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
from fastapi import UploadFile, File, Form
import shutil
import os
import uuid

@router.put("/{attraction_id}", response_model=AttractionResponse)
async def update_attraction(
    attraction_id: int,
    name: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    cover_image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme) 
):
    user = await get_current_user(db, token)
    result = await db.execute(
        select(Attractions).where(Attractions.id == attraction_id)
    )
    existing = result.scalar_one_or_none()

    if not existing:
        return {
            "data": None,
            "message": "Attraction not found",
            "status": False,
        }

    existing.name = name
    existing.location = location
    existing.description = description
    existing.updated_by = user.id
    existing.updated_at = datetime.now(timezone.utc)

    if cover_image is not None:
        file_extension = os.path.splitext(cover_image.filename)[1]
        filename = f"{uuid.uuid4().hex}{file_extension}"
        
        upload_dir = "uploads/attractions"
        os.makedirs(upload_dir, exist_ok=True)

        file_location = f"{upload_dir}/{filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)

        # เซ็ต path เก็บใน DB (เช่น /uploads/attractions/xxx.jpg)
        existing.cover_image = file_location

    await db.commit()
    await db.refresh(existing)

    return {
        "data": existing,
        "message": "Attraction updated successfully",
        "status": True,
    }


# DELETE attraction
@router.delete("/{attraction_id}", response_model=AttractionResponse)
async def delete_attraction(
    attraction_id: int, 
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    
    user = await get_current_user(db, token)
    result = await db.execute(
        select(Attractions).where(Attractions.id == attraction_id)
    )
    existing = result.scalar_one_or_none()
    
    existing.deleted_by = user.id
    existing.deleted_at = datetime.now(timezone.utc)
    
    await db.commit()
    await db.refresh(existing)

    return {
        "data": None,
        "message": "Attraction deleted successfully",
        "status": True,
    }
