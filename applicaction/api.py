from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import Schema
from environment import database
from flask_pymongo import PyMongo
from models.SchemasTrashes import UserSchema
from functions import forms, hash
from bson import ObjectId
from secrets import token_hex

''' This is the app config tha allows control the application '''


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
    Valida que el token este enlazado con un usuario en la bd
'''
def token_validation(token):
    return True if mongo.db.users_with_trashes.find_one({'token':token}) else False
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
        response = ""
        if token_validation(str(user)):
            try:
                if(data := mongo.db.users_with_trashes.find_one({"_id": ObjectId(id)})):
                    schema = UserSchema()
                    response = {
                        "message": "Access to resource was permited",
                        "status":200,
                        "data":schema.dump(data)
                    }
                else:
                    response = {
                        "message": "The id is not referenced with no user",
                        "status":403,
                        "data":[]
                    }
            except:
                response = {
                        "message": "Invalid format Id",
                        "status":403,
                        "data":[]
                    }
        else:
            response = {"message":"You access token is invalid, It's probabliy that you have not permisson to access or your access token has expired, please register an account to access to this resourse or contact to email: contact@smarttrash.com", "status":403}
        return response

    def put(self, user, id):
        return "put request"

    def patch(self,user, id):
        return "patch request"

    def delete(self, user, id):
        return "delete request"

'''
    * The next classes are to authenticate the access user     
        * First validate that email exists
        if email not exists return a 404 status
        * If email exists select the user data and compare the external
        password with the hash code of the database with the function
        validatePassword()       
'''
class AuthenticationLog(Resource):

    def post(self):
        response = ""
        if request.method == 'POST':
            data = {
                'email':request.form.get('email')
            }
            password = request.form.get('password')
            GetByEmail= mongo.db.users_with_trashes.find_one(data)

            if GetByEmail:                
                schema = UserSchema()
                data=schema.dump(GetByEmail)
                e = 5
                if  hash.validatePassword(password, data['password'].encode()):
                    response = {
                        "message": "You have logged successfully",
                        "status": 200,
                        "temp_token":data['token'],
                        "user_id":data['_id']
                    }
                else:
                    response = {"message": "Password is incorrect", "status":401}
                
            else:
                response = {"message":"The email dosen't exists", "status":404}

        return response
      
class AuthenticationLogout(Resource):

    def get(self, id):
        response = ""
        newToken = {"token":str(token_hex(32))}
        set = {'$set':newToken}
        
        try:
            if (update :=  mongo.db.users_with_trashes.update_one({"_id":ObjectId(id)}, set)):
                return {"message":"You have unlogged successfull", "status": 202}
            else:
                return {"message": "Probably not there is an active session", "status":404}
        except:
            return {"message":"There is a problem with ID", "status": 403}

class AuthenticationRegister(Resource):

      def post(self):
            return "register"

# These are the api resources url  
api.add_resource(UserWithTrashes, '/user_with_trashes/<user>')
api.add_resource(UserWithTrashesById, '/user_with_trashes/<user>/<id>')
api.add_resource(AuthenticationLog, '/authentication/log')
api.add_resource(AuthenticationLogout, '/authentication/logout/<id>')
api.add_resource(AuthenticationRegister, '/authentication/register')