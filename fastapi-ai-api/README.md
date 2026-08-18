--- a/README.md
+++ b/README.md
@@ -1 +1,146 @@
-# FastAPI AI Agent API with Ollama

- -This project is a backend API for an AI-powered agent, built with Python and FastAPI. It includes user registration and authentication, conversation and message storage, and integration with Ollama to provide responses from various large language models.
- -The application uses PostgreSQL as its database and SQLAlchemy as the ORM for all database operations.
- -## Features
- -- **User Management**: Secure user registration and JWT-based authentication.
  -- **Conversation History**: Stores and retrieves user conversations and individual messages.
  -- **AI Integration**: Connects to Ollama to stream responses from a selected AI model.
  -- **Async Support**: Fully asynchronous API endpoints for high performance.
  -- **ORM Integration**: Uses SQLAlchemy 2.0 for asynchronous database operations with PostgreSQL.
  -- **Dependency Management**: Uses Pydantic for data validation and settings management.
- -## Tech Stack
- -- **Backend**: FastAPI, Python 3.10+
  -- **Database**: PostgreSQL
  -- **ORM**: SQLAlchemy (with `asyncpg`)
  -- **AI Model Serving**: Ollama
  -- **Authentication**: JWT (JSON Web Tokens)
  -- **Data Validation**: Pydantic
- -## Prerequisites
- -Before you begin, ensure you have the following installed:
- -- Python 3.10 or higher
  -- PostgreSQL server
  -- Ollama (with a downloaded model, e.g., `ollama pull llama3`)
  -- `pip` for package management
- -## Installation
- -1. **Clone the repository:**
- ```bash

  ```
- git clone <your-repository-url>
- cd fastapi-ai-api
- ```

  ```
- -2. **Create and activate a virtual environment:**
- ```bash

  ```
- python -m venv venv
- source venv/bin/activate # On Windows use `venv\Scripts\activate`
- ```

  ```
- -3. **Install dependencies:**
- ```bash

  ```
- pip install -r requirements.txt
- ```

  ```
- _(You will need to create a `requirements.txt` file with packages like `fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `asyncpg`, `pydantic`, `python-jose[cryptography]`, `passlib[bcrypt]`, `ollama`)_
- -4. **Configure Environment Variables:**
- Create a `.env` file in the root directory and add the following variables.
-
- ```env

  ```
- DATABASE_URL="postgresql+asyncpg://user:password@host:port/database_name"
- SECRET_KEY="your_super_secret_key"
- ALGORITHM="HS256"
- ACCESS_TOKEN_EXPIRE_MINUTES=30
- OLLAMA_HOST="http://localhost:11434"
- ```

  ```
- -5. **Set up the database:**
- You may need to run a script to create the database tables based on your SQLAlchemy models. If you are using a migration tool like Alembic, you would run its migration commands.
-
- ```bash

  ```
- # Example if you have a script to create tables
- # python -m app.database.init_db
- ```

  ```
- -## Running the Application
- -Once the setup is complete, you can run the FastAPI application using Uvicorn.
- -`bash
-uvicorn app.main:app --reload
-`
- -The API will be available at `http://127.0.0.1:8000`.
- -## API Implementation
- -Here are some examples of how the API endpoints might be implemented.
- -### User Authentication
- -The API provides endpoints for user registration and login.
- -#### Register a new user
- -```python
  -# in app/routers/auth.py
- -from fastapi import APIRouter, Depends, HTTPException
  -from sqlalchemy.ext.asyncio import AsyncSession
  -from app.database import get_db
  -from app.schemas import UserCreate, User
  -from app.crud import user as crud_user
- -router = APIRouter()
- -@router.post("/register", response_model=User)
  -async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
- db_user = await crud_user.get_user_by_email(db, email=user_in.email)
- if db_user:
-        raise HTTPException(status_code=400, detail="Email already registered")
- return await crud_user.create_user(db=db, user=user_in)
  -```
- -### Conversations and Messages
- -Endpoints to manage conversations and interact with the Ollama AI.
- -#### Create a new conversation
- -```python
  -# in app/routers/conversations.py
- -@router.post("/", response_model=Conversation)
  -async def create_conversation(
- conversation_in: ConversationCreate,
- db: AsyncSession = Depends(get_db),
- current_user: User = Depends(get_current_active_user)
  -):
- return await crud_conversation.create_user_conversation(
-        db=db, conversation=conversation_in, user_id=current_user.id
- )
  -```
- -#### Add a message and get AI response
- -This endpoint receives a user's message, stores it, sends it to Ollama, and streams the response back.
- -```python
  -# in app/routers/conversations.py
- -import ollama
  -from fastapi.responses import StreamingResponse
- -@router.post("/{conversation_id}/messages", response_model=Message)
  -async def create_message_and_get_response(
- conversation_id: int,
- message_in: MessageCreate,
- db: AsyncSession = Depends(get_db),
- current_user: User = Depends(get_current_active_user)
  -):
- # 1. Store the user's message
- await crud_message.create_message(db=db, message=message_in, conversation_id=conversation_id)
-
- # 2. Get conversation history
- history = await crud_message.get_messages_by_conversation(db, conversation_id=conversation_id)
-
- # 3. Format for Ollama and get response
- ollama_messages = [{"role": msg.role, "content": msg.content} for msg in history]
-
- async def response_generator():
-        ai_response_content = ""
-        stream = ollama.chat(
-            model='llama3',
-            messages=ollama_messages,
-            stream=True,
-        )
-        for chunk in stream:
-            content_chunk = chunk['message']['content']
-            ai_response_content += content_chunk
-            yield content_chunk
-
-        # 4. Store AI's response
-        ai_message = MessageCreate(role="assistant", content=ai_response_content)
-        await crud_message.create_message(db=db, message=ai_message, conversation_id=conversation_id)
-
- return StreamingResponse(response_generator(), media_type="text/plain")
  -```
- -## Project Structure
- -Here is a recommended project structure for your FastAPI application:
- -`
-fastapi-ai-api/
-├── app/
-│   ├── __init__.py
-│   ├── main.py           # FastAPI app instance and main routes
-│   ├── crud/             # Database Create, Read, Update, Delete operations
-│   │   ├── __init__.py
-│   │   ├── base.py
-│   │   ├── user.py
-│   │   └── conversation.py
-│   ├── database/         # Database session and model definitions
-│   │   ├── __init__.py
-│   │   ├── base.py
-│   │   └── session.py
-│   ├── models/           # SQLAlchemy models
-│   │   ├── __init__.py
-│   │   ├── user.py
-│   │   └── conversation.py
-│   ├── routers/          # API endpoint routers
-│   │   ├── __init__.py
-│   │   ├── auth.py
-│   │   └── conversations.py
-│   ├── schemas/          # Pydantic schemas for data validation
-│   │   ├── __init__.py
-│   │   ├── user.py
-│   │   └── conversation.py
-│   └── core/             # Application configuration and security
-│       ├── __init__.py
-│       ├── config.py
-│       └── security.py
-├── tests/                # Application tests
-├── .env                  # Environment variables
-├── requirements.txt      # Project dependencies
-└── README.md             # This file
-`
  +This project is a backend API for an AI-powered agent, built with Python and FastAPI. It includes user registration and authentication, conversation and message storage, and integration with Ollama to provide responses from various large language models.

* +The application uses PostgreSQL as its database and SQLAlchemy as the ORM for all database operations.
* +## Features
* +- **User Management**: Secure user registration and JWT-based authentication.
  +- **Conversation History**: Stores and retrieves user conversations and individual messages.
  +- **AI Integration**: Connects to Ollama to stream responses from a selected AI model.
  +- **Async Support**: Fully asynchronous API endpoints for high performance.
  +- **ORM Integration**: Uses SQLAlchemy 2.0 for asynchronous database operations with PostgreSQL.
  +- **Dependency Management**: Uses Pydantic for data validation and settings management.
* +## Tech Stack
* +- **Backend**: FastAPI, Python 3.10+
  +- **Database**: PostgreSQL
  +- **ORM**: SQLAlchemy (with `asyncpg`)
  +- **AI Model Serving**: Ollama
  +- **Authentication**: JWT (JSON Web Tokens)
  +- **Data Validation**: Pydantic
* +## Prerequisites
* +Before you begin, ensure you have the following installed:
* +- Python 3.10 or higher
  +- PostgreSQL server
  +- Ollama (with a downloaded model, e.g., `ollama pull llama3`)
  +- `pip` for package management
* +## Installation
* +1. **Clone the repository:**
* ```bash

  ```
* git clone <your-repository-url>
* cd fastapi-ai-api
* ```

  ```
* +2. **Create and activate a virtual environment:**
* ```bash

  ```
* python -m venv venv
* source venv/bin/activate # On Windows use `venv\Scripts\activate`
* ```

  ```
* +3. **Install dependencies:**
* ```bash

  ```
* pip install -r requirements.txt
* ```

  ```
* _(You will need to create a `requirements.txt` file with packages like `fastapi`, `uvicorn`, `sqlalchemy[asyncio]`, `asyncpg`, `pydantic`, `python-jose[cryptography]`, `passlib[bcrypt]`, `ollama`)_
* +4. **Configure Environment Variables:**
* Create a `.env` file in the root directory and add the following variables.
*
* ```env

  ```
* DATABASE_URL="postgresql+asyncpg://user:password@host:port/database_name"
* SECRET_KEY="your_super_secret_key"
* ALGORITHM="HS256"
* ACCESS_TOKEN_EXPIRE_MINUTES=30
* OLLAMA_HOST="http://localhost:11434"
* ```

  ```
* +5. **Set up the database:**
* You may need to run a script to create the database tables based on your SQLAlchemy models. If you are using a migration tool like Alembic, you would run its migration commands.
*
* ```bash

  ```
* # Example if you have a script to create tables
* # python -m app.database.init_db
* ```

  ```
* +## Running the Application
* +Once the setup is complete, you can run the FastAPI application using Uvicorn.
* +`bash
+uvicorn app.main:app --reload
+`
* +The API will be available at `http://12.0.0.1:8000`.
* +## API Implementation
* +Here are some examples of how the API endpoints might be implemented.
* +### User Authentication
* +The API provides endpoints for user registration and login.
* +#### Register a new user
* +```python
  +# in app/routers/auth.py
* +from fastapi import APIRouter, Depends, HTTPException
  +from sqlalchemy.ext.asyncio import AsyncSession
  +from app.database import get_db
  +from app.schemas import UserCreate, User
  +from app.crud import user as crud_user
* +router = APIRouter()
* +@router.post("/register", response_model=User)
  +async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
* db_user = await crud_user.get_user_by_email(db, email=user_in.email)
* if db_user:
*        raise HTTPException(status_code=400, detail="Email already registered")
* return await crud_user.create_user(db=db, user=user_in)
  +```
* +### Conversations and Messages
* +Endpoints to manage conversations and interact with the Ollama AI.
* +#### Create a new conversation
* +```python
  +# in app/routers/conversations.py
* +@router.post("/", response_model=Conversation)
  +async def create_conversation(
* conversation_in: ConversationCreate,
* db: AsyncSession = Depends(get_db),
* current_user: User = Depends(get_current_active_user)
  +):
* return await crud_conversation.create_user_conversation(
*        db=db, conversation=conversation_in, user_id=current_user.id
* )
  +```
* +#### Add a message and get AI response
* +This endpoint receives a user's message, stores it, sends it to Ollama, and streams the response back.
* +```python
  +# in app/routers/conversations.py
* +import ollama
  +from fastapi.responses import StreamingResponse
* +@router.post("/{conversation_id}/messages", response_model=Message)
  +async def create_message_and_get_response(
* conversation_id: int,
* message_in: MessageCreate,
* db: AsyncSession = Depends(get_db),
* current_user: User = Depends(get_current_active_user)
  +):
* # 1. Store the user's message
* await crud_message.create_message(db=db, message=message_in, conversation_id=conversation_id)
*
* # 2. Get conversation history
* history = await crud_message.get_messages_by_conversation(db, conversation_id=conversation_id)
*
* # 3. Format for Ollama and get response
* ollama_messages = [{"role": msg.role, "content": msg.content} for msg in history]
*
* async def response_generator():
*        ai_response_content = ""
*        stream = ollama.chat(
*            model='llama3',
*            messages=ollama_messages,
*            stream=True,
*        )
*        for chunk in stream:
*            content_chunk = chunk['message']['content']
*            ai_response_content += content_chunk
*            yield content_chunk
*
*        # 4. Store AI's response
*        ai_message = MessageCreate(role="assistant", content=ai_response_content)
*        await crud_message.create_message(db=db, message=ai_message, conversation_id=conversation_id)
*
* return StreamingResponse(response_generator(), media_type="text/plain")
  +```
* +## Project Structure
* +Here is a recommended project structure for your FastAPI application:
* +`
+fastapi-ai-api/
+├── app/
+│   ├── __init__.py
+│   ├── main.py           # FastAPI app instance and main routes
+│   ├── crud/             # Database Create, Read, Update, Delete operations
+│   │   ├── __init__.py
+│   │   ├── base.py
+│   │   ├── user.py
+│   │   └── conversation.py
+│   ├── database/         # Database session and model definitions
+│   │   ├── __init__.py
+│   │   ├── base.py
+│   │   └── session.py
+│   ├── models/           # SQLAlchemy models
+│   │   ├── __init__.py
+│   │   ├── user.py
+│   │   └── conversation.py
+│   ├── routers/          # API endpoint routers
+│   │   ├── __init__.py
+│   │   ├── auth.py
+│   │   └── conversations.py
+│   ├── schemas/          # Pydantic schemas for data validation
+│   │   ├── __init__.py
+│   │   ├── user.py
+│   │   └── conversation.py
+│   └── core/             # Application configuration and security
+│       ├── __init__.py
+│       ├── config.py
+│       └── security.py
+├── tests/                # Application tests
+├── .env                  # Environment variables
+├── requirements.txt      # Project dependencies
+└── README.md             # This file
+`
