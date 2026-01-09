from fastapi import APIRouter

router = APIRouter(prefix="/hoteles", tags=["Hoteles"])

@router.get("/")
def listar_hoteles():
    return {"message": "Listado de hoteles"}
