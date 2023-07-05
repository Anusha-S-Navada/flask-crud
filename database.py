from builtins import str
from builtins import object
from pymongo import MongoClient


class DatabaseAPI(object):

    def __init__(self, uri):
        self.dbclient = MongoClient(uri)
        self.usersDb = self.dbclient.users
        super(DatabaseAPI, self).__init__()

    def dbInsert(self, collection, keyValues, primaryKey):
        try:
            result = self.usersDb[collection].insert_one(keyValues)
        except Exception as e:
            return None
        return result

    def dbUpdateWithPull(self, collection, keyValues, pullValues, primaryKey):
        try:
            # result = self.usersDb[collection].save(keyValues)
            result = self.usersDb[collection].update(keyValues, pullValues)
        except Exception as e:
            # app.logger.error('Failed to add to table ' + primaryKey + ' ' + str(repr(e)))
            return False
        return True

    def dbGet(self, collection, keyValues, projection):
        try:
            if any(keyValues):
                result = self.usersDb[collection].find(keyValues, projection=projection)
            else:
                result = self.usersDb[collection].find(projection=projection)
        except Exception as e:
            return None
        return result

    def dbGetOne(self, collection, keyValues, projection):
        try:
            if any(keyValues):
                result = self.usersDb[collection].find_one(filter=keyValues, projection=projection)
            else:
                result = self.usersDb[collection].find_one(projection=projection)
        except Exception as e:
            return None
        return result

    def dbDeleteOne(self, collection, keyValues):
        try:
            result = self.usersDb[collection].delete_one(keyValues)
        except Exception as e:
            return None
        return result
