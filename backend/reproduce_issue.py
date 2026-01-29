
import asyncio
import os
from app.schemas.chat import ChatRequest, Message
from app.agents.orchestrator import OrchestratorAgent

async def reproduce():
    orchestrator = OrchestratorAgent()
    
    # Simulate Turn 3 history
    history = [
        Message(role="assistant", content="Hello! I'm your AI Property Manager. How can I help you today?"),
        Message(role="user", content="I have a maintenance issue"),
        Message(role="assistant", content="I understand you have a maintenance issue. Could you describe the problem in more detail? (e.g., 'Leaky faucet in kitchen', 'AC not cooling')"),
        Message(role="user", content="leaky faucet"),
        Message(role="assistant", content="Got it. How urgent is this? (Low, Medium, High, Emergency)")
    ]
    
    request = ChatRequest(
        message="high",
        user_id="test-user",
        history=history
    )
    
    print("Testing turn with message: high")
    response = await orchestrator.process(request)
    print(f"Agent Used: {response.agent_used}")
    print(f"Response: {response.response}")

if __name__ == "__main__":
    # Ensure we are in the right directory or set PYTHONPATH
    import sys
    sys.path.append(os.getcwd())
    asyncio.run(reproduce())
