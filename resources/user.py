import sqlite3
from flask_restful import Resource,reqparse
from models.usermodel import UserModel



class UserResgiter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', help="pls enter your username", required=True)
    parser.add_argument('password', required=True, help="Pls enter your password")

    def post(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        data = UserResgiter.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'msg' : "user already registered"}
        user = UserModel(**data)
        user.save_to_db()
        return {'msg' : "user registered successfully"}

