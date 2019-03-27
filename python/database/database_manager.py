from database import sql_helper
from database.database_connection import DatabaseConnection
from database.decorators import CursorDecorator


class DatabaseManager:

    db = DatabaseConnection()

    @CursorDecorator(db.conn)
    def insert(self, var_dict, table, cur=None):
        statement = sql_helper.generate_insert_sql(var_dict, table)
        cur.execute(statement)
        insert_id = cur.fetchone()[0]
        self.db.conn.commit()
        return insert_id

    @CursorDecorator(db.conn)
    def update(self, var_dict, id_no, primary_key, table, cur=None):
        statement = sql_helper.generate_update_sql(var_dict, id_no, primary_key, table)
        cur.execute(statement)
        self.db.conn.commit()

    @CursorDecorator(db.conn)
    def delete(self, id_no, primary_key, table, cur=None):
        statement = sql_helper.generate_delete_sql(id_no, primary_key, table)
        cur.execute(statement)
        self.db.conn.commit()

    @CursorDecorator(db.conn)
    def select_one(self, id_no, primary_key, table, cur=None):
        statement = sql_helper.generate_get_row_sql(id_no, primary_key, table)
        cur.execute(statement)
        row = cur.fetchone()
        return row

    @CursorDecorator(db.conn)
    def select_all(self, statement, cur=None):
        cur.execute(statement)
        rows = cur.fetchall()
        return rows

    def get_columns(self, table):
        statement = sql_helper.generate_column_sql(table)
        result = []
        for t in self.select_all(statement):
            result.append(t[0])
        return result

    def get_rows(self, table, sort):
        statement = sql_helper.generate_all_rows_sql(table, sort=sort)
        return self.select_all(statement)
