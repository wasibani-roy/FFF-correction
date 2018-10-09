"""
Routes module to handle request urls
"""
from fast_food_app.controllers.menu import menu_items
from fast_food_app.controllers.users import user_login, user_registration
from fast_food_app.controllers.orders import order_modal, specific_order, get_user_history


class Urls:
    """
        Class to generate urls
    """

    @staticmethod
    def generate(app):
        """
        Generate urls
        :param app:
        :return:
        """
        app.add_url_rule('/api/v2/signup/', view_func=user_registration.as_view('register'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v2/login/', view_func=user_login.as_view('login'),
                         methods=['post'], strict_slashes=False)
        app.add_url_rule('/api/v2/menu/', view_func=menu_items.as_view('add_menu'),
                         methods=['post'], strict_slashes=False)
        app.add_url_rule('/api/v2/menu/', view_func=menu_items.as_view('list_menu_items'),
                         methods=['get'], strict_slashes=False)
        app.add_url_rule('/api/v2/order/', view_func=order_modal.as_view('place_your_order'),
                         methods=['post'], strict_slashes=False)
        app.add_url_rule('/api/v2/order/', view_func=order_modal.as_view('get all orders'),
                         methods=['get'], strict_slashes=False)
        app.add_url_rule('/api/v2/order/<int:order_id>/', view_func=specific_order.as_view('get all orders by id'),
                         methods=['get'], strict_slashes=False)
        app.add_url_rule('/api/v2/user/order/', view_func=get_user_history.as_view('get user history data'),
                         methods=['get'], strict_slashes=False)
        app.add_url_rule('/api/v2/order/', view_func=order_modal.as_view('update order details'),
                         methods=['put'], strict_slashes=False)
