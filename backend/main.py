from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import json
import asyncio
from chatbot_engine import (
    chatbot,
    retrieve_all_threads,
    checkpointer,
    ChatState
)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

app = FastAPI(title="Personal Assistant Chatbot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class Thread(BaseModel):
    thread_id: str
    name: str

class ThreadsResponse(BaseModel):
    threads: List[Thread]

class ConversationResponse(BaseModel):
    messages: List[Message]

class DeleteThreadRequest(BaseModel):
    thread_id: str


@app.get("/")
async def root():
    return {"message": "Personal Assistant Chatbot API"}


@app.get("/threads", response_model=ThreadsResponse)
async def get_threads():
    """Get all conversation threads"""
    try:
        threads_dict = retrieve_all_threads()
        threads = [
            Thread(thread_id=tid, name=name)
            for tid, name in threads_dict.items()
        ]
        return ThreadsResponse(threads=threads)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_stream(message: str, thread_id: str):
    """Generator function for streaming responses"""
    try:
        config = {'configurable': {'thread_id': thread_id}}
        
        # Get current state
        state = chatbot.get_state(config=config)
        messages = state.values.get('messages', []) if state.values else []
        
        # If this is the first message, set the thread name
        if len(messages) == 0:
            # Create a meaningful name from the first message
            preview = message[:50] + "..." if len(message) > 50 else message
            chatbot.update_state(
                config={
                    "configurable": {
                        "thread_id": thread_id,
                        "name": preview
                    },
                    "metadata": {
                        "thread_id": thread_id
                    },
                    "run_name": "chat_turn",
                },
                values={"messages": []}
            )
        
        # Stream the response
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=message)]},
            config=config,
            stream_mode="messages",
        ):
            if isinstance(message_chunk, AIMessage) and message_chunk.content:
                # Send each chunk as JSON
                chunk_data = {
                    "type": "content",
                    "content": message_chunk.content
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                await asyncio.sleep(0.01)  # Small delay for smoother streaming
        
        # Send completion signal
        completion_data = {
            "type": "done",
            "thread_id": thread_id
        }
        yield f"data: {json.dumps(completion_data)}\n\n"
        
    except Exception as e:
        error_data = {
            "type": "error",
            "error": str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Send a message and get a streaming response"""
    return StreamingResponse(
        generate_stream(request.message, request.thread_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get a response (non-streaming fallback)"""
    try:
        config = {'configurable': {'thread_id': request.thread_id}}
        
        # Get current state
        state = chatbot.get_state(config=config)
        messages = state.values.get('messages', []) if state.values else []
        
        # If this is the first message, set the thread name
        if len(messages) == 0:
            preview = request.message[:50] + "..." if len(request.message) > 50 else request.message
            chatbot.update_state(
                config={
                    "configurable": {
                        "thread_id": request.thread_id,
                        "name": preview
                    },
                    "metadata": {
                        "thread_id": request.thread_id
                    },
                    "run_name": "chat_turn",
                },
                values={"messages": []}
            )
        
        # Stream the response
        full_response = ""
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
            stream_mode="messages",
        ):
            if isinstance(message_chunk, AIMessage):
                full_response += message_chunk.content
        
        return ChatResponse(
            response=full_response,
            thread_id=request.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{thread_id}", response_model=ConversationResponse)
async def get_conversation(thread_id: str):
    """Get all messages in a conversation thread"""
    try:
        config = {'configurable': {'thread_id': thread_id}}
        state = chatbot.get_state(config=config)
        messages = state.values.get('messages', []) if state.values else []
        
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_messages.append(Message(role='user', content=msg.content))
            elif isinstance(msg, AIMessage):
                formatted_messages.append(Message(role='assistant', content=msg.content))
        
        return ConversationResponse(messages=formatted_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/thread/new")
async def create_thread():
    """Create a new conversation thread"""
    try:
        thread_id = str(uuid.uuid4())
        return {"thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/thread/{thread_id}")
async def delete_thread(thread_id: str):
    """Delete a conversation thread"""
    try:
        checkpointer.delete_thread(thread_id)
        return {"message": "Thread deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
