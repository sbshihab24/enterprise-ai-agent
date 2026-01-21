from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """
    Abstract base class for all Agents.
    Guarantees that every agent can 'run' given a message and user_id.
    """
    
    @abstractmethod
    def run(self, message: str, user_id: str) -> Dict[str, Any]:
        """
        Main entry point for the agent.
        Returns a dictionary matching the ChatResponse contract (response + metadata).
        """
        pass
