from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AttractionListResponse(BaseModel):
    data: List[AttractionRead]
    message: str
    status: bool

class AttractionResponse(BaseModel):
    data: Optional[AttractionRead]
    message: str
    status: bool

class AttractionBase(BaseModel):
    name: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = True

class AttractionCreate(AttractionBase):
    pass

class AttractionUpdate(AttractionBase):
    pass

class AttractionRead(AttractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
