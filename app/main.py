from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import attractions
from app.routers import auth
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Attractions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attractions.router)
app.include_router(auth.router)


UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Serve uploaded files statically from /uploads URL (can be accessed via http://<host>/uploads/...)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")