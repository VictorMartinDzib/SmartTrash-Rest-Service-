''' author: Victor Alejandro Martin Dzib '''
from environment import setup
from api import app
#from flask_pymongo import PyMongo

if __name__ == '__main__':
    app.run(debug=setup['debug'], port=setup['port'])

    
