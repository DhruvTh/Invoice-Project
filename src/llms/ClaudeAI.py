from typing import List, Iterable
from src.utils.Schemas import LLMInput,  History
from src.llms.BaseLLM import BaseLLM
from anthropic import Anthropic
from PIL.Image import Image as Imagetype
import io, base64, os, json
from PIL import Image
from anthropic.types.message import Message
from src.utils.Constant import INVALID_ROLE_TYPE_ERROR_MSG

class ClaudeAILLM(BaseLLM):
    def __init__(self) -> None:
        super().__init__()
        self.client = Anthropic(api_key=os.environ["CLAUDEAI_API_KEY"])


    def get_image_data(self, image: Image.Image) -> Imagetype:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")

        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    

    def prepare_img_content(self, msg: History) -> List[dict]:
        content = [{"type": "text", "text": msg.content.text}]
        for i in msg.content.image_data:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": self.get_image_data(i.url),
                    },
                },
            )

        return content
    

    def prepare_msg(self, msg: History, image_analyze: bool) -> dict:
        if msg.role == "user":
            if image_analyze == True and msg.content.image_data != None:
                return {"role": "user", "content": self.prepare_img_content(msg)}
            else:
                return {
                    "role": "user",
                    "content": [{"type": "text", "text": msg.content.text}],
                }
        elif msg.role == "assistant":
            return {
                "role": "assistant",
                "content": [{"type": "text", "text": msg.content.text}],
            }
        else:
            raise Exception(INVALID_ROLE_TYPE_ERROR_MSG)

    def prepare_prompt(self, input_data: LLMInput) -> List[dict]:
        messages = []
        for i in input_data.history:
            messages.append(self.prepare_msg(i, input_data.image_analyze))

        return messages

    def get_llm(self, input_data: LLMInput) -> Anthropic:
        return self.client
    
    def modify_tool_dict(self, tools : list[dict]) -> list[dict]:
        for i in range(len(tools)):
            tools[i] = tools[i]["function"]
            tools[i]['input_schema'] = tools[i].pop('parameters')
        return tools

    def get_data(self, llm: Anthropic, input_data: LLMInput, messages: List[dict]) -> Iterable:
        return llm.messages.create(
                model=input_data.llm_model,
                messages=messages,
                temperature=input_data.temperature,
                system=input_data.system_msg,
                stream=False,
                tools=self.modify_tool_dict(input_data.function_call_list),
                max_tokens = 4096,
                tool_choice = {"type":"any"}
            )

    def get_response(self, output_data : Message) -> dict:
        return output_data.content[0].input
    
    def calculate_tokens(self, messages, output_data: Message, input_data: LLMInput, llm : Anthropic = None) -> List[int]:
        return [
            output_data.usage.input_tokens,
            output_data.usage.output_tokens,
            0
        ]
