from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(
    prefix="/heslth",
    tags=["Health"]
)


@router.get("/")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }