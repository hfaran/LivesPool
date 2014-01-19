from tornado.options import options
from tornado_json.db import MySQLConnection


class Connection(object):

    def __init__(self):
        conn = MySQLConnection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
        )
        self.generic_query = conn.generic_query
        self.__db_dataset = conn._db_dataset

