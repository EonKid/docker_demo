__author__ = 'Dhruv Narayan Singh'
from flask_restful import Resource
from flask import request


class UserList(Resource):

    def get(self):
        return [
            {"name":"John Doe", "id":25434343},
            {"name": "Jack Ryan", "id": 273463634},
            {"name": "The Avengers", "id": 3345345},
            {"name": "Captain America", "id": 5454545}
        ]


class AuthenticationHandler(Resource):

    def post(self, *args, **kwargs):
        print(args)
        try:
            username = request.headers["username"]
            password = request.headers["password"]
            if username is not None and password is not None:
                return {"msg": "Login successfully!"}
            else:
                return {"msg": "Authentication failed!"}

        except KeyError as ex:
            return {"error": str(ex)}