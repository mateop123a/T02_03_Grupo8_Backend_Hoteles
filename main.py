from fastapi import FastAPI
from src.database.database import Base, engine
from src.models import hotel, habitacion

from src.controllers.health_controller import router as health_router
from src.controllers.hotel_controller import router as hotel_router

app = FastAPI(
    title="Backend Hoteles",
    description="API para gestión de hoteles",
    version="1.0.0"
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Registrar routers
app.include_router(health_router)
app.include_router(hotel_router)

@app.get("/")
def root():
    return {"message": "API Hoteles funcionando correctamente"}
