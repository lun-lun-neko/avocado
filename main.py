from fastapi import FastAPI, Request
from app.routes import chat
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": ",,"}



"""
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "너는 친절한 도우미야."},
        {"role": "user", "content": "파이썬에서 GPT API 쓰는 방법 알려줘!"}
    ]
)

print(response.choices[0].message.content)
"""