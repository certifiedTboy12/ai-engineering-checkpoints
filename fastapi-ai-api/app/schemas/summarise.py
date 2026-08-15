from pydantic import BaseModel, Field


class SummariseRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=10000
    )

    max_bullets: int = Field(
        ...,
        ge=1,
        le=10
    )


class SummariseResponse(BaseModel):
    summary: list[str]