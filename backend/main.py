"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import logging

# Import configuration and logging
from config import settings
from logging_config import setup_logging

# Import database initialization
from database import init_db

# Import routers
from routes import farmer, soil_data, recommendations, soil_health_card

# Setup logging
setup_logging(
    log_level=settings.log_level,
    log_to_file=settings.log_to_file,
    log_file_path=settings.log_file_path
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app with conditional docs
app = FastAPI(
    title="Smart Fertilizer Recommendation System",
    description="IoT-integrated soil analysis and ML-based fertilizer recommendation platform",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    openapi_url="/openapi.json" if not settings.is_production else None,
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration from environment
logger.info(f"Configuring CORS for origins: {settings.allowed_origins_list}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Create directories for file uploads and reports
os.makedirs("uploads", exist_ok=True)
os.makedirs("reports/pdf", exist_ok=True)
os.makedirs("reports/excel", exist_ok=True)

# Mount static files for serving generated reports
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Include routers
app.include_router(farmer.router, prefix="/api", tags=["Farmers"])
app.include_router(soil_data.router, prefix="/api", tags=["Soil Data"])
app.include_router(recommendations.router, prefix="/api", tags=["Recommendations"])
app.include_router(soil_health_card.router, prefix="/api", tags=["Soil Health Card"])


@app.on_event("startup")
async def startup_event():
    """Initialize database and log startup info"""
    logger.info(f"Starting SoilSense API - Environment: {settings.environment}")
    logger.info(f"Database URL: {settings.database_url.split('@')[-1]}")  # Log without password
    logger.info(f"API Documentation: {'Enabled' if not settings.is_production else 'Disabled (Production)'}")
    
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart Fertilizer Recommendation System API",
        "version": "1.0.0",
        "status": "active",
        "environment": settings.environment,
        "docs": "/docs" if not settings.is_production else "disabled"
    }


@app.get("/health")
async def health_check():
    """
    Enhanced health check endpoint
    Validates database connectivity
    """
    from database import SessionLocal
    
    health_status = {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }
    
    # Check database connectivity
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["database"] = "connected"
        logger.debug("Health check: Database OK")
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = f"error: {str(e)}"
        logger.error(f"Health check failed: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Service unhealthy - database connection failed")
    
    return health_status

