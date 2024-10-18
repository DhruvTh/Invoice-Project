from fastapi import Query
from typing import Optional, List, Literal, Union, Any
from pydantic import BaseModel, Field


class ImageData(BaseModel):
    url: Any
    details: Optional[Literal["high", "low"]] = "low"


class Content(BaseModel):
    text: str
    image_data: Optional[List[ImageData]] = Field(default=None, max_length=20)


class History(BaseModel):
    role: Optional[Literal["user", "assistant"]] = "user"
    content: Content



class LLMInput(BaseModel):
    llm : str 
    llm_model: str = "gpt-4o-mini"  
    history: List[History]
    temperature: float = Query(default=0, ge=0, le=1)
    system_msg: Optional[str] = "You are a helpful assistant."
    function_call_list : Optional[list]
    image_analyze : Optional[bool] = True

class LLMAPIInput(BaseModel):
    llm : str = "OpenAI"
    llm_model: str = "gpt-4o-mini"
    invoice_url : str
    email_id : Optional[str] = None


class TokenCalculation(BaseModel):
    prompt_tokens: Optional[int] = 0
    prompt_tokens_cost: Optional[float] = 0
    completion_tokens: Optional[int] = 0
    completion_tokens_cost: Optional[float] = 0
    llm_model: Optional[str] = None
    image_cost: Optional[float] = 0



class TaskResponse(BaseModel):
    output: Optional[Union[str, dict, list]] = None
    token_cost: Optional[TokenCalculation] = Field(default_factory=TokenCalculation)
    time_required : Optional[float] = None
    invoice_url : Optional[str] = None


class LLMModelCostConfig(BaseModel):
    input_cost_per_token: float
    output_cost_per_token: float
    image_supported: bool = False
    image_cost_per_token: float = 0


class LLMModels(BaseModel):
    mistral_ai: str = "MistralAI"
    mistral_small: str = "open-mixtral-8x7b"
    mistral_large: str = "mistral-large-latest"
    mistral_mini : str = "open-mistral-7b"	
    gemini_ai: str = "GeminiAI"
    gemini_pro: str = "gemini-pro"
    gemini_pro_vision: str = "gemini-pro-vision"
    gemini_15_pro : str = "gemini-1.5-pro-001"
    gemini_15_flash : str = "gemini-1.5-flash-001"
    open_ai: str = "OpenAI"
    gpt_4_0125_latest: str = "gpt-4-turbo-2024-04-09"
    gpt_4o_2024_05_13: str = "gpt-4o-2024-05-13"
    chatgpt_4o_latest: str = "gpt-4o-2024-08-06"		
    gpt_35_turbo_0125: str = "gpt-3.5-turbo-0125"
    gpt_4o_mini : str = "gpt-4o-mini"
    claude_3_haiku : str = "claude-3-haiku-20240307"
    claude_3_sonnet : str = "claude-3-sonnet-20240229"
    claude_3_opus : str = "claude-3-opus-20240229"
    claude_35_sonnet : str = "claude-3-5-sonnet-20240620"
    claude_ai : str = "ClaudeAI"
    codestral_latest : str = "codestral-latest"
    llamaai : str = "LLamaAI"
    llama3_405b_instruct : str = "meta/llama3-405b-instruct-maas"
    vertexmistralai : str = "VertexMistralAI"
    mistral_large_2407 : str = "mistral-large@2407"
    codestral_2405 : str = "codestral@2405"
    groqai : str = "GroqAI"
    llama_31_70b_versatile : str = "llama-3.1-70b-versatile"
    llama_31_8b_instant : str = "llama-3.1-8b-instant"

