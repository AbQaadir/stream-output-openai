import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
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


async def generate_response(topic: str):
    model = ChatOpenAI(model="gpt-4o-mini")
    async for event in model.astream_events(input=topic, version="v2"):
        if event["event"] == "on_chat_model_stream":
            chunk_content = event["data"]["chunk"].content
            yield chunk_content.encode()

@app.get("/stream/{topic}")
async def stream_endpoint(topic: str):
    return StreamingResponse(
        generate_response(topic),
        media_type="text/plain"
    )

# Basic health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI streaming server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)