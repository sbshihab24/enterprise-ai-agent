from fastapi import APIRouter, HTTPException, Depends
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.agents.agent_manager import AgentManager
from app.core.logger import logger

router = APIRouter()

# Dependency to get the agent. 
# In a more complex app, we might check auth or load-balance agents here.
def get_agent():
    return AgentManager.get_agent()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, agent = Depends(get_agent)):
    """
    Primary endpoint for user interaction.
    Delegates logic to the Reasoning Agent.
    """
    logger.info(f"Received chat request from user: {request.user_id}")
    
    try:
        # Run the agent logic
        result = agent.run(request.message, request.user_id)
        
        # Map dictionary result to Pydantic model
        return ChatResponse(
            response=result["response"],
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        # Return a clean error to the client, hiding internal stack traces
        raise HTTPException(status_code=500, detail="Internal Server Error processing request.")
