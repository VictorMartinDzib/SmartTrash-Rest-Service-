''' author: Victor Alejandro Martin Dzib '''
#import environment
#from api import app
#from flask_pymongo import PyMongo

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Servicio para el monitoreo de basureros inteligentes'

#if __name__ == '__main__':
    #app.run()
    #app.run(debug=environment.setup['debug'], port=environment.setup['port'])

    
