from fastapi import APIRouter

from app.schemas.summarise import (
    SummariseRequest,
    SummariseResponse
)
from app.services.ai_service import generate_summary

router = APIRouter()


@router.post("/summarise", response_model=SummariseResponse)
def summarise(request: SummariseRequest):
    summary = generate_summary(
        request.text,
        request.max_bullets
    )

    return {
        "summary": summary
    }