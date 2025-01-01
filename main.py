from dotenv import load_dotenv
load_dotenv()

from src.llms.GeminiAI import GeminiAILLM
from src.llms.OpenAI import OpenAILLM
from src.llms.BaseLLM import BaseLLM
from src.llms.ClaudeAI import ClaudeAILLM
from src.utils.Constant import *
import time, uvicorn, copy, json
from src.utils.Schemas import LLMInput, History, Content, ImageData, LLMAPIInput, TaskResponse
from src.utils.Constant import LLMModels
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.utils.Globals import url_to_pil_image, sum_token_cost
from src.DB.MongoClient import InvoiceDataDB
from textwrap import dedent
from datetime import date
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


llm_models = LLMModels()

llm_list : dict[str, BaseLLM] = {
    llm_models.open_ai : OpenAILLM(),
    llm_models.claude_ai : ClaudeAILLM(),
    llm_models.gemini_ai : GeminiAILLM()
}


llms = [llm_models.open_ai] 

invoice_db = InvoiceDataDB()

invoice_db.connect_invoice_db()

@app.post("/extract_data")
def extract_data(input_data: LLMAPIInput):
    try:
        st = time.time()
        llm_input = LLMInput(
        llm = input_data.llm,
        llm_model=input_data.llm_model,
        history=[
            History(
                role="user",
                content=Content(
                    text="Please extract the invoice type. While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention false for any extracting parameter.",
                    image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
                )
            )],
            function_call_list=[copy.deepcopy(invoice_type_schema)]
        )
        invoice_identification_response, invoice_identify_cost = llm_list[input_data.llm].generate_response(llm_input)

        check_invoice = False
        if(invoice_identification_response["is_digital_invoice"] == True and input_data.check_invoice_type.digital == True):
            check_invoice = True
        if(invoice_identification_response["is_handwritten_invoice"] == True and input_data.check_invoice_type.handwritten_invoice == True):
            check_invoice = True
        
        if(check_invoice == False):
            raise Exception("Given document is not Invoice or Invoice is not according to defined category.")

        invoice_extraction_input = LLMInput(
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
        invoice_extraction_response, invoice_extraction_cost = llm_list[input_data.llm].generate_response(invoice_extraction_input)
        
        invoice_extraction_cost.token_cost = sum_token_cost(invoice_identify_cost.token_cost, invoice_extraction_cost.token_cost)

        invoice_str = json.dumps(invoice_extraction_response, indent=2)

        po_data = json.dumps(invoice_db.get_po(invoice_extraction_response["po_number"]), indent=2)

        vendor_data = json.dumps(invoice_db.get_vendor(invoice_extraction_response["customer_details"]["tax_registration_number"]), indent=2)
        
        added_params = []
        BASE_CONDITION_CHECK_SCHEMA_COPY = copy.deepcopy(BASE_CONDITION_CHECK_SCHEMA)
        for i in range(0, len(input_data.conditions)):
            BASE_CONDITION_CHECK_SCHEMA_COPY["function"]["parameters"]["properties"][f"condition_{i}"] = {
                "type": "boolean",
                "description": input_data.conditions[i]
            }
            BASE_CONDITION_CHECK_SCHEMA_COPY["function"]["parameters"]["properties"][f"reason_{i}"] = {
                "type": "string",
                "description": "Reason for the condition_1 result."
            }
            added_params.append(f"condition_{i}")
            added_params.append(f"reason_{i}")

        BASE_CONDITION_CHECK_SCHEMA_COPY["function"]["parameters"]["required"] = added_params

        condition_check_input = LLMInput(
            llm = input_data.llm,
            llm_model=input_data.llm_model,
            history=[History(
                role="user",
                content=Content(
                    text = dedent(
                        f"""Based on given PO data, vendor data and Invoice data, you must verify the conditions. If PO data and Vendor data are empty JSON or null, provide false for any comparision associated with vendor data and PO data. You must not assume any data by yourself. 
                        PO data : 
                        {po_data}

                        vendor data : 
                        {vendor_data}

                        invoice data : 
                        {invoice_str}

                        Today's Date : 
                        {date.today()}"""
                    )
                )
            )],
            function_call_list=[copy.deepcopy(BASE_CONDITION_CHECK_SCHEMA_COPY)]
        )

        condition_response, condition_check_cost = llm_list[input_data.llm].generate_response(condition_check_input)

        final_invoice_result = True
        for key, value in condition_response.items():
            if(type(value) == bool):
                if(value == False):
                    final_invoice_result = False
                    break

        final_cost = sum_token_cost(condition_check_cost.token_cost, invoice_extraction_cost.token_cost)

        output = TaskResponse(
            output=condition_response,
            token_cost = final_cost,
            time_required=time.time()-st,
            extracted_invoice_data=invoice_extraction_response,
            final_invoice_result=final_invoice_result,
            provided_conditions=input_data.conditions
        )
        invoice_db.add_invoice(output.model_dump())
        return JSONResponse(output.model_dump())
    except Exception as error:
        output = TaskResponse(error=str(error.args))
        return JSONResponse(output.model_dump(), status_code=500)


@app.get("/dashboard_data")
def extract_data():
    try:
        return invoice_db.get_dashboard_data()
    except Exception as error:
        output = TaskResponse(error=str(error.args))
        return JSONResponse(output.model_dump(), status_code=500)
    
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=9000,
        workers=1,
    )




# @app.post("/extract_po_data")
# def extract_data(input_data: LLMAPIInput):
#     st = time.time()
#     llm_input = LLMInput(
#         llm = input_data.llm,
#         llm_model=input_data.llm_model,
#         history=[History(
#             role="user",
#             content=Content(
#                 text="Please extract po details from given data. While extracting information, if invoice language is not in English, you must make sure that  you translate the details in English.  While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention None for any extracting parameter.",
#                 image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
#             )
#         )],
#         function_call_list=[copy.deepcopy(purchase_order_extraction_schema)]
#     )
#     response, cost = llm_list[input_data.llm].generate_response(llm_input)
#     PODate = response["PO_Date"] if response["PO_Date"] is not None else 'Unknown'
#     PO_number = response["PO_number"] if response["PO_number"] is not None else 'Unknown'
#     Vendor_name = response["Vendor_name"] if response["Vendor_name"] is not None else 'Unknown Vendor'
#     Vendor_address = response["Vendor_Address"] if response["Vendor_Address"] is not None else 'Unknown Address'
#     Vendor_contact = response["Vendor_Contact"] if response["Vendor_Contact"] is not None else 'No Contact'
#     SKU_Code = response["SKU_Code"] if response["SKU_Code"] is not None else 'No SKU'
#     SKU_Desc = response["SKU_Desc"] if response["SKU_Desc"] is not None else 'No Description'
#     Quantity = response["Quantity"] if response["Quantity"] is not None else 0
#     price_per_pack = response["price_per_pack"] if response["price_per_pack"] is not None else 0.0
#     Currency_Code = response["Currency_Code"] if response["Currency_Code"] is not None else 'Unknown Currency'
#     price_per_L_or_Kg = response["Price_AED_per_L_or_Kg"] if response["Price_AED_per_L_or_Kg"] is not None else 'Unknown'
#     Price_VAT_Included = response["Price_Incl_VAT_AED_per_pack"] if response["Price_Incl_VAT_AED_per_pack"] is not None else False
#     Tax_percent = response["VAT_percent"] if response["VAT_percent"] is not None else 0
#     AuthorizedBy = response["AuthorizedBy"] if response["AuthorizedBy"] is not None else 'Unknown Authorizer'
#     Special_Instructions = response["Special_Instructions_Comments"] if response["Special_Instructions_Comments"] is not None else 'No Special Instructions'

#     add_purchase_order(PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions)
#     output = TaskResponse(
#         output=response,
#         token_cost = cost.token_cost,
#         time_required=time.time()-st,
#         invoice_url=input_data.invoice_url
#     )

#     return JSONResponse(output.model_dump())


# @app.post("/identify_invoice")
# def extract_data(input_data: LLMAPIInput):
#     st = time.time()
#     llm_input = LLMInput(
#         llm = input_data.llm,
#         llm_model=input_data.llm_model,
#         history=[History(
#             role="user",
#             content=Content(
#                 text="Please extract the invoice type. While extracting information, You must not make up any information by yourself. If you think that, given details are missing, you could mention false for any extracting parameter.",
#                 image_data=[ImageData(url=img) for img in url_to_pil_image(input_data.invoice_url)]
#             )
#         )],
#         function_call_list=[copy.deepcopy(invoice_type_schema)]
#     )
#     response, cost = llm_list[input_data.llm].generate_response(llm_input)

#     output = TaskResponse(
#         output=response,
#         token_cost = cost.token_cost,
#         time_required=time.time()-st,
#         invoice_url=input_data.invoice_url
#     )

#     return JSONResponse(output.model_dump())


# @app.post("/validate_incoice_number")
# def extract_data(input_data: LLMAPIInputValidate):
#     st = time.time()
#     llm_input = LLMInput(
#         llm = input_data.llm,
#         llm_model=input_data.llm_model,
#         history=[History(
#             role="user",
#             content=Content(
#                 text=f"We have a vendor table with columns as (VendorName,VendorType,Address,Currency,TaxDetails,BankName,BranchName,BankAccount,BankSwiftCode), a purchaseorder table with columns as (PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions) and a invoice table with columns as (InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN). Now we want to convert all the below conditions mentioned in english into a where condition based on sqlite syntax(SQL dialect) without the term where. The conditions are: invoice number->{input_data.invoice_number} condition1->{input_data.condition1},condition2->{input_data.condition2},condition3->{input_data.condition3},condition4->{input_data.condition4},condition5->{input_data.condition5},condition6->{input_data.condition6}"
#                 #conditions_data=[input_data.invoice_number,input_data.condition1,input_data.condition2,input_data.condition3,input_data.condition4,input_data.condition5,input_data.condition6]
#             )
#         )],
#         function_call_list=[copy.deepcopy(validate_incoice_conditions_schema)]
#     )
#     response, cost = llm_list[input_data.llm].generate_response(llm_input)
    
#     condition_checks={}
#     condition_checks['vendor_address_check']=cc.check_vendor_address(input_data.invoice_url,response["condition1"])
#     condition_checks['invoice_currency_check']=cc.check_currency(input_data.invoice_url,response["condition2"])
#     condition_checks['invoice_tax_check']=cc.check_tax_details(input_data.invoice_url,response["condition3"])
#     condition_checks['invoice_gross_amount_check']=cc.check_amount(input_data.invoice_url,response["condition4"])
#     condition_checks['invoice_taxable_amount_check']=cc.check_taxable_amount(input_data.invoice_url,response["condition5"])
#     condition_checks['invoice_payment_details_check']=cc.check_payment_details(input_data.invoice_url,response["condition6"])
#     output = TaskResponse(
#         output=response,
#         token_cost = cost.token_cost,
#         time_required=time.time()-st,
#         invoice_number=input_data.invoice_number,
#         condition_checks=condition_checks
#     )

#     return JSONResponse(output.model_dump())


