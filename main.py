from llms.GeminiAI import GeminiAILLM
from llms.OpenAI import OpenAILLM
from llms.BaseLLM import BaseLLM
from llms.ClaudeAI import ClaudeAILLM
from Constant import *
import time, uvicorn, copy
from Schemas import LLMInput, History, Content, ImageData, LLMAPIInput, LLMModels, TaskResponse, LLMAPIInputValidate
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Globals import url_to_pil_image, send_data_supabase
from Create_table import add_invoice,add_purchase_order
import condition_check as cc

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
    #print(type(response))
    InvoiceNumber = response["invoice_number"]
    InvoiceDate = response["invoice_date"]
    CustomerName = response["customer_details"]["name"]
    CustomerAddress = response["customer_details"]["address"]
    CustomerTRN = response["customer_details"]["tax_registration_number"]

    # Assuming PONumber is not directly available in the response, set it to None or a placeholder
    PONumber = 'None'  

    # Mapping item details from the first item in the "item_details" list
    ItemSlNo = response["item_details"][0]["serial_number"]
    ItemCode = 'None'  # Assuming ItemCode is not present in the response
    ItemDetail = response["item_details"][0]["name_and_description"]
    ItemQuantity = 1  # Assuming quantity is 1 as it's not explicitly provided
    ItemDueDate = '2024-01-01'  # Due date is not present in the response
    ItemUnitPrice = response["item_details"][0]["per_month_with_fuel"]
    ItemTaxRate = response["item_details"][0]["tax_details"]
    ItemTaxableAmount = response["item_details"][0]["per_month_with_fuel"]
    ItemTaxAmount = response["item_details"][0]["unit_total"] - response["item_details"][0]["per_month_with_fuel"]
    ItemGrossAmountPayable = response["item_details"][0]["unit_total"]

    PaymentCompany = response["customer_details"]["name"]
    PaymentAddress = response["customer_details"]["address"]
    PaymentBankName = response["payment_details"]["bank_name"]
    PaymentBranchName = 'None'  # Branch name is not present in the response
    PaymentAccount = response["payment_details"]["account_name"]
    PaymentIBAN = response["payment_details"]["iban"]
    PaymentCurrency = response["item_details"][0]["currency"]
    CompanyTRN = response["payment_details"]["tax_registration_number"]
    add_invoice(InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN)
    condition_checks={}
    condition_checks['vendor_name_check']=cc.check_vendor_name(InvoiceNumber)
    condition_checks['vendor_address_check']=cc.check_vendor_address(InvoiceNumber)
    condition_checks['invoice_currency_check']=cc.check_currency(InvoiceNumber)
    condition_checks['invoice_tax_check']=cc.check_tax_details(InvoiceNumber)
    condition_checks['invoice_gross_amount_check']=cc.check_amount(InvoiceNumber)
    condition_checks['invoice_taxable_amount_check']=cc.check_taxable_amount(InvoiceNumber)
    condition_checks['invoice_payment_details_check']=cc.check_payment_details(InvoiceNumber)
    output = TaskResponse(
        output=response,
        token_cost = cost.token_cost,
        time_required=time.time()-st,
        invoice_url=input_data.invoice_url,
        condition_checks=condition_checks
    )

    # send_data_supabase(extracted_data=output.model_dump())
    return JSONResponse(output.model_dump())


@app.post("/extract_po_data")
def extract_data(input_data: LLMAPIInput):
    st = time.time()
    llm_input = LLMInput(
        llm = input_data.llm,
        llm_model=input_data.llm_model,
        history=[History(
            role="user",
            content=Content(
                text="Please extract po details from given data. While extracting information, if invoice language is not in English, you must make sure that  you translate the details in English.  While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention None for any extracting parameter.",
                image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
            )
        )],
        function_call_list=[copy.deepcopy(purchase_order_extraction_schema)]
    )
    response, cost = llm_list[input_data.llm].generate_response(llm_input)
    PODate = response["PO_Date"] if response["PO_Date"] is not None else 'Unknown'
    PO_number = response["PO_number"] if response["PO_number"] is not None else 'Unknown'
    Vendor_name = response["Vendor_name"] if response["Vendor_name"] is not None else 'Unknown Vendor'
    Vendor_address = response["Vendor_Address"] if response["Vendor_Address"] is not None else 'Unknown Address'
    Vendor_contact = response["Vendor_Contact"] if response["Vendor_Contact"] is not None else 'No Contact'
    SKU_Code = response["SKU_Code"] if response["SKU_Code"] is not None else 'No SKU'
    SKU_Desc = response["SKU_Desc"] if response["SKU_Desc"] is not None else 'No Description'
    Quantity = response["Quantity"] if response["Quantity"] is not None else 0
    price_per_pack = response["price_per_pack"] if response["price_per_pack"] is not None else 0.0
    Currency_Code = response["Currency_Code"] if response["Currency_Code"] is not None else 'Unknown Currency'
    price_per_L_or_Kg = response["Price_AED_per_L_or_Kg"] if response["Price_AED_per_L_or_Kg"] is not None else 'Unknown'
    Price_VAT_Included = response["Price_Incl_VAT_AED_per_pack"] if response["Price_Incl_VAT_AED_per_pack"] is not None else False
    Tax_percent = response["VAT_percent"] if response["VAT_percent"] is not None else 0
    AuthorizedBy = response["AuthorizedBy"] if response["AuthorizedBy"] is not None else 'Unknown Authorizer'
    Special_Instructions = response["Special_Instructions_Comments"] if response["Special_Instructions_Comments"] is not None else 'No Special Instructions'

    add_purchase_order(PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions)
    output = TaskResponse(
        output=response,
        token_cost = cost.token_cost,
        time_required=time.time()-st,
        invoice_url=input_data.invoice_url
    )

    # send_data_supabase(extracted_data=output.model_dump())
    return JSONResponse(output.model_dump())


@app.post("/identify_invoice")
def extract_data(input_data: LLMAPIInput):
    st = time.time()
    llm_input = LLMInput(
        llm = input_data.llm,
        llm_model=input_data.llm_model,
        history=[History(
            role="user",
            content=Content(
                text="Please extract the invoice type. While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention false for any extracting parameter.",
                image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
            )
        )],
        function_call_list=[copy.deepcopy(invoice_type_schema)]
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






@app.post("/validate_incoice_number")
def extract_data(input_data: LLMAPIInputValidate):
    st = time.time()
    llm_input = LLMInput(
        llm = input_data.llm,
        llm_model=input_data.llm_model,
        history=[History(
            role="user",
            content=Content(
                text=f"We have a vendor table with columns as (VendorName,VendorType,Address,Currency,TaxDetails,BankName,BranchName,BankAccount,BankSwiftCode), a purchaseorder table with columns as (PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions) and a invoice table with columns as (InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN). Now we want to convert all the below conditions mentioned in english into a where condition based on sqlite syntax(SQL dialect) without the term where. The conditions are: invoice number->{input_data.invoice_number} condition1->{input_data.condition1},condition2->{input_data.condition2},condition3->{input_data.condition3},condition4->{input_data.condition4},condition5->{input_data.condition5},condition6->{input_data.condition6}"
                #conditions_data=[input_data.invoice_number,input_data.condition1,input_data.condition2,input_data.condition3,input_data.condition4,input_data.condition5,input_data.condition6]
            )
        )],
        function_call_list=[copy.deepcopy(validate_incoice_conditions_schema)]
    )
    response, cost = llm_list[input_data.llm].generate_response(llm_input)
    
    condition_checks={}
    condition_checks['vendor_address_check']=cc.check_vendor_address(input_data.invoice_url,response["condition1"])
    condition_checks['invoice_currency_check']=cc.check_currency(input_data.invoice_url,response["condition2"])
    condition_checks['invoice_tax_check']=cc.check_tax_details(input_data.invoice_url,response["condition3"])
    condition_checks['invoice_gross_amount_check']=cc.check_amount(input_data.invoice_url,response["condition4"])
    condition_checks['invoice_taxable_amount_check']=cc.check_taxable_amount(input_data.invoice_url,response["condition5"])
    condition_checks['invoice_payment_details_check']=cc.check_payment_details(input_data.invoice_url,response["condition6"])
    output = TaskResponse(
        output=response,
        token_cost = cost.token_cost,
        time_required=time.time()-st,
        invoice_number=input_data.invoice_number
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

