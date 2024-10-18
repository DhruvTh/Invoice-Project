import os
from pdf2image import convert_from_path
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types.content_types import FunctionDeclaration


load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def pdf_to_images(pdf_path = "/home/dhruv/test/91springboard-invoice-RI-1460.pdf", dpi=300):
    return convert_from_path(pdf_path, dpi=dpi)

def get_header_content():
    images = pdf_to_images()
    content = [header_extraction_prompt]
    content.append(genai.upload_file("/home/dhruv/test/images/page_1.png"))
    tool = FunctionDeclaration(
        name=invoice_header_extraction_tool["function"]["name"],
        description=invoice_header_extraction_tool["function"]["description"],
        parameters=invoice_header_extraction_tool["function"]["parameters"]
    )
    return content, tool

def get_header_data():
    
    content, tool = get_header_content()

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction="You are a helpful assistant.", tools=[tool])

    response = model.generate_content(
        {
            "role": "user",
            "parts": content
        }
    )
    print(response.candidates[0].content.parts[0].function_call)

    return response.usage_metadata.total_token_count

def get_vendor_content():
    images = pdf_to_images()
    content = [vendor_extraction_prompt]
    content.append(genai.upload_file("/home/dhruv/test/images/page_1.png"))
    tool = FunctionDeclaration(
        name=invoice_vendor_information_tool["function"]["name"],
        description=invoice_vendor_information_tool["function"]["description"],
        parameters=invoice_vendor_information_tool["function"]["parameters"]
    )
    return content, tool

def get_vendor_data():
    
    content, tool = get_vendor_content()

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction="You are a helpful assistant.", tools=[tool])

    response = model.generate_content(
        {
            "role": "user",
            "parts": content
        }
    )
    print(response.candidates[0].content.parts[0].function_call)

    return response.usage_metadata.total_token_count

def get_client_content():
    images = pdf_to_images()
    content = [client_extraction_prompt]
    content.append(genai.upload_file("/home/dhruv/test/images/page_1.png"))
    tool = FunctionDeclaration(
        name=invoice_client_information_tool["function"]["name"],
        description=invoice_client_information_tool["function"]["description"],
        parameters=invoice_client_information_tool["function"]["parameters"]
    )
    return content, tool

def get_client_data():
    
    content, tool = get_client_content()

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction="You are a helpful assistant.", tools=[tool])

    response = model.generate_content(
        {
            "role": "user",
            "parts": content
        }
    )
    print(response.candidates[0].content.parts[0].function_call)

    return response.usage_metadata.total_token_count

def get_financial_content():
    images = pdf_to_images()
    content = [financial_extraction_prompt]
    content.append(genai.upload_file("/home/dhruv/test/images/page_1.png"))
    tool = FunctionDeclaration(
        name=invoice_financial_information["function"]["name"],
        description=invoice_financial_information["function"]["description"],
        parameters=invoice_financial_information["function"]["parameters"]
    )
    return content, tool

def get_financial_data():
    
    content, tool = get_financial_content()

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction="You are a helpful assistant.", tools=[tool])

    response = model.generate_content(
        {
            "role": "user",
            "parts": content
        }
    )
    print(response.candidates[0].content.parts[0].function_call)

    return response.usage_metadata.total_token_count

def get_item_detail_content():
    images = pdf_to_images()
    content = [item_details_extraction_prompt]
    content.append(genai.upload_file("/home/dhruv/test/images/page_1.png"))
    tool = FunctionDeclaration(
        name=invoice_item_details_tool["function"]["name"],
        description=invoice_item_details_tool["function"]["description"],
        parameters=invoice_item_details_tool["function"]["parameters"]
    )
    return content, tool

def get_item_data():
    
    content, tool = get_item_detail_content()

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction="You are a helpful assistant.", tools=[tool])

    response = model.generate_content(
        {
            "role": "user",
            "parts": content
        }
    )
    print(response.candidates[0].content.parts)

    return response.usage_metadata.total_token_count


import time

st = time.time()

total_tokens = get_header_data() + get_vendor_data() + get_client_data() + get_financial_data() + get_item_data()

print(total_tokens)
print(time.time()-st)