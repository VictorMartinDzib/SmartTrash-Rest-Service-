from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema
#from controllers.ResourcesController import UserWithTrashes, UserWithTrashesById, AuthenticationLog, AuthenticationLogout, AuthenticationRegister
from environment import database
from flask_pymongo import PyMongo
from models.SchemasTrashes import UserSchema
from functions import forms

''' This is the app config tha allows control the application '''
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://"+ database['host'] +":"+str(database['port']) +"/" + database['dbname']
api = Api(app)
mongo = PyMongo(app)

#Default route
@app.route('/')
def index():
    return 'Servicio para el monitoreo de basureros inteligentes'


'''
    * Function to give format to json array response
    * return an array
'''
def format_response(object, schema):
    return [schema.dump(doc) for doc in object]


'''
    * Class to get User resources after that the user is logged
'''
class UserWithTrashes(Resource):

      def get(self, user):
        user_data = mongo.db.users_with_trashes.find({})
        schema = UserSchema()
        return format_response(user_data, schema)

      def post(self, user):
          
        if request.method == 'POST':
            
            data=forms.createFormDataUser()
            print(data[1])
            if(data[0]):
                print(data[1])
                store = mongo.db.users_with_trashes.insert_one(data[1]).inserted_id    
            else:
                return {'message':'It Could not insert the data, Reintent later',
                        'status':404}
        return {"message":"The data was inserted successfull",
                "status": 200}


'''
    * Class to get User an specifi resource by ID
'''
class UserWithTrashesById(Resource):

      def get(self, user, id):
            return "get request"

      def put(self, user, id):
            return "put request"

      def patch(self,user, id):
            return "patch request"

      def delete(self, user, id):
            return "delete request"

'''
    * The next classes are to authenticate the access user            
'''
class AuthenticationLog(Resource):

      def post(self):
            return "Start sesion"
      
class AuthenticationLogout(Resource):

      def get(self):
            return "Close sesion"

class AuthenticationRegister(Resource):

      def post(self):
            return "register"

# These are the api resources url  
api.add_resource(UserWithTrashes, '/user_with_trashes/<user>')
api.add_resource(UserWithTrashesById, '/user_with_trashes/<user>/<id>')
api.add_resource(AuthenticationLog, '/authentication/log')
api.add_resource(AuthenticationLogout, '/authentication/logout')
api.add_resource(AuthenticationRegister, '/authentication/register')