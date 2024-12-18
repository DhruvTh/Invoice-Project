from PIL import Image
from pdf2image import convert_from_bytes
from docx2pdf import convert
import os, tempfile, io, requests
import requests
from src.utils.Schemas import TokenCalculation

def url_to_pil_image(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: HTTP {response.status_code}")

    content = response.content
    file_type = response.headers.get('Content-Type', '').lower()

    if 'pdf' in file_type:
        images = convert_from_bytes(content)
        return images

    elif 'docx' in file_type or 'document' in file_type:
        # Convert DOCX to PDF, then to image
        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = os.path.join(temp_dir, 'temp.docx')
            pdf_path = os.path.join(temp_dir, 'temp.pdf')
            
            with open(docx_path, 'wb') as f:
                f.write(content)
            
            convert(docx_path, pdf_path)
            
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
            
            images = convert_from_bytes(pdf_content)
            return images

    elif 'image' in file_type:
        return [Image.open(io.BytesIO(content))]

    else:
        raise Exception(f"Unsupported file type: {file_type}")

def sum_token_cost(cost_data1 : TokenCalculation, cost_data2 : TokenCalculation) -> TokenCalculation:
    return TokenCalculation(
        prompt_tokens=cost_data1.prompt_tokens + cost_data2.prompt_tokens,
        prompt_tokens_cost=cost_data1.prompt_tokens_cost + cost_data2.prompt_tokens_cost,
        completion_tokens=cost_data1.completion_tokens + cost_data2.completion_tokens,
        completion_tokens_cost=cost_data1.completion_tokens_cost + cost_data2.completion_tokens_cost,
        llm_model=cost_data1.llm_model,
        image_cost=cost_data1.image_cost + cost_data2.image_cost
    )