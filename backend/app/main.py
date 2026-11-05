import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load root .env or local .env
load_dotenv()

from app.core.config import settings
from app.core.database import engine, Base
from app.api import (
    auth,
    loans,
    campaigns,
    repayments,
    credit,
    analytics,
    lending_circles,
    business,
    user,
    admin,
    chat,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if not existing
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-performance Python FastAPI backend for EmpowerMSME - supporting Decoupled Next.js Frontend and AI Microservices",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api
api_prefix = settings.API_V1_STR

app.include_router(auth.router, prefix=api_prefix)
app.include_router(loans.router, prefix=api_prefix)
app.include_router(campaigns.router, prefix=api_prefix)
app.include_router(repayments.router, prefix=api_prefix)
app.include_router(credit.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(lending_circles.router, prefix=api_prefix)
app.include_router(business.router, prefix=api_prefix)
app.include_router(user.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(chat.router, prefix=api_prefix)

@app.get("/")
def root():
    return {
        "service": "EmpowerMSME Python FastAPI Backend",
        "status": "online",
        "docs": "/docs",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
