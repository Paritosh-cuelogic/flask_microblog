from flask_restful import Resource
from app.api import api


class User(Resource):
    def get(self):
        return 'get users list'


api.add_resource(User, '/user')
