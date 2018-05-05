from psycopg2 import pool

class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)
        return cls.__connection_pool

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def put_connection(cls, connection):
        return cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connection(cls):
        return cls.__connection_pool.closeall()

    @staticmethod
    def clear_table(name):
        with ConnectionPool() as cursor:
            cursor.execute("TRUNCATE TABLE {} RESTART IDENTITY;".format(name))


class ConnectionPool:

    def __init__(self):
        self.connection, self.cursor = None, None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.put_connection(self.connection)