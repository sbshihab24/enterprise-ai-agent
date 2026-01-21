from app.agents.reasoning_agent import ReasoningAgent
from app.tools.search_tool import SearchTool
from app.tools.math_tool import MathTool
from app.tools.summarizer_tool import SummarizerTool

class AgentManager:
    """
    Factory to create and manage agent instances.
    In a bigger app, this could handle multi-agent orchestration.
    """
    
    @staticmethod
    def get_agent() -> ReasoningAgent:
        # distinct tools for the main agent
        tools = [
            SearchTool(),
            MathTool(),
            SummarizerTool()
        ]
        
        return ReasoningAgent(tools=tools)
