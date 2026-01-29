from app.schemas.chat import ChatRequest, ChatResponse
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

# Placeholder for real LangGraph Orchestrator
class OrchestratorAgent:
    def __init__(self):
        # Initialize LLM (Mock or Real if key exists)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        else:
            self.llm = None

    async def process(self, request: ChatRequest) -> ChatResponse:
        """
        Main entry point. 
        """
        user_msg = request.message
        history = request.history or []

        # 1. Check if we are already in a conversation with a sub-agent
        active_agent = self._detect_active_agent(history)
        print(f"DEBUG: history length: {len(history)}")
        print(f"DEBUG: active_agent detected: {active_agent}")
        
        if active_agent == "MaintenanceAgent":
            return await self.handle_maintenance_turn(user_msg, history)
        
        # 2. If no active agent, try to route based on intent
        if "maintenance" in user_msg.lower() or "fix" in user_msg.lower() or "leak" in user_msg.lower():
            # Start Maintenance Flow
            return ChatResponse(
                response="I understand you have a maintenance issue. Could you describe the problem in more detail? (e.g., 'Leaky faucet in kitchen', 'AC not cooling')",
                agent_used="MaintenanceAgent"
            )
        
        if "rent" in user_msg.lower() or "pay" in user_msg.lower():
            return ChatResponse(
                response="I can help with rent and payments. usage: 'Pay rent', 'Show invoice history'.",
                agent_used="FinanceAgent"
            )

        # 3. Default: General Chat
        return await self.general_chat(request)

    def _detect_active_agent(self, history: list) -> str:
        """
        Heuristic to find if we are already talking to a specific agent.
        Look at the last several Assistant messages to find the most recent active flow.
        """
        if not history:
            return None
        
        # Iterate backwards through history to find the most recent assistant message 
        # that indicates an active agent flow.
        for msg in reversed(history):
            if msg.role == "assistant":
                content = msg.content.lower()
                # Check for keywords that indicate an active flow
                if ("maintenance agent" in content or 
                    "describe the problem" in content or 
                    "priority level" in content or
                    "maintenance issue" in content or
                    "urgent" in content or
                    "how urgent" in content or
                    "emergency" in content):
                    return "MaintenanceAgent"
                if "finance agent" in content or "rent" in content or "invoice" in content:
                    return "FinanceAgent"
        
        return None

    async def handle_maintenance_turn(self, user_msg: str, history: list) -> ChatResponse:
        """
        Simulate Maintenance Agent logic state machine.
        """
        # 1. Find the most recent assistant message that was actually a question/prompt
        # This allows us to ignore "Echo" or generic "I've noted that" messages.
        last_relevant_bot_msg = ""
        for msg in reversed(history):
            if msg.role == "assistant":
                content = msg.content.lower()
                if "urgent" in content or "priority" in content or "emergency" in content or "describe" in content or "maintenance issue" in content:
                    last_relevant_bot_msg = content
                    break
        
        user_msg_lower = user_msg.lower()
        
        # State: Prior Bot asked for urgency
        if "urgent" in last_relevant_bot_msg or "priority" in last_relevant_bot_msg or "emergency" in last_relevant_bot_msg:
            # Check if user provided a priority
            priorities = ["low", "medium", "high", "emergency", "urgent"]
            if any(p in user_msg_lower for p in priorities):
                import random
                ticket_id = f"M-{random.randint(1000, 9999)}"
                return ChatResponse(
                    response=f"I've logged a maintenance request for you with priority: **{user_msg.upper()}**. Ticket ID: **{ticket_id}**. A vendor will be assigned shortly.",
                    agent_used="MaintenanceAgent"
                )

        # State: Bot asked for description
        if "describe" in last_relevant_bot_msg or "maintenance issue" in last_relevant_bot_msg:
            return ChatResponse(
                response="Got it. How urgent is this? (Low, Medium, High, Emergency)",
                agent_used="MaintenanceAgent"
            )
            
        # Fallback
        return ChatResponse(
            response="I've noted that. Is there anything else about this maintenance request?",
            agent_used="MaintenanceAgent"
        )
        
    async def general_chat(self, request: ChatRequest) -> ChatResponse:
        if self.llm:
            # Simple direct LLM call
            messages = [
                SystemMessage(content="You are a helpful AI Property Management Assistant."),
                HumanMessage(content=request.message)
            ]
            result = self.llm.invoke(messages)
            content = result.content
        else:
            content = f"Echo: {request.message} (No API Key configured)"
            
        return ChatResponse(
            response=content,
            agent_used="Orchestrator"
        )

orchestrator = OrchestratorAgent()
