from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os

class LeasingResponse(BaseModel):
    action: Literal["reply", "search_units", "schedule_tour"] = Field(description="The action to take based on user intent.")
    message: str = Field(description="The message to send back to the user.")
    search_criteria_beds: Optional[int] = Field(default=None, description="Number of bedrooms requested (if searching).")
    search_criteria_budget: Optional[float] = Field(default=None, description="Budget limit requested (if searching).")
    tour_date: Optional[str] = Field(default=None, description="Preferred date/time for a tour (if scheduling).")

class LeasingAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=LeasingResponse)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful Leasing Agent for a property management company.
            Your goal is to help prospective tenants find apartments and schedule tours.
            
            CAPABILITIES:
            1. Search for units: If user asks for apartments, identifying bedroom count and budget.
            2. Schedule tours: If user wants to see a unit, ask for a preferred time.
            3. Answer questions: General questions about amenities, pet policy, etc.
            
            OUTPUT FORMAT:
            - If user wants to search, set action='search_units' and extract criteria.
            - If user wants a tour, set action='schedule_tour' and extract date/time.
            - If you need more info, set action='reply' and ask.
            
            STYLING RULES:
            - Use **Bold** for property names or key details.
            - Use Lists (- item) for features or options.
            - Keep paragraphs short.
            
            {format_instructions}
            """),
            ("human", "{input}"),
        ])
        
        self.chain = self.prompt | self.llm | self.parser

    async def process(self, history: list, user_input: str) -> LeasingResponse:
        try:
            response = await self.chain.ainvoke({
                "input": user_input,
                "format_instructions": self.parser.get_format_instructions()
            })
            return response
        except Exception as e:
            print(f"Error in LeasingAgent: {e}")
            return LeasingResponse(action="reply", message="I'm having trouble understanding. Could you please rephrase?")
