from flask import request
from flask_restful import Resource
from marshmallow import Schema
from applicaction.models.SchemasTrashes import UserSchema
from applicaction.functions import forms, hash
from bson import ObjectId
from secrets import token_hex
from applicaction import mongo, api, app

defaultFirebaseRoute = "https://smarttrash-6587f.firebaseio.com/database"

#Default route
@app.route('/')
def index():

    #user_data = mongo.db.users_with_trashes.find({})
    #schema = UserSchema()
    #return format_response(user_data, schema)

    return 'Servicio para el monitoreo de basureros inteligentes'

'''
    * Function to give format to json array response
    * return an array
'''
def format_response(object, schema):
    return [schema.dump(doc) for doc in object]

'''
    * Database token validation
'''


def token_validation(token):
    return True if mongo.db.users_with_trashes.find_one({'token':token}) else False

'''
    * Class to get User resources after that the user is logged
'''
class UserWithTrashes(Resource):

    #Get all user info
    def get(self, token, id_user):
        response = ""
        if token_validation(str(token)):
            try:
                data = mongo.db.users_with_trashes.find_one({"_id": ObjectId(id_user)})
                if (data):
                    schema = UserSchema()
                    response = {
                        "message": "Access to resource was permited",
                        "status": 200,
                        "data": schema.dump(data)
                    }
                else:
                    response = {
                        "message": "The id is not referenced with no user",
                        "status": 403,
                        "data": []
                    }
            except:
                response = {
                    "message": "Invalid format Id",
                    "status": 403,
                    "data": []
                }
        else:
            response = {
                "message": "You access token is invalid, It's probabliy that you have not permisson to access or your access token has expired, please register an account to access to this resourse or contact to email: contact@smarttrash.com",
                "status": 403
            }

        return response

    #  Save a new trash
    def post(self, token, id_user):

        response = None
        if token_validation(token):
            if request.method == 'POST':

                name = request.form.get('name')

                new_trash = {
                    "name": name,
                    "percent_fill": 0,
                    "realtime_db_url": defaultFirebaseRoute + "/user"+ str(id_user)+"/"+name,
                    "status": 1,
                    "uses": 0,
                    "filled": 0,
                    "message": "El basurero esta vacio",
                    "active": 1
                }

                #updating user
                user = mongo.db.users_with_trashes.find_one({"_id":ObjectId(id_user)})
                user['firebase_collection_url'] = defaultFirebaseRoute + "/user" + str(id_user)
                set = {"$set":user}
                update = mongo.db.users_with_trashes.update_one({"_id":ObjectId(id_user)}, set)

                push = {"$push":{"trashes":new_trash}}
                save = mongo.db.users_with_trashes.update_one({"_id":ObjectId(id_user)}, push)
                response = {"message":"Trash inserted successfully", "status":200}
        else:
            response = {
                "message": "You access token is invalid, It's probabliy that you have not permisson to access or your access token has expired, please register an account to access to this resourse or contact to email: contact@smarttrash.com",
                "status": 403
            }
        return response

    #   Edit user data
    def put(self, token, id_user):

        response = None
        if token_validation(token):
            if request.method == 'PUT':
                user = mongo.db.users_with_trashes.find_one({'_id':ObjectId(id_user)})
                data = forms.updateFormDataUser(user)
                if data[0]:
                    set = {'$set': data[1]}
                    update = mongo.db.users_with_trashes.update_one({'_id':ObjectId(id_user)}, set)
                    response = {'message':'User data was updated successfully', 'status':200}
                else:
                    response = {'message':'User was not updated :(', 'status':404}
        else:
            response = { "message": "You access token is invalid, It's probabliy that you have not permisson to access or your access token has expired, please register an account to access to this resourse or contact to email: contact@smarttrash.com",
                "status": 403}

        return response

'''
    * Class to get a user specific resource by ID
'''
class UserWithTrashesById(Resource):

    def get(self, token, id_user, id_trash):

        response = None
        if token_validation(token):

            try:
                trash = mongo.db.users_with_trashes.find_one({"_id":ObjectId(id_user)},
                            {"trashes":{"$elemMatch":{"name":str(id_trash)}}})

                response = {
                    "message": "Trash found",
                    "status":200,
                    "data": trash['trashes'][0]
                }
            except:
                response = {
                    "message": "Trash not found :(",
                    "status": 200,
                    "data": {}
                }
        else:
            print("err")
            response = {
                "message": "You access token is invalid, It's probabliy that you have not permisson to access or your access token has expired, please register an account to access to this resourse or contact to email: contact@smarttrash.com",
                "status": 403}
        return response

    def put(self, token, id_user, id_trash):
        return "put request"

    def patch(self,token, id_user, id_trash):
        return "patch request"

    def delete(self, token, id_user, id_trash):
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
            update = mongo.db.users_with_trashes.update_one({"_id": ObjectId(id)}, set)
            if (update):
                return {"message":"You have unlogged successfull", "status": 202}
            else:
                return {"message": "Probably not there is an active session", "status":404}
        except:
            return {"message":"There is a problem with ID", "status": 403}

class AuthenticationRegister(Resource):

    def post(self):

        response = None
        if request.method == 'POST':

            data = forms.createFormDataUser()
            print(data[1])
            if (data[0]):
                print(data[1])
                store = mongo.db.users_with_trashes.insert_one(data[1]).inserted_id

                response = {
                "message": "The data was inserted successfull",
                "status": 200
                }
            else:
                response = {
                    'message': 'It Could not insert the data, Reintent later',
                    'status': 404
                }

        return response

# These are the api resources url  
api.add_resource(UserWithTrashes, '/service/user_with_trashes/<token>/<id_user>')
api.add_resource(UserWithTrashesById, '/service/user_with_trashes/<token>/<id_user>/<id_trash>')
api.add_resource(AuthenticationLog, '/service/authentication/log')
api.add_resource(AuthenticationLogout, '/service/authentication/logout/<id>')
api.add_resource(AuthenticationRegister, '/service/authentication/register')