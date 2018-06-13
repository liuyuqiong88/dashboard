# -*- coding: utf-8 -*-

import pymongo

class MongoLinks(object):

    def __init__(self, config, collection, user=None, password=None):
        self.host = config['host']
        self.port = config['port']
        self.db = config['db']
        self.collection_name = collection
        self.user = user
        self.password = password
        self.conn = pymongo.MongoClient(host=self.host, port=self.port)

        if self.user and self.password:
            db_auth = self.conn[self.db]
            db_auth.authenticate(self.user, self.password)
            self.collection = self.conn[self.db][self.collection_name]
        else:
            self.collection = self.conn[self.db][self.collection_name]