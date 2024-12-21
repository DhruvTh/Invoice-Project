import requests
import base64

# Read a PDF file and convert it to base64
with open("/home/dhruv/Invoice-Project/123.pdf", "rb") as pdf_file:
    pdf_base64 = base64.b64encode(pdf_file.read()).decode()

# Make the request
response = requests.post(
    "http://localhost:8000/extract_data",
    json = {
        "llm": "ClaudeAI",
        "llm_model": "claude-3-5-sonnet-20240620",
        "invoice_url": pdf_base64,
        "conditions": [
            "True if the invoice is raised between 2023 and 2024, otherwise false.",
            "True if the invoice currency is AED, otherwise false.",
            "True if the invoice has a 5% tax rate, otherwise false.",
            "True if vendor name, tax registration number, and other details match with invoice data, otherwise false.",
            "True if the PO number in the invoice matches the given PO data, otherwise false."
        ],
        "check_invoice_type": {
            "handwritten_invoice": True,
            "digital": True
        }
        }
)

print(response.json())