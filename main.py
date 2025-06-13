from smolagents.agents import CodeAgent
from smolagents import InferenceClientModel,HfApiModel
from smolagents import DuckDuckGoSearchTool, LiteLLMModel,FinalAnswerTool,WikipediaSearchTool
from pathlib import Path
from datetime import datetime
from tools import save_to_txt
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
import json
class ResearchSchema(BaseModel):

    topic:str
    summary :str
    sources:list[str]
    tools_used:list[str]

parser = PydanticOutputParser(pydantic_object=ResearchSchema)
# model = LiteLLMModel(
#     model_id="ollama/gemma3:latest",  # Added 'ollama/' prefix
#     api_base="http://localhost:11434",        # Changed to http://
#     num_ctx=8192,
    
# )
def build_prompt(user_query: str, format_instructions: str) -> str:
    return f"""
You are a research assistant. When given a query, you must research using available tools 
and then return the result in the following structured JSON format:

{format_instructions}

Now, here's the query:
{user_query}

If the user asks to save the result, use the save_to_txt tool after completing the research.
"""

