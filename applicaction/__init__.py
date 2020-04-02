''' author: Victor Alejandro Martin Dzib '''

from applicaction.environment import setup, database
from flask_restful import Api
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://"+ database['host'] +":"+str(database['port']) +"/" + database['dbname']
mongo = PyMongo(app)


import applicaction.api

#if __name__ == '__main__':
 #     app.run()

