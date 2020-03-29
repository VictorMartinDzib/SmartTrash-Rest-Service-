from api import app
from environment import database

app.config["MONGO_URI"] = "mongodb://"+ database['host'] +":"+database['port'] +"/" + database['dbname']

mongo = PyMongo(app)