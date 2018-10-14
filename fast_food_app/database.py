from urllib.parse import urlparse
import psycopg2
from flask import current_app as app
import psycopg2.extras as roy


class Database:
    """This class connects to the database"""
    def __init__(self, database_url):
        parsed_url = urlparse(database_url)
        db = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port

        self.conn = psycopg2.connect(
            database=db, user="postgres", password="",
            host="localhost", port=""
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=roy.RealDictCursor)

    def check_table(self, table_name):
        self.cur.execute("select * from information_schema.tables where table_name=%s", (table_name,))
        return bool(self.cur.rowcount)



    def drop_table(self, *table_names):
        '''Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            print('all tables dropped')
            self.cur.execute(drop_table)