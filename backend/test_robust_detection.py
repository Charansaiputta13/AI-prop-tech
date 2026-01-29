
import asyncio
import os
import sys
from app.schemas.chat import ChatRequest, Message
from app.agents.orchestrator import orchestrator

async def test_robustness():
    print("--- Starting Robustness Test ---")
    
    # Context: Bot asked for urgency, but then some other message was added (e.g. an Echo or manual note)
    history = [
        Message(role="assistant", content="Hello! I'm your AI Property Manager. How can I help you today?"),
        Message(role="user", content="I have a maintenance issue"),
        Message(role="assistant", content="I understand you have a maintenance issue. Could you describe the problem in more detail?"),
        Message(role="user", content="leaky faucet"),
        Message(role="assistant", content="Got it. How urgent is this? (Low, Medium, High, Emergency)"),
        Message(role="assistant", content="Echo: high (No API Key configured)"), # Simulated interference
    ]
    
    req = ChatRequest(
        message="low",
        user_id="test_user",
        history=history
    )
    
    print("\nTurn: User says 'low' (after an 'Echo' message was already in history)")
    
    resp = await orchestrator.process(req)
    print(f"Bot Response: {resp.response}")
    print(f"Agent Used: {resp.agent_used}")

    if "Ticket ID" in resp.response:
         print("\nSUCCESS: Robust detection worked!")
    else:
         print("\nFAILURE: Robust detection failed.")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    asyncio.run(test_robustness())
