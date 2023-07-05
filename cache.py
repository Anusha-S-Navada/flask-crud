from __future__ import print_function
from __future__ import absolute_import
from builtins import object
from pymongo import MongoClient
from database import DatabaseAPI
import time


class CacheAPI(object):

    def __init__(self, db):
        self.db = db
        super(CacheAPI, self).__init__()

    def get(self, collection, keyValues, projection=None):
        return self.db.dbGet(collection, keyValues, projection)

    def getone(self, collection, keyValues, projection=None):
        return self.db.dbGetOne(collection, keyValues, projection)

    def add(self, collection, keyValues, primaryKey):
        return self.db.dbInsert(collection, keyValues, primaryKey)

    def updateWithPull(self, collection, keyValues, pullValues, primaryKey):
        return self.db.dbUpdateWithPull(collection, keyValues, pullValues, primaryKey)

    def deleteone(self, collection, keyValues):
        return self.db.dbDeleteOne(collection, keyValues)
