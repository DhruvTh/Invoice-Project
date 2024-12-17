from typing import List
import os, io, base64, json
from openai import OpenAI
from openai.types.chat import ChatCompletion
from src.utils.Schemas import LLMInput, History
from src.llms.BaseLLM import BaseLLM
from PIL import Image

class OpenAILLM(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def get_image_data(self, image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")

        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def prepare_img_content(self, msg: History) -> List[dict]:
        content = [{"type": "text", "text": msg.content.text}]
        for i in msg.content.image_data:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{self.get_image_data(i.url)}", "detail": i.details},
                }
            )

        return content

    def prepare_msg(self, msg: History, image_analyze: bool) -> dict:
        if msg.role == "user":

            if image_analyze == True and msg.content.image_data != None:
                return {"role": "user", "content": self.prepare_img_content(msg)}

            else:
                return {
                    "role": "user",
                    "content": msg.content.text,
                }

        elif msg.role == "assistant":
            return {
                "role": "assistant",
                "content": msg.content.text,
            }

        else:
            raise Exception("Invalid Role type")

    def prepare_prompt(self, input_data: LLMInput) -> List[dict]:
        messages = [{"role": "system", "content": input_data.system_msg}]
        for i in input_data.history:
            messages.append(self.prepare_msg(i, input_data.image_analyze))

        return messages

    def get_llm(self, input_data: LLMInput) -> OpenAI:
        return self.client

    def get_data(
        self, llm: OpenAI, input_data: LLMInput, messages: List[dict]
    ) -> ChatCompletion:
        return llm.chat.completions.create(
            messages=messages,
            model=input_data.llm_model,
            stream=False,
            temperature=input_data.temperature,
            tool_choice="required",
            tools=input_data.function_call_list,
            parallel_tool_calls = False,
        )
    
    def get_response(self, output_data : ChatCompletion)-> dict:
        return json.loads(output_data.choices[0].message.tool_calls[0].function.arguments)


    def calculate_tokens(
        self,
        messages: List[dict],
        output_data: ChatCompletion,
        input_data: LLMInput,
        llm : OpenAI = None 
    ) -> List[int]:

        return[
            output_data.usage.prompt_tokens,
            output_data.usage.completion_tokens,
            0
        ]
