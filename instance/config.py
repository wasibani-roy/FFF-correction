import os

class BaseConfig:
    DATABASE_URL = 'postgresql://postgres:root@localhost:5432/order3_db'
    DEBUG = True
    DB = 'fast_food_db'

class DevelopmentConfig(BaseConfig):
    DATABASE_URL = 'postgresql://postgres:root@localhost:5432/order3_db'
    DEBUG = True
    DB = 'fast_food_db'

class TestingConfig(BaseConfig):
    if os.getenv('TRAVIS'):
        DATABASE_URL = 'postgres://postgres@localhost/order3_test_db'
    else:
        DATABASE_URL = 'postgres://postgres:root@localhost:5432/order3_test_db'
    DEBUG = False
    Testing = True
    DB = 'order3_test_db'

class ProductionConfig(BaseConfig):
    os.getenv('FLASK_ENV')
    Debug = False
    DATABASE_URL = ''

app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
