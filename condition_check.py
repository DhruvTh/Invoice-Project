#Test the preparation of Constant.py on the go

import sqlite3

def check_vendor_name(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT "Success" FROM invoice where InvoiceNumber={InvoiceNumber} and PaymentCompany in (select VendorName from Vendor)')
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failed'
    finally:
        conn.close()

def check_vendor_name(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT "Success" FROM invoice where InvoiceNumber={InvoiceNumber} and PaymentCompany in (select VendorName from Vendor)')
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_vendor_address(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" FROM invoice i
                        join Vendor v
                        on i.PaymentCompany =v.VendorName
                        and i.PaymentAddress =v.Address
                        where InvoiceNumber={InvoiceNumber} ''')
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_currency(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice i
                        join vendor v
                        on i.PaymentCompany =v.VendorName
                        and i.PaymentCurrency =v.Currency
                        join PurchaseOrder po
                        on SUBSTR(i.PONumber, 1, INSTR(i.PONumber, "-") - 1)=po.PO_number
                        and i.PaymentCurrency =po.Currency_Code
                        where InvoiceNumber={InvoiceNumber} '''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_tax_details(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice i
                        join vendor v
                        on i.PaymentCompany =v.VendorName
                        and i.CompanyTRN =v.TaxDetails
                        where InvoiceNumber={InvoiceNumber} '''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_amount(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice i
                        where InvoiceNumber={InvoiceNumber} 
                        and ItemGrossAmountPayable=ItemTaxableAmount*(1+(ItemTaxRate/100.0))
                        '''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_taxable_amount(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice i
                        where InvoiceNumber={InvoiceNumber} 
                        and ItemTaxAmount=ItemTaxableAmount*(ItemTaxRate/100.0)
                        '''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_payment_details(InvoiceNumber):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice i
                        join vendor v
                        on i.PaymentCompany =v.VendorName
                        and i.PaymentBankName =v.BankName
                        and i.PaymentAccount =v.BankAccount
                        where InvoiceNumber={InvoiceNumber} '''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

def check_where_condition(InvoiceNumber, where_cond):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'''SELECT "Success" 
                        FROM invoice 
                        join vendor 
                        on invoice.PaymentCompany =vendor.VendorName
                        join PurchaseOrder 
                        on SUBSTR(invoice.PONumber, 1, INSTR(invoice.PONumber, "-") - 1)=PurchaseOrder.PO_number
                        where InvoiceNumber={InvoiceNumber} 
                        and {where_cond}'''
                        )
        for row in cursor.fetchall():
            if row[0]:
                return row[0]
        return 'Failure'
    finally:
        conn.close()

# Example Usage
if __name__ == "__main__":
    #C
    print(f"Vendor name check is a {check_vendor_name(9000414225)}")
    print(f"Vendor address check is a {check_vendor_address(9000414225)}")
    print(f"Invoice currency check is a {check_currency(9000414225)}")
    print(f"Invoice tax check is a {check_tax_details(9000414225)}")
    print(f"Invoice gross amount check is a {check_amount(9000414225)}")
    print(f"Invoice taxable amount check is a {check_taxable_amount(9000414225)}")
    print(f"Invoice payment details check is a {check_payment_details(9000414225)}")
    print(f"Invoice condition-1 check is a {check_where_condition(9000414225,'ItemGrossAmountPayable > 1000')}")
    print(f"Invoice condition-2 check is a {check_where_condition(9000414225,'ItemGrossAmountPayable < 1000')}")
    print(f"Invoice condition-3 check is a {check_where_condition(9000414225,'currency = "USD"')}")
    print(f"Invoice condition-4 check is a {check_where_condition(9000414225,'currency = "AED"')}")
    print(f"Invoice condition-5 check is a {check_where_condition(9000414225,'ItemTaxRate = 5')}")
