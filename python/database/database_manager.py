from database import sql_helper
from database.database_connection import DatabaseConnection
from database.decorators import CursorDecorator


class DatabaseManager:
    """Manager for the database."""

    db = DatabaseConnection()

    @CursorDecorator(db.conn)
    def insert(self, var_dict, table, value_request=None, cur=None):
        """
        Insert a new entry into a database.
        :param var_dict: A dictionary containing the values that should be added.
        :param table: The table in which the dictionary should be inserted.
        :param value_request: Whether the method should return a value.
        :param cur: Cursor. Used by the CursorDecorator.
        :return: The value requested by the method, if any.
        """
        statement, values = sql_helper.generate_insert_sql(var_dict, table, value_request)
        cur.execute(statement, values)
        self.db.conn.commit()
        if value_request is not None:
            return_value = cur.fetchone()[0]
            return return_value

    @CursorDecorator(db.conn)
    def update(self, var_dict, pk_value, primary_key, table, cur=None):
        """
        Update an entry in the database.
        :param var_dict: A dictionary containing the updated values.
        :param pk_value: The Primary Key value of the entry to be updated.
        :param primary_key: The primary key of the chosen table.
        :param table: The table which should be updated.
        :param cur: Cursor. Used by the CursorDecorator.
        """
        statement, values = sql_helper.generate_update_sql(var_dict, pk_value, primary_key, table)
        cur.execute(statement, values)
        self.db.conn.commit()

    @CursorDecorator(db.conn)
    def delete(self, pk_value, primary_key, table, cur=None):
        """
        Delete an entry in the database.
        :param pk_value: The primary key value of the entry to be deleted.
        :param primary_key: The primary key of the chosen table.
        :param table: The table to be updated.
        :param cur: Cursor. Used by the CursorDecorator.
        """
        statement = sql_helper.generate_delete_sql(pk_value, primary_key, table)
        cur.execute(statement)
        self.db.conn.commit()

    @CursorDecorator(db.conn)
    def select_one_row(self, pk_value, primary_key, table, cur=None):
        """
        Read an entry in the database.
        :param pk_value: The Primary Key value of the entry to be selected.
        :param primary_key: The primary key of the chosen table.
        :param table: The table to read from.
        :param cur: Cursor. Used by the CursorDecorator.
        :return: The entire entry.
        """
        statement = sql_helper.generate_get_row_sql(pk_value, primary_key, table)
        cur.execute(statement)
        row = cur.fetchone()
        return row

    @CursorDecorator(db.conn)
    def select_all(self, statement, cur=None):
        """
        Reads an entire table, based on the given statement.
        :param statement: The statement
        :param cur: Cursor. Used by the CursorDecorator.
        :return: The result of the statement.
        """
        cur.execute(statement)
        rows = cur.fetchall()
        return rows

    def get_columns(self, table):
        """
        Get all column names of a specific table.
        :param table: The table to get the column names of.
        :return: A list of all column names.
        """
        statement = sql_helper.generate_column_sql(table)
        result = []
        for t in self.select_all(statement):
            result.append(t[0])
        return result

    def get_rows(self, table, sort=None):
        """
        Get all rows/entries of a specific table.
        :param table: The table to get the entries of.
        :param sort: The columns that the table should be sorted by.
        :return: A list of all entries of a table.
        """
        statement = sql_helper.generate_all_rows_sql(table, sort=sort)
        return self.select_all(statement)
