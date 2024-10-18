from PIL import Image
from pdf2image import convert_from_bytes
from docx2pdf import convert
import os, smtplib, tempfile, io, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests, json
from datetime import datetime

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
    

## TODO : Need to replace the send email part with tempmail email sending API. But, card is required for sign into the Rapid API 

def send_email(receiver_email, subject, body, sender_email, sender_password ):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            print("after this")
            server.login(sender_email, sender_password)

            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

    except Exception as e:
        print(str(e))
        pass



def send_data_supabase(extracted_data : dict) -> None:

    PROJECT_ID = "yxaogvuhrlmduxjzcyjr"
    API_KEY = os.environ["SUPABASE_API_KEY"]

    # API endpoint
    url = f"https://{PROJECT_ID}.supabase.co/rest/v1/invoices"

    # Headers
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    # Prepare the payload
    payload = {
        "reference_number": extracted_data["output"]["invoice_number"],
        "date": extracted_data["output"]["invoice_date"],
        "customer_name": extracted_data["output"]["customer_details"]["name"],
        "customer_address": extracted_data["output"]["customer_details"]["address"],
        "customer_tax_number": extracted_data["output"]["customer_details"]["tax_registration_number"],
        "items": extracted_data["output"]["item_details"],
        "grand_total": extracted_data["output"]["grand_total"],
        "payment_mode": extracted_data["output"]["payment_details"]["payment_mode"],
        "bank_name": extracted_data["output"]["payment_details"]["bank_name"],
        "account_name": extracted_data["output"]["payment_details"]["account_name"],
        "iban": extracted_data["output"]["payment_details"]["iban"],
        "tax_registration_number": extracted_data["output"]["payment_details"]["tax_registration_number"],
        "file_path": extracted_data["invoice_url"],
        "document_type": "Invoice",
        "status": "Uploaded",
        "uploaded_by": "System"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 201:
        print("Invoice created successfully")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)