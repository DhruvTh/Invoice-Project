from Schemas import LLMModels, LLMModelCostConfig

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



invoice_header_extraction_tool = {
  "type": "function",
  "function": {
    "name": "extract_invoice_header",
    "description": "Extracts header information from an invoice.",
    "parameters": {
      "type": "object",
      "properties": {
        "invoice_number": {
          "type": "string",
          "description": "The unique identifier for the invoice"
        },
        "invoice_date": {
          "type": "string",
          "description": "The date the invoice was issued"
        },
        "due_date": {
          "type": "string",
          "description": "The date by which the payment is due"
        },
        "purchase_order_number": {
          "type": "string",
          "description": "The purchase order number associated with the invoice, if applicable"
        },
        "payment_terms": {
          "type": "string",
          "description": "The terms of payment, e.g., 'Net 30', '2% 10 Net 30'"
        }
      },
      "required": ["invoice_number", "invoice_date", "due_date", "purchase_order_number", "payment_terms"]
    }
  }
}

header_extraction_prompt = "Please extract the header information from given invoice image for further processing"

invoice_vendor_information_tool = {
  "type": "function",
  "function": {
    "name": "extract_vendor_info",
    "description": "Extracts vendor information from an invoice.",
    "parameters": {
      "type": "object",
      "properties": {
        "vendor_name": {
          "type": "string",
          "description": "The name of the vendor issuing the invoice"
        },
        "vendor_id": {
          "type": "string",
          "description": "The unique identifier for the vendor, if available"
        },
        "vendor_address": {
          "type": "string",
          "description": "The mailing address of the vendor"
        },
        "vendor_contact_information": {
          "type": "string",
          "description": "The vendor's contact information, including phone and email"
        },
        "vendor_tax_id": {
          "type": "string",
          "description": "The vendor's tax ID or VAT number"
        }
      },
      "required": ["vendor_name", "vendor_id", "vendor_address", "vendor_contact_information", "vendor_tax_id"]
    }
  }
}

vendor_extraction_prompt = "Please extract the vendor information from given invoice image for further processing"

invoice_client_information_tool = {
  "type": "function",
  "function": {
    "name": "extract_client_info",
    "description": "Extracts client information from an invoice.",
    "parameters": {
      "type": "object",
      "properties": {
        "client_name": {
          "type": "string",
          "description": "The name of the client or company being invoiced"
        },
        "client_address": {
          "type": "string",
          "description": "The mailing address of the client or company"
        },
        "client_tax_id": {
          "type": "string",
          "description": "The client's tax ID or VAT number, if listed"
        }
      },
      "required": ["client_name", "client_address", "client_tax_id"]
    }
  }
}

client_extraction_prompt = "Please extract the client information from given invoice image for further processing"


invoice_financial_information_tool = {
  "type": "function",
  "function": {
    "name": "extract_financial_info",
    "description": "Extracts financial information from an invoice.",
    "parameters": {
      "type": "object",
      "properties": {
        "subtotal": {
          "type": "string",
          "description": "The subtotal amount before taxes and discounts"
        },
        "discount_amount": {
          "type": "string",
          "description": "The amount of any discount applied"
        },
        "tax_amounts": {
          "type": "string",
          "description": "The tax amounts, broken down by tax type if multiple taxes apply"
        },
        "shipping_charges": {
          "type": "string",
          "description": "Any shipping or freight charges, if applicable"
        },
        "total_amount_due": {
          "type": "string",
          "description": "The total amount due on the invoice"
        },
        "currency": {
          "type": "string",
          "description": "The currency in which the invoice is issued"
        }
      },
      "required": ["subtotal", "discount_amount", "tax_amounts", "shipping_charges", "total_amount_due", "currency"]
    }
  }
}

financial_extraction_prompt = "Please extract the financial information from given invoice image for further processing"


invoice_item_details_tool = {
  "type": "function",
  "function": {
    "name": "extract_line_item_details",
    "description": "Extracts line item details from an invoice.",
    "parameters": {
      "type": "object",
      "properties": {
        "item_description": {
          "type": "string",
          "description": "Description of the item or service being invoiced"
        },
        "quantity": {
          "type": "string",
          "description": "The quantity of the item or service"
        },
        "unit_price": {
          "type": "string",
          "description": "The price per unit of the item or service"
        },
        "total_price": {
          "type": "string",
          "description": "The total price for the item or service"
        },
        "item_code": {
          "type": "string",
          "description": "The item code or SKU, if available"
        },
        "unit_of_measure": {
          "type": "string",
          "description": "The unit of measure for the item or service, e.g., hours, pieces, kg"
        }
      },
      "required": ["item_description", "quantity", "unit_price", "total_price", "item_code", "unit_of_measure"]
    }
  }
}

item_details_extraction_prompt = "Please extract the item information from given invoice image for further processing"

invoice_extraction_schema = {
  "type": "function",
  "function": {
  "name": "extract_invoice_data",
  "description": "Extracts detailed information from an invoice. While extracting information, if it is not in english, you must make sure that  you translate the details in english.",
  "parameters": {
    "type": "object",
    "properties": {
      "invoice_number": {
        "type": "string",
        "description": "The unique invoice number or ID of the invoice. It might be given on the top and provide complete invoice ID. If given details is not in English, please translate the details while extracting "
      },
      "invoice_date": {
        "type": "string",
        "description": "The date when the invoice was issued, in YYYY-MM-DD format. If given details is not in English, please translate the details while extracting "
      },
      "customer_details": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Full name of the customer or company. If given details is not in English, please translate the details while extracting "
          },
          "address": {
            "type": "string",
            "description": "Complete address of the customer. If given details is not in English, please translate the details while extracting "
          },
          "tax_registration_number": {
            "type": "string",
            "description": "Tax registration number of the customer. If given details is not in English, please translate the details while extracting "
          }
        },
        "required": ["name", "address", "tax_registration_number"]
      },
      "item_details": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "serial_number": {
              "type": "string",
              "description": "Serial number or unique identifier for the item. If given details is not in English, please translate the details while extracting "
            },
            "name_and_description": {
              "type": "string",
              "description": "Name and description of the item or service. If given details is not in English, please translate the details while extracting "
            },
            "time_period": {
              "type": "string",
              "description": "Time period of the transaction or service. If given details is not in English, please translate the details while extracting "
            },
            "per_month_with_fuel": {
              "type": "number",
              "description": "Cost per month including fuel, if applicable. If given details is not in English, please translate the details while extracting "
            },
            "tax_details": {
              "type": "string",
              "description": "Details of taxes applied to this item. If given details is not in English, please translate the details while extracting "
            },
            "unit_total": {
              "type": "number",
              "description": "Total cost for this item or unit. If given details is not in English, please translate the details while extracting "
            },
            "currency":{
                "type": "string",
                "description": "Details of 3 digit Currency Unit such as INR, USD, EUR."
            }
          },
          "required": ["serial_number", "name_and_description", "time_period", "per_month_with_fuel", "tax_details", "unit_total"]
        }
      },
      "grand_total": {
        "type": "number",
        "description": "The grand total amount of the invoice. If given details is not in English, please translate the details while extracting "
      },
      "payment_details": {
        "type": "object",
        "properties": {
          "payment_mode": {
            "type": "string",
            "description": "Mode of payment (e.g., bank transfer, cash, check). If given details is not in English, please translate the details while extracting "
          },
          "bank_name": {
            "type": "string",
            "description": "Name of the bank for the payment. If given details is not in English, please translate the details while extracting "
          },
          "account_name": {
            "type": "string",
            "description": "Name of the account holder. If given details is not in English, please translate the details while extracting "
          },
          "iban": {
            "type": "string",
            "description": "International Bank Account Number. If given details is not in English, please translate the details while extracting "
          },
          "tax_registration_number": {
            "type": "string",
            "description": "Tax registration number associated with the payment account. If given details is not in English, please translate the details while extracting "
          }
        },
        "required": ["payment_mode", "bank_name", "account_name", "iban", "tax_registration_number"]
      }
    },
    "required": ["reference_number", "invoice_date", "customer_details", "item_details", "grand_total", "payment_details"]
  }
}
}

invoice_type_schema = {
  "type": "function",
  "function": {
    "name": "identify_invoice_type",
    "description": "Identify the type of invoice and return true or false for each type.",
    "parameters": {
      "type": "object",
      "properties": {
        "is_proforma_invoice": {
          "type": "boolean",
          "description": "True if the invoice is a Proforma invoice, otherwise false."
        },
        "is_interim_invoice": {
          "type": "boolean",
          "description": "True if the invoice is an Interim invoice, otherwise false."
        },
        "is_normal_invoice": {
          "type": "boolean",
          "description": "True if the invoice is a normal invoice, otherwise false."
        }
      },
      "required": ["is_proforma_invoice", "is_interim_invoice", "is_final_invoice"]
    }
  }
}

#Todo : for currently add the document type, later on try to check if we could check the invoice type, Based on the invoice type we need to only extract data for invoice, not for proforma
#Todo : add examples in function calling whenver possible. For example, add examples for invoice id.

#Todo : Try to convert the araabic into the english while extracting the data
#Todo : Try to check for the handwritten invoicess' accuracy.