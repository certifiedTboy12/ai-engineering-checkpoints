from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


N8N_AI_ENDPOINT = os.getenv("N8N_URL")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/prompt-ai")
async def prompt_ai():
    url = N8N_AI_ENDPOINT

    if not url:
        raise ValueError

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

            response.raise_for_status()

            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="The external API returned an error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the external API"
        )
