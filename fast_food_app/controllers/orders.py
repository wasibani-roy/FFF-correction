from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from fast_food_app.models.models import Order, Users

class order_modal(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('menuid', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        menu_item_id = int(data["menuid"].strip())

        if menu_item_id == "":
            return jsonify({"Error": "You have not selected you're order"}), 404
        else:
                new_order = Order(menu_id=menu_item_id, user_id=current_user,status="none",order_id="none")


                return new_order.add_order()

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        x = Users(email=None, username=None, password=None)
        if x.check_admin(current_user):
            orders = Order(order_id="none", status="none", menu_id="none", user_id="none")
            return orders.get_order_items()
        else:
            return jsonify({"Error": "Unauthorised access"}), 400

    # def get(self):
    #     current_user = get_jwt_identity()
    #     orders = Order(user_id=current_user, menu_id="null", status="null", order_id="null")
    #     return orders.get_user_order()


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('orderid', help='This field cannot be blank', required=True)
        parser.add_argument('status', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        order_id = data["orderid"].strip()
        order_status = data["status"].strip()
        if order_id == "" or order_status == "":
            return jsonify({"Error": "Missing order id or order status"}),404
        else:
            orders = Order(order_id=order_id,status="null", user_id="null", menu_id="null")
            return orders.update_order(order_status)


class specific_order(Resource):
    @jwt_required
    def get(self,order_id= id):
        current_user = get_jwt_identity()
        x = Users(email=None, username=None, password=None)
        if x.check_admin(current_user):
            new_order_id = int(order_id)
            orders = Order(user_id=current_user, order_id=new_order_id, menu_id="none", status="none")

            return orders.order_by_id()
        else:
            return jsonify({"Error": "Unauthorised access"}), 400

class get_user_history(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        orders = Order(user_id=current_user, order_id="none", status="none", menu_id="none")
        return orders.get_user_order()


