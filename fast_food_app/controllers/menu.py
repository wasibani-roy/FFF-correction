from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from fast_food_app.models.models import Menu, Users

class menu_items(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        x = Users(email=None,username=None,password=None)
        if x.check_admin(current_user):
            parser = reqparse.RequestParser()
            parser.add_argument('product', help='This field cannot be blank', required=True)
            parser.add_argument('description', help='This field cannot be blank', required=True)
            parser.add_argument('price', help='This field cannot be blank', required=True)
            data = parser.parse_args()
            if "product" not in data:
                return jsonify({"Error": "Please enter product"}), 404
            if "description" not in data:
                return jsonify({"Error": "Please enter description"}),404
            if "price" not in data:
                return jsonify({"Error": "Please enter price"}),404
            product = data['product'].strip()
            description = data['description'].strip()
            price = data['price'].strip()
            if product == "" or description == "" or price == "":
                return jsonify({"Error": "Sorry one or more fields are incomplete"}), 400
            else:
                data = {"product": product, "description": description, "price": price}
                menu_item = Menu(product=product, description=description, price=price)
                return menu_item.new_menu()
        else:
            return jsonify({"Message": "Unauthorised"}), 404

    def get(self):
        all_menu_items = Menu(product="none", price="none", description="none")
        return all_menu_items.get_menu_items()

