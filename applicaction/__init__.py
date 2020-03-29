''' author: Victor Alejandro Martin Dzib '''
#import environment
#from api import app
#from flask_pymongo import PyMongo

from flask import Flask
from flask_restful import Api
from flask_pymongo import  PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://"+ database['host'] +":"+str(database['port']) +"/" + database['dbname']
api = Api(app)
mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Servicio para el monitoreo de basureros inteligentes, estoy cambiando esto alv'

#if __name__ == '__main__':
    #app.run()
    #app.run(debug=environment.setup['debug'], port=environment.setup['port'])

    
