from fastapi import FastAPI
from src.database.database import Base, engine
from src.models import hotel, habitacion

app = FastAPI(
    title="Backend Hoteles",
    description="API para gestión de hoteles",
    version="1.0.0"
)

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API Hoteles funcionando correctamente"}
