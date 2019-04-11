import psycopg2


class CursorDecorator:
    """
    Decorator class for the database manager.
    """

    def __init__(self, conn):
        self.conn = conn

    def __call__(self, func):
        def wrapped_func(*args):
            try:
                cur = self.conn.cursor()
                value = func(*args, cur=cur)
                cur.close()
                return value
            except (Exception, psycopg2.DatabaseError) as error:
                # print(error)
                raise error
        return wrapped_func
