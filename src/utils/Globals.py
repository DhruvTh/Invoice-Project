from PIL import Image
from pdf2image import convert_from_bytes
from docx2pdf import convert
import os, tempfile, io, requests
import requests
from src.utils.Schemas import TokenCalculation
import base64

def url_to_pil_image(url):
    pdf_bytes = base64.b64decode(url)

    images = convert_from_bytes(pdf_bytes)
    return images


def sum_token_cost(cost_data1 : TokenCalculation, cost_data2 : TokenCalculation) -> TokenCalculation:
    return TokenCalculation(
        prompt_tokens=cost_data1.prompt_tokens + cost_data2.prompt_tokens,
        prompt_tokens_cost=cost_data1.prompt_tokens_cost + cost_data2.prompt_tokens_cost,
        completion_tokens=cost_data1.completion_tokens + cost_data2.completion_tokens,
        completion_tokens_cost=cost_data1.completion_tokens_cost + cost_data2.completion_tokens_cost,
        llm_model=cost_data1.llm_model,
        image_cost=cost_data1.image_cost + cost_data2.image_cost
    )