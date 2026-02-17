from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import chat

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000"), "http://localhost:8000"], # Restrict to frontend and self
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.on_event("startup")
def startup_event():
    from app.core.database import Base, engine
    # Import all models to ensure they are registered
    from app.models import user, property, ticket 
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"status": "ok", "message": f"{settings.PROJECT_NAME} API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
