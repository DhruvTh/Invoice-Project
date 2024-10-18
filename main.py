from llms.GeminiAI import GeminiAILLM
from llms.OpenAI import OpenAILLM
from llms.BaseLLM import BaseLLM
from llms.ClaudeAI import ClaudeAILLM
from Constant import *
import time, uvicorn, copy
from Schemas import LLMInput, History, Content, ImageData, LLMAPIInput, LLMModels, TaskResponse
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Globals import url_to_pil_image, send_data_supabase

app = FastAPI()

load_dotenv()

llm_models = LLMModels()

llm_list : dict[str, BaseLLM] = {
    llm_models.open_ai : OpenAILLM(),
    llm_models.claude_ai : ClaudeAILLM(),
    llm_models.gemini_ai : GeminiAILLM()
}


llms = [llm_models.open_ai] 

@app.post("/extract_data")
def extract_data(input_data: LLMAPIInput):
    st = time.time()
    llm_input = LLMInput(
        llm = input_data.llm,
        llm_model=input_data.llm_model,
        history=[History(
            role="user",
            content=Content(
                text="Please extract invoice details from given data. While extracting information, if invoice language is not in English, you must make sure that  you translate the details in English.  While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention None for any extracting parameter.",
                image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
            )
        )],
        function_call_list=[copy.deepcopy(invoice_extraction_schema)]
    )
    response, cost = llm_list[input_data.llm].generate_response(llm_input)

    output = TaskResponse(
        output=response,
        token_cost = cost.token_cost,
        time_required=time.time()-st,
        invoice_url=input_data.invoice_url
    )

    # send_data_supabase(extracted_data=output.model_dump())
    return JSONResponse(output.model_dump())



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=9000,
        workers=1,
    )
