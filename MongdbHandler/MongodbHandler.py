import pymongo
from LogHandler.MailHandler import MailHandler


class MongodbHandler(MailHandler):
    def __init__(self):
        MailHandler.__init__(self)
        self.host = self.get_config_value('mongodb', 'host')
        self.port = self.get_config_value('mongodb', 'port')

        self.database_name = self.get_config_value('mongodb', 'database_name')
        self.precision_collection_name = self.get_config_value('mongodb', 'precision_collection_name')
        self.keep_balance_collection_name = self.get_config_value('mongodb', 'keep_balance_collection_name')
        self.lock_collection_name = self.get_config_value('mongodb', 'lock_collection_name')

        self.client = pymongo.MongoClient(f'mongodb://{self.host}:{self.port}/')
        self.mongo_database = self.client[self.database_name]
        self.precision_collection = self.mongo_database[self.precision_collection_name]
        self.keep_balance_collection = self.mongo_database[self.keep_balance_collection_name]
        self.lock_collection = self.mongo_database[self.lock_collection_name]
