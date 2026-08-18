from typing import Any, cast
from app.models.conversations import Conversation
from app.models.messages import Message
from app.exceptions.custom import CustomException
from app.config.dbconfig import SessionLocal
import ollama


def generate_chat_response(new_user_message: str, conversation_topic: str, user_id: str) -> str:

    db = SessionLocal()
    conversation = None
    try:

        print(new_user_message, conversation_topic, user_id)
        # Find an existing conversation for the user and topic, or create a new one
        conversation = db.query(Conversation).filter(
            Conversation.title == conversation_topic,
            Conversation.user_id == user_id
        ).first()

        if not conversation:
            conversation = Conversation(
                title=conversation_topic,
                user_id=user_id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Generate AI response using Ollama
        response = cast(Any, ollama).chat(
            model="llama3.1:8b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational assistant expert in AI, your task is to response to every question in detailed manner"
                },
                {
                    "role": "user",
                    "content": new_user_message
                }
            ]
        )
        ai_response_content = response["message"]["content"]
      

        # Save user and AI messages to the conversation
        db.add(conversation)
        ai_message: Message = Message(
            content=ai_response_content,
            role="assistant",
            conversation_id=conversation.id
        )
        
        user_message: Message = Message(
            content=new_user_message,
            role="user",
            conversation_id=conversation.id
        )
        
        db.add(user_message)
        db.add(ai_message)
        db.commit()
        
        return ai_response_content

    except Exception as e:
        raise CustomException(
            status_code=500,
            detail=str(e)
        )
    finally:
        db.close()

