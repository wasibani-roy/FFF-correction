from fast_food_app import create_app
from fast_food_app.database  import Database
import os

config_name = 'development'
app = create_app(config_name)

# db = Database('postgresql://postgres:1460@localhost:5432/fast_food_db')

if __name__ == '__main__':
    # db.create_tables()
    # db.drop_table('users','orders','food_items')
    app.run()
