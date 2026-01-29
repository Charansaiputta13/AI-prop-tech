from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.orchestrator import orchestrator

router = APIRouter()

@router.post("/send", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = await orchestrator.process(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
