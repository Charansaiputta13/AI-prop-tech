import sys
import os
import asyncio
from sqlalchemy.orm import Session

# Add current directory to path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.schemas.chat import ChatRequest, Message
from app.agents.orchestrator import OrchestratorAgent
from app.core.database import SessionLocal, Base, engine
from app.models.ticket import Ticket
from app.models.user import User

# Create tables
Base.metadata.create_all(bind=engine)

async def test_flow():
    db = SessionLocal()
    try:
        orchestrator = OrchestratorAgent()
        
        print("--- Starting Test Flow ---")
        
        # 1. User reports issue
        msg1 = "My sink is leaking really bad in the kitchen"
        req1 = ChatRequest(
            message=msg1,
            user_id="demo-user",
            history=[]
        )
        print(f"User: {msg1}")
        try:
            res1 = await orchestrator.process(req1, db)
            print(f"Agent: {res1.response} (Agent: {res1.agent_used})")
        except Exception as e:
            print(f"Error processing Turn 1: {e}")
            return

        # Update history
        history = [
            Message(role="user", content=msg1),
            Message(role="assistant", content=res1.response)
        ]
        
        # 2. User provides urgency if asked, or we check if ticket already created
        # If the agent was smart enough to get 'really bad' as high priority, it might have created it.
        # But let's assume it might ask.
        
        if "ticket" in res1.response.lower() or "created" in res1.response.lower():
            print("Ticket created in Turn 1!")
        else:
            msg2 = "It is an emergency"
            req2 = ChatRequest(
                message=msg2,
                user_id="demo-user",
                history=history
            )
            print(f"User: {msg2}")
            try:
                res2 = await orchestrator.process(req2, db)
                print(f"Agent: {res2.response} (Agent: {res2.agent_used})")
            except Exception as e:
                print(f"Error processing Turn 2: {e}")
                return

        # 3. Verify DB
        ticket = db.query(Ticket).order_by(Ticket.id.desc()).first()
        if ticket:
            print(f"\nSUCCESS: Ticket found in DB!")
            print(f"ID: {ticket.id}")
            print(f"Title: {ticket.title}")
            print(f"Description: {ticket.description}")
            print(f"Priority: {ticket.priority}")
            print(f"Status: {ticket.status}")
            print(f"Owner ID: {ticket.user_id}")
        else:
            print("\nFAILURE: No ticket found in DB.")
            
    finally:
        db.close()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY not set. Test might fail or use mock.")
    asyncio.run(test_flow())
