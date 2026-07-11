# FastAPI
from fastapi import FastAPI

# Database
from database.base import Base
from db import engine

# Routers
from routers import (
    note
)

# Import all Models
import models

# Create tables
Base.metadata.create_all(bind=engine)

# The FastAPI Instance
app = FastAPI(
    title="Mahi Notes API",
    version="1.0.0",
    summary="A simple Backend as our second project to use APIs in ReactJs",
    description="",
    openapi_tags=[
        {"name": "Application", "description": "Application endpoints like root and ping"},
        {"name": "Note", "description": "Note endpoint includes CRUD, Search, Sort, Filter and Pagination"}
    ]
)


@app.get("/", tags=["Application"])
async def root():
    """
    A simple route just to check server is running

    - Endpoint: /
    - Method: GET
    """

    return {"message": "Server is functioning"}


@app.get("/api", tags=["Application"])
async def api():
    """
    Where the whole application begins from

    - Endpoint: /api
    - Method: GET
    """

    return {"message": "Welcome to Mahi Todo List API"}


# Note Router
app.include_router(note.router, prefix="/api")
