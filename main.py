import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import asyncio

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    topic: str

async def generate_response(topic: str):
    model = ChatOpenAI(model="gpt-4o-mini")
    async for event in model.astream_events(input=topic, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk_content = event["data"]["chunk"].content
            yield chunk_content.encode()

@app.post("/stream")
async def stream_endpoint(request: QueryRequest):
    return StreamingResponse(
        generate_response(request.topic),
        media_type="text/plain"
    )

# Basic health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI streaming server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
