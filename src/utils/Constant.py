from pydantic import BaseModel

class LLMModelCostConfig(BaseModel):
    input_cost_per_token: float
    output_cost_per_token: float
    image_supported: bool = False
    image_cost_per_token: float = 0


class LLMModels(BaseModel):
    mistral_ai: str = "MistralAI"
    mistral_small: str = "open-mixtral-8x7b"
    mistral_large: str = "mistral-large-latest"
    mistral_mini : str = "open-mistral-7b"	
    gemini_ai: str = "GeminiAI"
    gemini_pro: str = "gemini-pro"
    gemini_pro_vision: str = "gemini-pro-vision"
    gemini_15_pro : str = "gemini-1.5-pro-001"
    gemini_15_flash : str = "gemini-1.5-flash-001"
    open_ai: str = "OpenAI"
    gpt_4_0125_latest: str = "gpt-4-turbo-2024-04-09"
    gpt_4o_2024_05_13: str = "gpt-4o-2024-05-13"
    chatgpt_4o_latest: str = "gpt-4o-2024-08-06"		
    gpt_35_turbo_0125: str = "gpt-3.5-turbo-0125"
    gpt_4o_mini : str = "gpt-4o-mini"
    claude_3_haiku : str = "claude-3-haiku-20240307"
    claude_3_sonnet : str = "claude-3-sonnet-20240229"
    claude_3_opus : str = "claude-3-opus-20240229"
    claude_35_sonnet : str = "claude-3-5-sonnet-20240620"
    claude_ai : str = "ClaudeAI"
    codestral_latest : str = "codestral-latest"
    llamaai : str = "LLamaAI"
    llama3_405b_instruct : str = "meta/llama3-405b-instruct-maas"
    vertexmistralai : str = "VertexMistralAI"
    mistral_large_2407 : str = "mistral-large@2407"
    codestral_2405 : str = "codestral@2405"
    groqai : str = "GroqAI"
    llama_31_70b_versatile : str = "llama-3.1-70b-versatile"
    llama_31_8b_instant : str = "llama-3.1-8b-instant"

INVALID_ROLE_TYPE_ERROR_MSG = "Invalid role"

llm_models = LLMModels()
llm_model_list = {
    llm_models.mistral_ai: {
        llm_models.mistral_mini: LLMModelCostConfig(
            input_cost_per_token=0.00000025,
            output_cost_per_token=0.00000025,
            image_supported=False,
        )
    },
    llm_models.gemini_ai: {
        llm_models.gemini_15_pro: LLMModelCostConfig(
            input_cost_per_token=0.000007,
            output_cost_per_token=0.000021, 
            image_supported=True,
            image_cost_per_token=0.0,
        ),
        llm_models.gemini_15_flash : LLMModelCostConfig(
            input_cost_per_token=0.00000015,
            output_cost_per_token=0.0000006, 
            image_supported=True,
            image_cost_per_token=0.0,
        )
    },
    llm_models.open_ai: {
        llm_models.gpt_4o_mini : LLMModelCostConfig(
            input_cost_per_token=0.00000015,
            output_cost_per_token=0.0000006,
            image_supported=True,
            image_cost_per_token=0.00000015
        ),
        llm_models.chatgpt_4o_latest : LLMModelCostConfig(
            input_cost_per_token=0.0000025,
            output_cost_per_token=0.00001,
            image_supported=True,
            image_cost_per_token=0.0000025
        )
    },   
    llm_models.claude_ai: {
        llm_models.claude_3_haiku: LLMModelCostConfig(
            input_cost_per_token=0.00000025,
            output_cost_per_token=0.00000125,
            image_supported=False
        ),
        llm_models.claude_3_opus: LLMModelCostConfig(
            input_cost_per_token=0.000015,
            output_cost_per_token=0.000075,
            image_supported=True,
            image_cost_per_token=0
        ),
        llm_models.claude_35_sonnet : LLMModelCostConfig(
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000015,
            image_supported=True,
            image_cost_per_token=0
        )
    },
    llm_models.llamaai :{
        llm_models.llama3_405b_instruct : LLMModelCostConfig(
            input_cost_per_token=0.000001,
            output_cost_per_token=0.000001,
            image_supported=False,
        )
    },
    llm_models.groqai : {
        llm_models.llama_31_70b_versatile :  LLMModelCostConfig(
            input_cost_per_token=0.00000089,
            output_cost_per_token=0.00000089,
            image_supported=False
        ),
        llm_models.llama_31_8b_instant : LLMModelCostConfig(
            input_cost_per_token=0.00000089,
            output_cost_per_token=0.00000089,
            image_supported=False
        )
    },
    llm_models.vertexmistralai: {
        llm_models.mistral_large_2407: LLMModelCostConfig(
            input_cost_per_token=0.000003,
            output_cost_per_token=0.000009,
            image_supported=False,
        ),
        llm_models.codestral_2405: LLMModelCostConfig(
            input_cost_per_token=0.000001,
            output_cost_per_token=0.000003,
            image_supported=False,
        )
    }
}


invoice_extraction_schema = {
  "type": "function",
  "function": {
    "name": "extract_invoice_data",
    "description": "Extracts detailed information from an invoice. While extracting information, if it is not in English, you must make sure that you translate the details into English.",
    "parameters": {
      "type": "object",
      "properties": {
        "invoice_number": {
          "type": "string",
          "description": "The unique invoice number or ID of the invoice. It might be given on the top and provide complete invoice ID. If given details are not in English, please translate the details while extracting."
        },
        "invoice_date": {
          "type": "string",
          "description": "The date when the invoice was issued, in YYYY-MM-DD format. If given details are not in English, please translate the details while extracting."
        },
        "due_date": {
          "type": "string",
          "description": "The due date for payment of the invoice, in YYYY-MM-DD format. If given details are not in English, please translate the details while extracting."
        },
        "po_number": {
          "type": "string",
          "description": "The unique purchase order number. If given details are not in English, please translate the details while extracting."
        },
        "customer_details": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Full name of the customer or company. If given details are not in English, please translate the details while extracting."
            },
            "address": {
              "type": "string",
              "description": "Complete address of the customer. If given details are not in English, please translate the details while extracting."
            },
            "tax_registration_number": {
              "type": "string",
              "description": "Tax registration number of the customer. If given details are not in English, please translate the details while extracting."
            }
          },
          "required": ["name", "address", "tax_registration_number"]
        },
        "vendor_details": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Full name of the vendor or company. If given details are not in English, please translate the details while extracting."
            },
            "address": {
              "type": "string",
              "description": "Complete address of the vendor. If given details are not in English, please translate the details while extracting."
            },
            "tax_registration_number": {
              "type": "string",
              "description": "Tax registration number of the vendor. If given details are not in English, please translate the details while extracting."
            }
          },
          "required": ["name", "address", "tax_registration_number"]
        },
        "grand_total": {
          "type": "number",
          "description": "The grand total amount of the invoice. If given details are not in English, please translate the details while extracting."
        },
        "currency": {
          "type": "string",
          "description": "Provide the country code for currency used in this Invoice. If given details are not in English, please translate the details while extracting."
        },
        "tax_percentage": {
          "type": "string",
          "description": "Provide the percentage of tax applied over base amount. Value could be 5%, 10%, 18%, or any other percentage number. If given details are not in English, please translate the details while extracting."
        }
      },
      "required": ["invoice_number", "invoice_date", "due_date", "po_number", "customer_details", "vendor_details", "grand_total", "tax_percentage", "currency"]
    }
  }
}


po_extraction_schema = {
  "type": "function",
  "function": {
    "name": "extract_po_data",
    "description": "Extracts detailed information from a Purchase Order. While extracting information, if it is not in English, you must make sure that you translate the details into English.",
    "parameters": {
      "type": "object",
      "properties": {
        "po_number": {
          "type": "string",
          "description": "The unique Purchase Order number or ID. It might be given on the top and provide complete PO ID. If given details are not in English, please translate the details while extracting."
        },
        "po_date": {
          "type": "string",
          "description": "The date when the Purchase Order was issued, in YYYY-MM-DD format. If given details are not in English, please translate the details while extracting."
        },
        "due_date": {
          "type": "string",
          "description": "The due date for fulfillment of the Purchase Order, in YYYY-MM-DD format. If given details are not in English, please translate the details while extracting."
        },
        "related_invoice_number": {
          "type": "string",
          "description": "The unique invoice number related to this Purchase Order. If given details are not in English, please translate the details while extracting."
        },
        "customer_details": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Full name of the customer or company. If given details are not in English, please translate the details while extracting."
            },
            "address": {
              "type": "string",
              "description": "Complete address of the customer. If given details are not in English, please translate the details while extracting."
            },
            "tax_registration_number": {
              "type": "string",
              "description": "Tax registration number of the customer. If given details are not in English, please translate the details while extracting."
            }
          },
          "required": ["name", "address", "tax_registration_number"]
        },
        "vendor_details": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "Full name of the vendor or company. If given details are not in English, please translate the details while extracting."
            },
            "address": {
              "type": "string",
              "description": "Complete address of the vendor. If given details are not in English, please translate the details while extracting."
            },
            "tax_registration_number": {
              "type": "string",
              "description": "Tax registration number of the vendor. If given details are not in English, please translate the details while extracting."
            }
          },
          "required": ["name", "address", "tax_registration_number"]
        },
        "grand_total": {
          "type": "number",
          "description": "The grand total amount of the Purchase Order. If given details are not in English, please translate the details while extracting."
        },
        "currency": {
          "type": "string",
          "description": "Provide the country code for currency used in this Purchase Order. If given details are not in English, please translate the details while extracting."
        },
        "tax_percentage": {
          "type": "string",
          "description": "Provide the percentage of tax applied over base amount. Value could be 5%, 10%, 18%, or any other percentage number. If given details are not in English, please translate the details while extracting."
        }
      },
      "required": ["po_number", "po_date", "due_date", "related_invoice_number", "customer_details", "vendor_details", "grand_total", "tax_percentage", "currency"]
    }
  }
}

invoice_type_schema = {
  "type": "function",
  "function": {
    "name": "identify_invoice_type",
    "description": "Identify the type of invoice and return true or false for each type. If given document is not invoice then return false for both cases.",
    "parameters": {
      "type": "object",
      "properties": {
        "is_digital_invoice": {
          "type": "boolean",
          "description": "True if the invoice is an digital invoice, otherwise false."
        },
        "is_handwritten_invoice": {
          "type": "boolean",
          "description": "True if the invoice is a handwritten invoice, otherwise false."
        }
      },
      "required": ["is_digital_invoice", "is_handwritten_invoice"]
    }
  }
}



doc_type_schema = {
  "type": "function",
  "function": {
    "name": "identify_document_type",
    "description": "Identify the type of document and return true or false for each type. If the given document is neither a Purchase Order nor an Invoice, return false for both cases.",
    "parameters": {
      "type": "object",
      "properties": {
        "is_purchase_order": {
          "type": "boolean",
          "description": "True if the document is a Purchase Order, otherwise false."
        },
        "is_invoice": {
          "type": "boolean",
          "description": "True if the document is an Invoice, otherwise false."
        }
      },
      "required": ["is_purchase_order", "is_invoice"]
    }
  }
}

BASE_CONDITION_CHECK_SCHEMA = {
  "type": "function",
  "function": {
    "name": "check_invoice_conditions",
    "description": "Checks various conditions on invoice data to determine if it should be processed or rejected.",
    "parameters": {
      "type": "object",
      "properties": {
      },
      "required": []
    }
  }
}



BASE_CONDITIONS = [
    "True if the invoice is raised between 2023 and 2024, otherwise false.",
    "True if the invoice currency is AED, otherwise false.",
    "True if the invoice has a 5% tax rate, otherwise false.",
    "True if vendor name, tax registration number, and other details match with invoice data, otherwise false.",
    "True if the PO number in the invoice matches the given PO data, otherwise false."
]

VENDOR_DUMMY_DATA = [
  {
    "vendorName": "Barnes, Garcia & Martin",
    "typeOfVendor": "Service",
    "address": "13868 Michael Wall, North Cindytown, CT 45483 US",
    "currency": "USD",
    "taxDetails": "33123456789102Z1",
    "bankName": "BNY Mellon",
    "branchName": "City Square",
    "bankAccountNumber": "911356431",
    "bankSwiftCode": "BNMXINBXX"
  },
  {
    "vendorName": "Huff-Bryan",
    "typeOfVendor": "Transport",
    "address": "2180 Michael Ridges Apt 385, Port Lindsey, MP 98258 US",
    "currency": "",
    "taxDetails": "",
    "bankName": "Bank of America",
    "branchName": "Morish Drive",
    "bankAccountNumber": "819775634",
    "bankSwiftCode": "BANINBXYX"
  },
  {
    "vendorName": "Kirk, Murphy and Daniels",
    "typeOfVendor": "Business",
    "address": "00205 Gallegos Light, Potterstad, FM 8203 US",
    "currency": "USD",
    "taxDetails": "7935DF1125",
    "bankName": "NY Central Bank",
    "branchName": "NYC",
    "bankAccountNumber": "2298836512",
    "bankSwiftCode": "NYCINBYT"
  },
  {
    "vendorName": "EPPCO LUBRICANTS",
    "typeOfVendor": "Transport",
    "address": "P.O. Box 28577, Dubai, Unite Arab Emirates",
    "currency": "AED",
    "taxDetails": "",
    "bankName": "Emirates NBD Bank PJSC",
    "branchName": "Main Branch, Deira, Dubai",
    "bankAccountNumber": "1011022503102",
    "bankSwiftCode": "AE86026000"
  },
  {
    "vendorName": "C9 Enterprises",
    "typeOfVendor": "Material Supplier",
    "address": "1624 Timothy Mission, Markville, AK 58294 US",
    "currency": "USD",
    "taxDetails": "OG@AAMFCO376K124",
    "bankName": "Central Bank of Europe",
    "branchName": "Ref Camp",
    "bankAccountNumber": "17994867",
    "bankSwiftCode": "SBININBB250"
  }
]

#Todo : for currently add the document type, later on try to check if we could check the invoice type, Based on the invoice type we need to only extract data for invoice, not for proforma

#Todo : add examples in function calling whenver possible. For example, add examples for invoice id.

#Todo : Try to convert the araabic into the english while extracting the data

#Todo : Try to check for the handwritten invoicess' accuracy.
