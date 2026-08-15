from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    number_of_questions: int = Field(
        ...,
        ge=1,
        le=20
    )


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]