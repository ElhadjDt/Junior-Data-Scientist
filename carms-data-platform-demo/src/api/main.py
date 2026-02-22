# api/main.py

from fastapi import FastAPI

# Routers
from src.api.routers import (
    disciplines,
    programs,
    schools,
    sites,
    streams,
    qa,
)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="CARMS Residency API",
        version="1.0.0",
        description="Backend API for residency programs and QA system."
    )

    # Register routers
    app.include_router(disciplines.router)
    app.include_router(programs.router)
    app.include_router(schools.router)
    app.include_router(sites.router)
    app.include_router(streams.router)
    app.include_router(qa.router)

    return app


app = create_app()