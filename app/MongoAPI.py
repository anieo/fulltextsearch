import os
from pymongo import MongoClient
import urllib.parse
from databases import DatabaseURL
from pymongo.common import TIMEOUT_OPTIONS
class MongoAPI:
    def __init__(self, data):
        #TODO take from envriroment variables
        # conn="mongodb://{user}:{password}@{host}:{port}/default_db?authSource=admin"

        user=os.environ['DB_USER']
        password=os.environ['DB_PASSWORD']
        host=os.environ['DAT_HOST']
        port=os.environ['DAT_PORT']
        # mongo_uri ="mongodb://"+user+":" + password + "@"+host+":"+port+"/db?authSource=admin"
        # mongo_uri ="mongodb://asd:1234@172.17.0.1:5000"
        # mongo_uri ="mongodb://"+host+":"+port
        MONGODB_URL =str(DatabaseURL(
        f"mongodb://{user}:{password}@{host}:{port}"))
        print(MONGODB_URL)
        
        self.client = MongoClient(MONGODB_URL,serverSelectionTimeoutMS = 5000,uuidRepresentation='standard')  
        
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self,guid):
        documents = self.collection.find({'guid':guid})  
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def create(self, data):
        data['guid']=data['guid']
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(data['guid'])}

        return output ,response.acknowledged


    def delete(self, guid):
        response = self.collection.delete_one({'guid':guid})
        return response.deleted_count
        