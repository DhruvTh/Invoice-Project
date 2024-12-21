from fastapi import Query
from typing import Optional, List, Literal, Union, Any
from pydantic import BaseModel, Field
from datetime import date
from src.utils.Constant import BASE_CONDITIONS

class ImageData(BaseModel):
    url: Any
    details: Optional[Literal["high", "low"]] = "low"


class Content(BaseModel):
    text: str
    image_data: Optional[List[ImageData]] = Field(default=None, max_length=20)
    condition_data: Optional[List[str]] = Field(default=None, max_length=100)


class History(BaseModel):
    role: Optional[Literal["user", "assistant"]] = "user"
    content: Content



class LLMInput(BaseModel):
    llm : str 
    llm_model: str = "claude-3-5-sonnet-20240620"  
    history: List[History]
    temperature: float = Query(default=0, ge=0, le=1)
    system_msg: Optional[str] = "You are a helpful assistant."
    function_call_list : Optional[list]
    image_analyze : Optional[bool] = True

class InvoiceType(BaseModel):
    handwritten_invoice : Optional[bool] = False
    digital : Optional[bool] = True

class LLMAPIInput(BaseModel):
    llm : str = "ClaudeAI"
    llm_model: str = "claude-3-5-sonnet-20240620"
    invoice_url : str
    conditions : Optional[list[str]] = BASE_CONDITIONS
    check_invoice_type : InvoiceType

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
    final_invoice_result : Optional[bool] = None
    extracted_invoice_data : Optional[dict] = None
    provided_conditions : Optional[list[str]] = None
    error : Optional[str] = None



class CustomerDetails(BaseModel):
    name: str
    address: str
    tax_registration_number: str


class ExtractedInvoiceData(BaseModel):
    invoice_number: str
    invoice_date: date
    po_number : str
    customer_details: CustomerDetails
    grand_total: float
