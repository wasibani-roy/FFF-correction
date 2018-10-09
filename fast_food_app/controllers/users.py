from flask_restful import Resource, reqparse
from flask import jsonify
from fast_food_app.models.models import Users

class user_registration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        user_name = data["username"].strip()
        email = data["email"].strip()
        if '@' and '.' not in email:
            return jsonify({"error": "Please input a valid email"}), 400
        elif email[0] == '@' or email[0] == '.':
            return jsonify({"error": "Please input a valid email"}), 400
        elif email.index("@") >= email.index('.'):
            return jsonify({"error": "Please input a valid email"}),
        elif email.count("@") > 1 or email.count(".") > 1:
            return jsonify({"error": "Please input a valid email"}), 400
        password = data["password"].strip()

        if user_name == "" or email == "" or  password == "":
            return jsonify({"Error": "Fields have not been filled"}), 400
        else:
            t = tuple(user_name)
            if  t[0].isdigit():
                return jsonify({"error": "username cant be string"}), 400
            else:
                # password_candidste = Users.generate_hash(password)
                new_user = Users(user_name,password,email)

                # user_data = {"username": user_name.lower(), "email": email, "password": password_candidste}

                return new_user.check_user()


class user_login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        user_name = data['username'].lower()
        username = user_name.strip()
        password = data['password']
        if username == "" or password == "":
            return jsonify({"Error": "Username or password missing"}),400
        else:
            verify_user = Users(username, password, email="none")
            return verify_user.authenticate_user()



