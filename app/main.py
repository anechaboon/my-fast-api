from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import attractions
from app.routers import auth

app = FastAPI(title="Attractions API")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(attractions.router)
app.include_router(auth.router)