from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.orchestrator import orchestrator

router = APIRouter()

@router.post("/send", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        response = await orchestrator.process(request, db)
        return response
    except Exception as e:
        # Log the full error
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
