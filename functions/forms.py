
from flask import request
from functions.hash import encryptPassword
from secrets import token_hex



def createFormDataUser():

      try:
            data = {
                  "name" : request.form.get('name'),
                  "lastname" : request.form.get('lastname'),
                  "company" : request.form.get('company'),
                  "country" : request.form.get('country'),
                  "state" : request.form.get('state'),
                  "city" : request.form.get('city'),
                  "zip_code" : int(request.form.get('zip_code')),
                  "address" : request.form.get('address'),
                  "email" : request.form.get('email'),
                  "password" : encryptPassword(request.form.get('password')),
                  "token" : str(token_hex(32)),
                  "status" : 1,
                  "role" : request.form.get('role'),
                  "active" : 1,
                  "firebase_collection_url" : "",
                  "trashes" : []
            }

            return (True, data)
      
      except:

            return (False, {'error':'Invalid params'})


