from fastapi import FastAPI

from app.routers import health
from app.routers import chat
from app.routers import quiz
from app.routers import summarise


app = FastAPI(
    title="AI Learning API",
    version="1.0.0",
    description="FastAPI application providing chat, quiz, and summarisation endpoints."
)


app.include_router(health.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(summarise.router)