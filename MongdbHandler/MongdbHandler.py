import pymongo
from LogHandler.LogHandler import LogHandler


class MongodbHandler(LogHandler):
    def __init__(self):
        self.host = self.get_config_value('mongodb', 'host')
        self.port = self.get_config_value('mongodb', 'port')
        self.database_name = self.get_config_value('mongodb', 'database')
        self.collection_name = self.get_config_value('mongodb', 'collection')
        self.client = pymongo.MongoClient(f'mongodb://{self.host}:{self.port}/')
        self.mongo_database = self.client[self.database_name]
        self.mongo_collection = self.mongo_database[self.collection_name]
