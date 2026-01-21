from typing import Dict, Any
from app.tools.base import BaseTool
from app.services.llm_service import LLMService
from app.core.logger import logger

class SummarizerTool(BaseTool):
    name = "summarizer_tool"
    description = "Useful for summarizing long text into a concise summary."
    
    def __init__(self):
        # Initialize LLM service for summarization
        self.llm = LLMService()

    def run(self, text: str) -> str:
        logger.info(f"SummarizerTool called with text length: {len(text)}")
        
        prompt = f"Please summarize the following text concisely:\n\n{text}"
        try:
            summary = self.llm.generate(prompt)
            return summary
        except Exception as e:
            return f"Error summarizing text: {str(e)}"

    @property
    def openai_schema(self) -> Dict[str, Any]:
        """
        Override schema because parameter name is 'text', not 'query'.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The long text content to be summarized."
                        }
                    },
                    "required": ["text"]
                }
            }
        }
