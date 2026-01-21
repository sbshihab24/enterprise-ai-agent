from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    """
    user_id: str = Field(..., description="Unique identifier for the user to track session memory.")
    message: str = Field(..., min_length=1, description="The user's input message.")

class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint.
    Hides internal complexity while providing useful metadata.
    """
    response: str = Field(..., description="The agent's final answer to the user.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional info: tools used, memory retrieved, execution time, etc."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The capital of France is Paris.",
                "metadata": {
                    "tools_used": ["search_tool"],
                    "memory_retrieved": True
                }
            }
        }
