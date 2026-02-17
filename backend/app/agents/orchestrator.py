from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.maintenance import MaintenanceAgent
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
            self.llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        else:
            self.llm = None
            
        self.maintenance_agent = MaintenanceAgent()

    async def process(self, request: ChatRequest, db: Session) -> ChatResponse:
        user_msg = request.message
        history = request.history or []
        
        # Resolve User (Simple logic for demo)
        # In a real app, we would get user_id from the auth token (Depends(get_current_user))
        user_id = self._get_or_create_demo_user(db)

        # 1. Check if we are in a maintenance flow or intent
        if self._is_maintenance_context(user_msg, history):
             return await self.handle_maintenance(user_msg, history, db, user_id)
        
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

    def _is_maintenance_context(self, user_msg: str, history: list) -> bool:
        """
        Determine if the user is talking about maintenance.
        Check current message and recent history.
        """
        keywords = ["fix", "leak", "broken", "repair", "maintenance", "not working", "hot water", "light", "power"]
        
        # check current message
        if any(k in user_msg.lower() for k in keywords):
            return True
            
        # check if last assistant message was from maintenance agent
        if history and history[-1].role == "assistant":
            # Heuristic: if last message asked about priority or description, we are likely in flow
            last_content = history[-1].content.lower()
            if "priority" in last_content or "describe" in last_content or "ticket" in last_content:
                return True
                
        return False

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
