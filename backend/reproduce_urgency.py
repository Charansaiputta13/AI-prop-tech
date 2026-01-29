
import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(r"c:\Users\charan\.gemini\antigravity\scratch\ai-prop-tech\backend")

from app.schemas.chat import ChatRequest, Message
from app.agents.orchestrator import orchestrator

async def run_test():
    print("--- Starting Urgency Reproduction Test ---")
    
    # Context: Bot just asked for urgency
    last_bot_msg = "Got it. How urgent is this? (Low, Medium, High, Emergency)"
    
    print(f"\nPrevious Bot Msg: {last_bot_msg}")
    print("\nTurn: User says 'high'")
    
    history = [
        Message(role="user", content="My sink is leaking"),
        Message(role="assistant", content=last_bot_msg)
    ]
    
    req = ChatRequest(
        message="high",
        user_id="test_user",
        history=history
    )
    
    resp = await orchestrator.process(req)
    print(f"Bot Response: {resp.response}")
    print(f"Agent Used: {resp.agent_used}")

    # Check logic
    if "Ticket ID" in resp.response:
         print("\nSUCCESS: Ticket created.")
    elif "Echo" in resp.response:
         print("\nFAILURE: Fell back to Echo/General Chat.")
    else:
         print(f"\nUNKNOWN RESULT: {resp.response}")

if __name__ == "__main__":
    asyncio.run(run_test())
