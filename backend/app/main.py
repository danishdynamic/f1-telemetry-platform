
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db

from app.routers.sessions import router as sessions_router



# Create the FastAPI application.
app = FastAPI(
    title="F1 Telemetry Analytics API",
    description="Backend API for our Formula 1 data engineering project.",
    version="0.1.0",
)


# Register the sessions endpoints with the main application.
app.include_router(sessions_router)


@app.get("/")
def root():
    # A simple welcome endpoint.
    return {
        "message": "Welcome to the F1 Telemetry Analytics API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Check whether PostgreSQL can execute a simple query.
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError:
        # Return HTTP 503 if the database is unavailable.
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )


@app.get("/api/v1/status")
def project_status(db: Session = Depends(get_db)):
    # Return basic project information and verify the database.
    try:
        db.execute(text("SELECT 1"))

        return {
            "project": "F1 Telemetry Analytics",
            "version": "0.1.0",
            "database": "connected",
            "message": "Backend is ready",
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )
