from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """
    Abstract base class for all tools.
    Enforces a standard structure for the Agent to use.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def run(self, **kwargs) -> str:
        """
        Execute the tool logic.
        """
        pass

    @property
    def openai_schema(self) -> Dict[str, Any]:
        """
        Returns the function definition for OpenAI function calling.
        Can be overridden by subclasses if complex parameters are needed.
        Default assumes a single 'query' parameter for simplicity.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The input query or expression for the tool."
                        }
                    },
                    "required": ["query"]
                }
            }
        }
