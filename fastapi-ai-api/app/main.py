from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from app.routers import health
from app.routers import chat
from app.exceptions.custom import CustomException
from app.routers import user
from app.routers import auth



app = FastAPI(
    title="AI Learning API",
    version="1.0.0",
    description="FastAPI application providing chat, quiz, and summarisation endpoints."
)

logger = logging.getLogger(__name__)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"Custom exception caught: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "status_code": 500
        }
    )



app.include_router(health.router)
app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)