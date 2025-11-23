from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import attractions
from app.routers import auth
from fastapi.staticfiles import StaticFiles

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

# Serve uploaded files statically from /uploads URL (can be accessed via http://<host>/uploads/...)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
