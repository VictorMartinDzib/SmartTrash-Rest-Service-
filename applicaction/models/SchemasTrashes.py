from marshmallow import fields, Schema, pprint

class TrashSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    percent_fill = fields.Float()
    realtime_db_url = fields.Str()
    status = fields.Int()
    uses = fields.Float()
    filled = fields.Int()
    message = fields.Str()
    active = fields.Int()
    
class UserSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    lastname = fields.Str()
    company = fields.Str()
    country = fields.Str()
    state = fields.Str()
    city = fields.Str()
    zip_code = fields.Int()
    address = fields.Str()
    email = fields.Str()
    password = fields.Str()
    token = fields.Str()
    status = fields.Int()
    role = fields.Str()
    active = fields.Str()
    firebase_collection_url = fields.Str()
    trashes = fields.List(fields.Nested(TrashSchema))






