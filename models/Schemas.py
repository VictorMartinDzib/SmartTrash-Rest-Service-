from marshmallow import fields, Schema, pprint

class UserSchema(Schema):
    nombre = fields.Str()
    apellidos = fields.Str()
