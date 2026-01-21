from typing import List, Dict, Any, Optional, Tuple
from openai import OpenAI
from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()

class LLMService:
    """
    A unified, simple wrapper around the LLM provider (OpenAI).
    Design Goal: No hidden prompts, no magic. Just explicit method calls.
    """
    
    def __init__(self):
        # We initialize the client lazily or immediately if key is present.
        # This keeps the code robust even if env var checks happen elsewhere.
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"  # Or gpt-3.5-turbo if cost is a concern

    def generate(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Simple text generation.
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"LLM Generation Failed: {e}")
            raise e

    def generate_with_tools(
        self, 
        messages: List[Dict[str, str]], 
        tools: List[Dict[str, Any]]
    ) -> Any:
        """
        Generates a response that MAY decide to call a tool.
        Returns the raw message object which might contain tool_calls.
        
        Args:
            messages: Full conversation history [{"role": "user", "content": ...}]
            tools: List of tool definitions in OpenAI format
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                temperature=0
            )
            
            return response.choices[0].message
            
        except Exception as e:
            logger.error(f"LLM Tool Generation Failed: {e}")
            raise e
