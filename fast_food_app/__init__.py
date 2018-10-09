from flask import Flask, jsonify
from instance.config import app_config
from flask_jwt_extended import JWTManager
from fast_food_app.views import Urls
import os


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    env = os.getenv('FLASK_ENV')
    Urls.generate(app)

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

    jwt = JWTManager(app)

    return app


