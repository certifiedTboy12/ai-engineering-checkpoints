from fastapi import APIRouter, Depends, Body
from app.core.dependencies import get_current_user_id
from app.services.ai_service import generate_chat_response

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def post_chat_message(
    user_id: str = Depends(get_current_user_id),
    message: str = Body(..., embed=True),
    conversation_topic: str = Body(..., embed=True, alias="topic")
):
    """
    Handles a user's chat message, gets a response from the AI,
    and saves the conversation.
    """
    ai_response = generate_chat_response(message, conversation_topic, user_id)
    return {"answer": ai_response}