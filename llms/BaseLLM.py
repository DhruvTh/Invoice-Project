from typing import Iterator, Any
from Schemas import LLMInput, TaskResponse
from Constant import llm_model_list


class BaseLLM:
    def __init__(self) -> None:
        self.task_cost = None
        self.function_name = None
        self.function_input = []
    

    def prepare_cost(self, input_data: LLMInput, prompt_tokens: int, completion_tokens: int, image_tokens: int = 0) -> TaskResponse:

        task_response = TaskResponse()
        task_response.output = None

        task_response.token_cost.prompt_tokens = prompt_tokens

        input_token_cost = llm_model_list[input_data.llm][input_data.llm_model].input_cost_per_token

        task_response.token_cost.prompt_tokens_cost = prompt_tokens * input_token_cost 

        task_response.token_cost.completion_tokens = completion_tokens

        output_token_cost = llm_model_list[input_data.llm][input_data.llm_model].output_cost_per_token

        task_response.token_cost.completion_tokens_cost = completion_tokens * output_token_cost
    
        task_response.token_cost.llm_model = input_data.llm_model
        
        if input_data.image_analyze == True:
            image_cost = llm_model_list[input_data.llm][input_data.llm_model].image_cost_per_token
            
            task_response.token_cost.image_cost = image_tokens * image_cost

        return task_response

    def prepare_prompt(self, input_data: LLMInput):
        raise NotImplementedError("Not implemented in BaseLLM")

    def get_llm(self, input_data: LLMInput):
        raise NotImplementedError("Not implemented in BaseLLM")

    def get_data(self, llm: Any, input_data: LLMInput, messages: Any):
        raise NotImplementedError("Not implemented in BaseLLM")

    def calculate_tokens(self, messages: Any, output_data: Any, input_data: LLMInput, llm : Any = None):
        raise NotImplementedError("Not implemented in BaseLLM")
    
    def get_response(self, output_data : Any):
        raise NotImplementedError()

    def generate_response(self, input_data: LLMInput) -> tuple[dict, TaskResponse]:

        messages = self.prepare_prompt(input_data)

        llm = self.get_llm(input_data)

        response = self.get_data(llm, input_data, messages)
        input_tokens, output_tokens, image_tokens = self.calculate_tokens(
            messages, response, input_data, llm
        )
        task_cost: TaskResponse = self.prepare_cost(
            input_data, input_tokens, output_tokens, image_tokens
        )
        return self.get_response(response), task_cost

