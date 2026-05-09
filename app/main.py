from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os

from app.database import Base, engine

from app.routes import (
    auth,
    properties,
    leases,
    payments,
    maintenance,
    dashboard,
    admin
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Property Rental SaaS API",
)

# Serve uploaded images
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(leases.router)
app.include_router(payments.router)
app.include_router(maintenance.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/")
def root():

    return {
        "message": "Property Rental SaaS API Running"
    }