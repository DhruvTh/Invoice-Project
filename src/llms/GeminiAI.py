from typing import List, Iterator
from src.utils.Schemas import LLMInput, History
from src.llms.BaseLLM import BaseLLM
from src.utils.Constant import INVALID_ROLE_TYPE_ERROR_MSG
import google.generativeai as genai
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.generation_types import GenerateContentResponse
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class GeminiAILLM(BaseLLM):
    def __init__(self) -> None:
        super().__init__()


    def prepare_img_content(self, msg: History) -> List[dict]:
        content = []
        for i in msg.content.image_data:
            content.append(i.url)
        content.append(msg.content.text)

        return content

    def prepare_msg(self, msg: History, image_analyze: bool) -> dict:
        if msg.role == "user":
            if image_analyze == True and msg.content.image_data != None:
                return {
                        "role" : "user",
                        "parts" : self.prepare_img_content(msg)
                    }
            else:
                return {
                    "role" : "user",
                    "parts" : msg.content.text
                }

        elif msg.role == "assistant":
            return {
                    "role" : "model",
                    "parts" : msg.content.text
            }
        
        else:
            raise Exception(INVALID_ROLE_TYPE_ERROR_MSG)

    def prepare_prompt(self, input_data: LLMInput) -> List[dict]:
        messages: List[dict] = []
            
        for i in input_data.history:
            messages.append(self.prepare_msg(i, input_data.image_analyze))

        return messages

    def get_llm(self, input_data: LLMInput) -> genai.GenerativeModel:
        return genai.GenerativeModel(
                input_data.llm_model,
                system_instruction=input_data.system_msg,
                tools=self.modify_tool_dict(input_data.function_call_list)
            )

    
    def modify_tool_dict(self, tools : list[dict]) -> list[dict]:
        modified_tools = []
        for i in range(len(tools)):
            modified_tools.append(FunctionDeclaration(
                name=tools[i]["function"]["name"],
                description=tools[i]["function"]["description"],
                parameters=tools[i]["function"]["parameters"]
            ))

        return modified_tools

    def get_data(self, llm: genai.GenerativeModel, input_data: LLMInput, messages: List[dict]) -> Iterator:
        convo = llm.start_chat(history=messages[:-1])
        tool_config = {"function_calling_config": {"mode": "ANY"}}
        convo = llm.start_chat(history=messages[:-1])
        return convo.send_message(messages[-1], stream=False, tools=self.modify_tool_dict(input_data.function_call_list), tool_config=tool_config)

    def get_response(self, output_data : GenerateContentResponse) -> dict:
        return output_data.to_dict()["candidates"][0]["content"]["parts"][0]["function_call"]["args"]

    def calculate_tokens(self, messages: List[History], output_data: GenerateContentResponse, input_data: LLMInput, llm : genai.GenerativeModel) -> List[int]:
        return [
            output_data.usage_metadata.prompt_token_count,
            output_data.usage_metadata.candidates_token_count,
            0
        ]
