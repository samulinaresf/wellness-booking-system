from fastapi import FastAPI
from sqlmodel import SQLModel

from db.db import engine

from users.routes import router as users_router
from bookings.routes import router as bookings_router
from admin.routes import router as admin_router


app = FastAPI(
    title="Wellness Booking System",
    description="API para la gestión de usuarios, horarios y reservas.",
    version="1.0.0"
)


# Routers
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(admin_router)


# Crear tablas
SQLModel.metadata.create_all(engine)


# Health check
@app.get("/")
def root():
    return {"message": "FastAPI funcionando"}