from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    message: str
    user_id: str
    history: Optional[List[Message]] = []
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    agent_used: str
    data: Optional[Dict[str, Any]] = None
