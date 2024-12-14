#Test the preparation of Constant.py on the go

import sqlite3

# Establish connection to SQLite databa se (or create it if it doesn't exist)
conn = sqlite3.connect('vendor_system.db')
cursor = conn.cursor()

# Create tables for vendors, purchase orders, and invoices
def create_table_if_not_exist():
    #cursor.execute(''' DROP TABLE Vendor''')
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vendor (
            VendorID INTEGER PRIMARY KEY AUTOINCREMENT,
            VendorName TEXT NOT NULL,
            VendorType TEXT NOT NULL,
            Address TEXT NOT NULL,
            Currency TEXT NOT NULL,
            TaxDetails TEXT NOT NULL,
            BankName TEXT NOT NULL,
            BranchName TEXT NOT NULL,
            BankAccount BIGINT NOT NULL,
            BankSwiftCode TEXT NOT NULL
        )
    ''')
    #cursor.execute(''' DROP TABLE PurchaseOrder''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PurchaseOrder (
            POID INTEGER PRIMARY KEY AUTOINCREMENT,
            PODate DATE NOT NULL,
            PO_number TEXT NOT NULL,
            Vendor_name TEXT NOT NULL,
            Vendor_address TEXT NOT NULL,
            Vendor_contact TEXT NOT NULL,            
            SKU_Code TEXT NOT NULL,
            SKU_Desc TEXT NOT NULL,
            Quantity TEXT NOT NULL,
            price_per_pack REAL NOT NULL,
            Currency_Code TEXT NOT NULL,
            price_per_L_or_Kg REAL NOT NULL,
            Price_VAT_Included REAL NOT NULL,
            Tax_percent TEXT NOT NULL,
            AuthorizedBy TEXT NOT NULL,
            Special_Instructions TEXT NOT NULL
        )
    ''')
    #cursor.execute(''' DROP TABLE Invoice''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invoice (
            InvoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
            InvoiceNumber INTEGER NOT NULL,
            InvoiceDate DATE NOT NULL,
            CustomerName TEXT NOT NULL,
            CustomerAddress TEXT NOT NULL,
            CustomerTRN BIGINT NOT NULL,
            PONumber TEXT NOT NULL,
            ItemSlNo INTEGER NOT NULL,
            ItemCode TEXT NOT NULL,
            ItemDetail TEXT NOT NULL,
            ItemQuantity INTEGER NOT NULL,
            ItemDueDate DATE NOT NULL,
            ItemUnitPrice REAL NOT NULL,
            ItemTaxRate INTEGER NOT NULL,
            ItemTaxableAmount REAL NOT NULL,
            ItemTaxAmount REAL NOT NULL,
            ItemGrossAmountPayable REAL NOT NULL,
            PaymentCompany TEXT NOT NULL,
            PaymentAddress TEXT NOT NULL,
            PaymentBankName TEXT NOT NULL,
            PaymentBranchName TEXT NOT NULL,
            PaymentAccount BIGINT NOT NULL,
            PaymentIBAN TEXT NOT NULL,
            PaymentCurrency TEXT NOT NULL,
            CompanyTRN TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new vendor
def delete_table(TableName):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {TableName}')
    conn.commit()
    print(f"{TableName} deleted successfully!")
    conn.close()


# Add a new vendor
def add_vendor(VendorName,VendorType,Address,Currency,TaxDetails,BankName,BranchName,BankAccount,BankSwiftCode):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Vendor (VendorName,VendorType,Address,Currency,TaxDetails,BankName,BranchName,BankAccount,BankSwiftCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (VendorName,VendorType,Address,Currency,TaxDetails,BankName,BranchName,BankAccount,BankSwiftCode))
    conn.commit()
    print("Vendor added successfully!")
    conn.close()

# Add a new purchase order
def add_purchase_order(PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PurchaseOrder (PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (PODate,PO_number,Vendor_name,Vendor_address,Vendor_contact,SKU_Code,SKU_Desc,Quantity,price_per_pack,Currency_Code,price_per_L_or_Kg,Price_VAT_Included,Tax_percent,AuthorizedBy,Special_Instructions))
    conn.commit()
    print("Purchase order added successfully!")
    conn.close()

# Add a new invoice
def add_invoice(InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN):
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Invoice (InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (InvoiceNumber,InvoiceDate,CustomerName,CustomerAddress,CustomerTRN,PONumber,ItemSlNo,ItemCode,ItemDetail,ItemQuantity,ItemDueDate,ItemUnitPrice,ItemTaxRate,ItemTaxableAmount,ItemTaxAmount,ItemGrossAmountPayable,PaymentCompany,PaymentAddress,PaymentBankName,PaymentBranchName,PaymentAccount,PaymentIBAN,PaymentCurrency,CompanyTRN))
    conn.commit()
    print("Invoice added successfully!")
    conn.close()
    

# Display all records
def view_records():
    conn = sqlite3.connect('vendor_system.db')
    cursor = conn.cursor()
    print("\nVendors:")
    cursor.execute('SELECT * FROM Vendor')
    for row in cursor.fetchall():
        print(row)

    print("\nPurchase Orders:")
    cursor.execute('SELECT * FROM PurchaseOrder')
    for row in cursor.fetchall():
        print(row)

    print("\nInvoices:")
    cursor.execute('SELECT * FROM Invoice')
    for row in cursor.fetchall():
        print(row)

    conn.close()


# Example Usage
if __name__ == "__main__":
    create_table_if_not_exist()

    #delete tables
    #delete_table('Vendor')
    #delete_table('PurchaseOrder')
    #delete_table('Invoice')

    # Add sample data
    #add_vendor("C9 Enterprises","Material Supplier","1624 Timothy Mission, Markville, AK 58294 US","USD","OG@AAMFCO376K124","Central Bank of Europe","Ref Camp","17994867","SBININBB250")
    #add_vendor("Barnes, Garcia & Martin","Service","13868 Michael Wall, North Cindytown, CT 45483 US","USD","33123456789102Z1","BNY Mellon ","City Square","911356431","BNMXINBXX")
    #add_vendor("Kirk, Murphy and Daniels","Business","00205 Gallegos Light, Potterstad, FM 8203 US","USD","7935DF1125","NY Central Bank","NYC","2298836512","NYCINBYT")
    #add_vendor("Huff-Bryan","Transport ","2180 Michael Ridges Apt 385, Port Lindsey, MP 98258 US","","","Bank of America","Morish Drive","819775634","BANINBXYX")
    #add_vendor("EPPCO LUBRICANTS","Transport ","P.O. Box 28577, Dubai, Unite Arab Emirates","AED","","Emirates NBD Bank PJSC","Main Branch, Deira, Dubai","1011022503102","AE86026000")

    #add_purchase_order("2023-04-11","MXU111","EPPCO Lubricants(BR) EPPCO Projects Co. LLC","P.O. Box 28577, Dubai, Unite Arab Emirates","043133700","500574-012","DELO GOLD ULTRA SAE 15W-40 (20 L PAIL)","25","175","AED","8.75","4375","5","Rajendra Amilineni","90 days from date of delivery, Credit Limit: AED 30K, Account # 1001098874 Moxey Tech Limited")

    #add_invoice("9000414225","2023-04-19","MOXEY TECH LIMITED","14TH FLOOR,AL MARYAH ISLAND,ABU DHABI,Abu Dhabi,United Arab Emirates","100562096600003","MXU111-MAFRAQ-0581003652","1","500574-012","DELO GOLD ULTRA SAE 15W-40 (20 L PAIL)","25","2023-07-18","175","5","4375.00","218.75","4593.75","EPPCO LUBRICANTS","P.O. Box 28577, Dubai, Unite Arab Emirates","Emirates NBD Bank PJSC","Main Branch, Deira, Dubai","1011022503102","AE860260001011022503102","AED","100002726600003")


    #executed oher query
    #cursor.execute('UPDATE Vendor set TaxDetails="100002726600003" where vendorId=21;')
    #cursor.execute('commit;')

    # View all records
    view_records()


    # Close the database connection
    conn.close()

