
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get("/")
def health_check():
    return {
        "status": "OK",
        "message": "Backend funcionando correctamente"
    }
