import math
from app.tools.base import BaseTool
from app.core.logger import logger

class MathTool(BaseTool):
    name = "math_tool"
    description = "Useful for calculating math expressions. Input should be a valid mathematical expression (e.g., '2 + 2', 'sqrt(16)')."

    def run(self, query: str) -> str:
        """
        Evaluates a math expression safely using Python's eval with restricted globals.
        """
        logger.info(f"MathTool called with query: {query}")
        
        # Safe dictionary of allowed functions
        safe_dict = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        
        try:
            # Clean the query
            clean_query = query.strip()
            
            # Simple restricted eval
            result = eval(clean_query, {"__builtins__": None}, safe_dict)
            return str(result)
            
        except Exception as e:
            return f"Error calculating '{query}': {str(e)}"
