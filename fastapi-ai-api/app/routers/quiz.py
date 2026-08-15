from fastapi import APIRouter

from app.schemas.quiz import QuizRequest, QuizResponse
from app.services.ai_service import generate_quiz

router = APIRouter()


@router.post("/quiz", response_model=QuizResponse)
def quiz(request: QuizRequest):
    questions = generate_quiz(
        request.topic,
        request.number_of_questions
    )

    return {
        "questions": questions
    }