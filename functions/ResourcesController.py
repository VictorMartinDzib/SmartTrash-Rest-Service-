'''
      Clases encargadas de ejecutar acciones
      segun sea el metodo de petición.

      Classes that execute actions by request method
'''

from flask_restful import Resource
from marshmallow import Schema
from models.SchemasTrashes import UserSchema
#from database.Db import getDatabasInstance

def format_response(object, schema):
    return [schema.dump(doc) for doc in object]

class UserWithTrashes(Resource):

      def get(self, user):
            users = mongo.db.users_with_trashes.find({})
            schema = UserSchema()
            return format_response(users, schema)
            #return "get request: get all"
      def post(self, user):
            return "post request"


class UserWithTrashesById(Resource):

      def get(self, user, id):
            return "get request"

      def put(self, user, id):
            return "put request"

      def patch(self,user, id):
            return "patch request"

      def delete(self, user, id):
            return "delete request"

class AuthenticationLog(Resource):

      def post(self):
            return "Start sesion"
      
class AuthenticationLogout(Resource):

      def get(self):
            return "Close sesion"

class AuthenticationRegister(Resource):

      def post(self):
            return "register"
