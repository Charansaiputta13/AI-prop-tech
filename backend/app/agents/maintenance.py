from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os

class MaintenanceResponse(BaseModel):
    action: Literal["reply", "create_ticket"] = Field(description="The action to take: 'reply' to ask for more info, or 'create_ticket' if we have all details.")
    message: str = Field(description=" The message to send back to the user.")
    ticket_title: Optional[str] = Field(default=None, description="Short title of the issue if creating a ticket.")
    ticket_description: Optional[str] = Field(default=None, description="Detailed description of the issue if creating a ticket.")
    ticket_priority: Optional[str] = Field(default=None, description="Priority level: low, medium, high, emergency. Default to medium.")

class MaintenanceAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=MaintenanceResponse)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful Maintenance Assistant for a property management company.
            Your goal is to gather information about a maintenance issue and create a ticket.
            
            REQUIRED INFORMATION FOR A TICKET:
            1. Description of the issue (what is broken, where is it).
            2. Priority/Urgency (low, medium, high, emergency).
            
            If you have all the required information, set action to 'create_ticket'.
            If you are missing information, set action to 'reply' and ask the user for the missing details.
            
            STYLING RULES:
            - Use **Bold** for key questions.
            - Use Lists for multiple questions.
            
            Be polite and professional.
            
            {format_instructions}
            """),
            ("human", "{input}"),
        ])
        
        self.chain = self.prompt | self.llm | self.parser

    async def process(self, history: list, user_input: str) -> MaintenanceResponse:
        # Construct a conversation string from history for context (simplified)
        # In a real app, we'd pass the connection history properly.
        # For now, we rely on the latest input + implied context or just pass the last few messages.
        
        try:
            response = await self.chain.ainvoke({
                "input": user_input,
                "format_instructions": self.parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error in MaintenanceAgent: {e}")
            return MaintenanceResponse(action="reply", message="I'm having trouble understanding. Could you please describe the issue again?")
