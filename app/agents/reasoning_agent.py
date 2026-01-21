import json
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
from app.memory.memory_manager import MemoryManager
from app.tools.base import BaseTool
from app.core.logger import logger

class ReasoningAgent(BaseAgent):
    """
    The main agent that thinks, remembers, and acts.
    """
    
    def __init__(self, tools: List[BaseTool]):
        self.llm = LLMService()
        self.memory = MemoryManager()
        self.tools = {tool.name: tool for tool in tools}
        
        # Pre-calculate OpenAI tool schemas
        self.tool_schemas = [tool.openai_schema for tool in tools]
        
        # Load system prompt
        with open("app/prompts/system_prompt.txt", "r") as f:
            self.system_prompt = f.read()

    def run(self, message: str, user_id: str) -> Dict[str, Any]:
        logger.info(f"Agent running for user {user_id}: {message}")
        
        # 1. Retrieve Context (Memory)
        past_memories = self.memory.retrieve_relevant_memory(message, user_id)
        
        # 2. Construct Prompt with Context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if past_memories:
            memory_block = "\n".join(past_memories)
            messages.append({
                "role": "system", 
                "content": f"Relevant Past Memories:\n{memory_block}"
            })
            
        messages.append({"role": "user", "content": message})
        
        # 3. LLM Generation (Reasoning Loop)
        tools_used = []
        
        # Initial call - Model decides to talk or use tool
        response_msg = self.llm.generate_with_tools(messages, self.tool_schemas)
        
        # Loop for tool handling
        # NOTE: In a complex ReAct loop, we might loop multiple times. 
        # For simplicity/safety, we handle one round of tool calls here.
        if response_msg.tool_calls:
            messages.append(response_msg)  # Add assistant's tool-call message to history
            
            for tool_call in response_msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Agent deciding to call tool: {fn_name} with {fn_args}")
                
                if fn_name in self.tools:
                    tool_instance = self.tools[fn_name]
                    # We assume arguments match (or we'd unpack differently)
                    # For simplicity, we pass the main argument.
                    # Our tools generally take 'query' or 'text'.
                    try:
                        result = tool_instance.run(**fn_args)
                    except Exception as e:
                        result = f"Error executing {fn_name}: {e}"
                        
                    tools_used.append(fn_name)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": fn_name,
                        "content": str(result)
                    })
            
            # 4. Final Answer Generate (after tool outputs)
            final_response = self.llm.generate_with_tools(messages, tools=None) # No tools for final answer
            answer_text = final_response.content
        else:
            # Direct answer
            answer_text = response_msg.content

        # 5. Save new interaction to memory
        self.memory.save_memory(user_id, message, "user")
        self.memory.save_memory(user_id, answer_text, "assistant")

        return {
            "response": answer_text,
            "metadata": {
                "tools_used": tools_used,
                "memory_retrieved": bool(past_memories)
            }
        }
