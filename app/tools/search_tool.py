from app.tools.base import BaseTool
from app.core.logger import logger

class SearchTool(BaseTool):
    name = "search_tool"
    description = "Useful for searching the internet for current events or facts. Input is a search query."

    def run(self, query: str) -> str:
        """
        Simulates a web search. 
        In a real production app, this would call Google Custom Search, Serper, or Tavily.
        """
        logger.info(f"SearchTool called with query: {query}")
        
        # Deterministic local implementation (as requested)
        query_lower = query.lower()
        
        if "python" in query_lower:
            return "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation."
        elif "capital of france" in query_lower:
            return "The capital of France is Paris."
        elif "enterprise ai" in query_lower:
            return "Enterprise AI refers to the deployment of artificial intelligence in large organizations to improve data analytics, automate processes, and enhance decision-making."
        elif "weather" in query_lower and "london" in query_lower:
            return "The current weather in London is 15°C with scattered clouds."
        else:
            return f"Search results for '{query}': [No specific deterministic match found, but this simulates a search engine result page.]"
