import os
from dotenv import load_dotenv


load_dotenv()


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
JWT_ACCESS_TOKEN_SECRET=os.getenv("JWT_ACCESS_TOKEN_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

