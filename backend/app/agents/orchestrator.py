from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.maintenance import MaintenanceAgent
from app.agents.leasing import LeasingAgent
from app.models.ticket import Ticket
from app.models.user import User
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
import os

class OrchestratorAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
        else:
            self.llm = None
            
        self.maintenance_agent = MaintenanceAgent()
        self.leasing_agent = LeasingAgent()

    async def process(self, request: ChatRequest, db: Session) -> ChatResponse:
        user_msg = request.message
        history = request.history or []
        
        # Resolve User (Simple logic for demo)
        # In a real app, we would get user_id from the auth token (Depends(get_current_user))
        user_id = self._get_or_create_demo_user(db)

        # 1. Determine Intent
        intent = self._determine_intent(user_msg, history)
        
        if intent == "maintenance":
             return await self.handle_maintenance(user_msg, history, db, user_id)
        elif intent == "leasing":
             return await self.handle_leasing(user_msg, history)
        
        # 2. Default: General Chat
        return await self.general_chat(request)

    def _get_or_create_demo_user(self, db: Session) -> int:
        """Helper to ensure we have a user to attach tickets to."""
        email = "demo@example.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email, 
                full_name="Demo User", 
                hashed_password="hashed_secret", # Placeholder
                role="tenant"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user.id

    def _determine_intent(self, user_msg: str, history: list) -> str:
        """
        Determine the user's intent based on keywords and context.
        Returns: 'maintenance', 'leasing', or 'general'
        """
        msg_lower = user_msg.lower()
        
        # 1. Maintenance Keywords
        maint_keywords = ["fix", "leak", "broken", "repair", "maintenance", "not working", "hot water", "light", "power"]
        if any(k in msg_lower for k in maint_keywords):
            return "maintenance"

        # 2. Leasing Keywords
        leasing_keywords = ["rent", "lease", "apartment", "unit", "bedroom", "tour", "price", "cost", "available", "move in"]
        if any(k in msg_lower for k in leasing_keywords):
            return "leasing"
            
        # 3. Contextual check (last agent used)
        if history and history[-1].role == "assistant":
            # Heuristic: if last message asked about priority or description, we are likely in flow
            last_content = history[-1].content.lower()
            if "priority" in last_content or "ticket" in last_content:
                return "maintenance"
            if "tour" in last_content or "budget" in last_content or "bedroom" in last_content:
                return "leasing"
                
        return "general"

    async def handle_leasing(self, user_msg: str, history: list) -> ChatResponse:
        """Delegate to LeasingAgent."""
        result = await self.leasing_agent.process(history, user_msg)
        
        return ChatResponse(
            response=result.message,
            agent_used="LeasingAgent",
            data={"action": result.action}
        )

    async def handle_maintenance(self, user_msg: str, history: list, db: Session, user_id: int) -> ChatResponse:
        """
        Delegate to MaintenanceAgent.
        """
        # Convert Pydantic messages to dict or string for the agent if needed, 
        # but our agent takes raw strings and history.
        # We can pass the history as is if the agent expects it, but for now passing just user string
        # as the agent is simple one-turn logic with history context construction.
        
        result = await self.maintenance_agent.process(history, user_msg)
        
        if result.action == "create_ticket":
            # Persist to DB
            ticket = Ticket(
                title=result.ticket_title or "Maintenance Request",
                description=result.ticket_description or user_msg,
                priority=result.ticket_priority or "medium",
                user_id=user_id,
                status="open"
            )
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
            
            return ChatResponse(
                response=f"{result.message} (Ticket ID: #{ticket.id})",
                agent_used="MaintenanceAgent",
                data={"ticket_id": ticket.id, "status": "created"}
            )
        else:
            # Just a reply/question
            return ChatResponse(
                response=result.message,
                agent_used="MaintenanceAgent"
            )

    async def general_chat(self, request: ChatRequest) -> ChatResponse:
        if self.llm:
            try:
                converted_history = []
                for msg in request.history:
                    if msg.role == "user":
                        converted_history.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        converted_history.append(AIMessage(content=msg.content))
                    elif msg.role == "system":
                        converted_history.append(SystemMessage(content=msg.content))
                
                converted_history.append(HumanMessage(content=request.message))
                
                # Add a system message if not present
                if not any(isinstance(m, SystemMessage) for m in converted_history):
                    converted_history.insert(0, SystemMessage(content="You are a helpful AI Property Management Assistant."))

                result = await self.llm.ainvoke(converted_history)
                content = result.content
            except Exception as e:
                content = f"I'm having trouble connecting to my brain right now. ({str(e)})"
        else:
            content = f"Echo: {request.message} (No API Key configured)"
            
        return ChatResponse(
            response=content,
            agent_used="Orchestrator"
        )

orchestrator = OrchestratorAgent()
