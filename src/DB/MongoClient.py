from pymongo import MongoClient
import os
from src.utils.Constant import VENDOR_DUMMY_DATA


class InvoiceDataDB:
    def __init__(self):
        self.db_name = "Invoice-Data"
        self.invoice_collection = "Invoice-Extracted-Data"
        self.po_collection = "PO-Extracted-Data"
        self.vendor_collection = "Vendor-Data"        

    def connect_invoice_db(self):
        client = MongoClient(os.environ["MONGO_CONNECTION_STR"], serverSelectionTimeoutMS=5000) 

        available_databases = client.list_database_names()

        if(self.db_name in available_databases):
            self.db = client[self.db_name]
            available_collections = self.db.list_collection_names()
            if(not(self.invoice_collection in available_collections)):
                self.db.create_collection(self.invoice_collection)
            if(not(self.po_collection in available_collections)):
                self.db.create_collection(self.po_collection)
            if(not(self.vendor_collection in available_collections)):
                self.db.create_collection(self.vendor_collection)
        else:
            self.db = client[self.db_name]
            self.db.create_collection(self.invoice_collection)
            self.db.create_collection(self.po_collection)
            self.db.create_collection(self.vendor_collection)

        vendor_collection = self.db[self.vendor_collection]
        if(vendor_collection.count_documents({}) == 0):
            vendor_collection.insert_many(VENDOR_DUMMY_DATA)
        
    def get_vendor(self, tax_number : str):
        vendor_collection = self.db[self.vendor_collection]
        return vendor_collection.find_one({'taxDetails': tax_number}, {"_id": 0})
    
    def get_po(self, po_number : str):
        po_collection = self.db[self.po_collection]
        return po_collection.find_one({"po_number" : po_number}, {"_id": 0})
 
