import logging
import asyncio, time
from pymongo import MongoClient
#from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB():
    def __init__(self):
        self.client = MongoClient(host="localhost", port=27017)
        self.logger = logging.getLogger()
        
    def insert_one(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.insert_one(data)
        except:
            print("Insert one function have errors")
    
    
    def insert_many(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]

        try:
            output = collection.insert_many(data)
        except:
            print("Insert many function have errors")
           
            
    def delete_one(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]

        try:
            output = collection.delete_one(data)
        except:
            print("Delete one function have errors")
    
    
    def delete_many(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]

        try:
            output = collection.delete_many(data)
        except:
            print("Delete many function have errors")
    
            
    def update_one(self, db_name, collection_name, old_data, new_data):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.update_one(old_data, {"$set": new_data})
        except:
            print("Update one function have errors")
            return None
    
    def update_many(self, db_name, collection_name, old_data, new_data):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.update_many(old_data, {"$set": new_data})
            return output
        except:
            print("Update many function have errors")
            return None
    
    def find_one(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.find_one(data)
            return output
        except:
            print("Find one function have errors")
            return None
    
    
    def find_many(self, db_name, collection_name, data, sort_key=None, limit=None):
        db = self.client[db_name]
        collection = db[collection_name]
        a = collection.find({}).sort("count")
        print(list(a))

        if sort_key is not None:
            if limit == None:
                output = collection.find(data).sort(sort_key)
            else:
                output = collection.find(data).sort(sort_key).limit(limit)
        else:
            if limit == None:
                output = collection.find(data)
            else:
                output = collection.find(data).limit(limit)
                
        return output

    def find(self,db_name, collection_name, sort_key=None, limit=None):
        db = self.client[db_name]
        collection = db[collection_name]
        

        if sort_key is not None:
            if limit == None:
                output = collection.find().sort(sort_key)
            else:
                output = collection.find().sort(sort_key).limit(limit)
        else:
            if limit == None:
                output = collection.find()
            else:
                output = collection.find().limit(limit)
                
        return output
    
    def count_documents(self, db_name, collection_name, data):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.count_documents(data)
            return output
        except:
            print("Count documents function have errors")
            return None
       
        
    def drop_collection(self, db_name, collection_name):
        db = self.client[db_name]
        collection = db[collection_name]
        
        try:
            output = collection.drop()
        except:
            print("Drop collection function have errors")
    
    
    def drop_database(self, db_name):
        try:
            self.client.drop_database(db_name)
        except:
            print("Drop database function have errors")
        
     
import pandas as pd
def insert_hate_data(mongo):
    dataset = pd.read_csv("all_hate.csv")
    
    text_list = list(dataset["text"])
    for i in range(len(dataset)):
        now_data = dataset.iloc[i]
        text = text_list[i]
        
        data = {
            "_id": i,
            "text": text,
            "target": "",
            "status": 0,
        }
        
        mongo.insert_one("hate_data", "hate_data", data)
    print("insert ok")

def count_info(mongo):
    mongo.drop_collection("hate_data", "hate_data")
    mongo.drop_collection("hate_data", "test_data")
    mongo.drop_collection("hate_data", "view_count")
    mongo.drop_collection("hate_data", "labeled_count")
    mongo.drop_collection("hate_data", "target_count")
    mongo.drop_collection("hate_data", "need_check_test")
    mongo.drop_collection("hate_data", "user_info")
    db = mongo.client["hate_data"]
    collection = db["view_count"]
    collection = db["labeled_count"]
    collection = db["target_count"]
    collection = db["user_info"]
    
    print("ok")


def initial(mongo):
    count_info(mongo)
    insert_hate_data(mongo)
    print("all ok")
    return


if __name__ == "__main__":
    mongo = MongoDB()
    #initial(mongo)
    #insert_hate_data(mongo)
    out = mongo.find_many("hate_data", "user_info", {})
    out = list(out)
    out = []
    print(out[-10:])