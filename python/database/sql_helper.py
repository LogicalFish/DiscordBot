"""
Contains helper functions for generating proper SQL statements.
"""


def generate_insert_sql(var_dict, table, return_value=False):
    """
    Generates a valid query for Creating an entry into a table.
    :param var_dict: The values that should go into the table. Keys are columns.
    :param table: The table name.
    :param return_value: Whether the statement should return a value (and which value)
    :return: A valid SQL query, in addition to a list of values that should safely be inserted.
    """
    sql = """INSERT INTO {} ({}) VALUES ({}) {};"""
    columns = ""
    s_vals = ""
    value_list = []
    for key in var_dict.keys():
        if columns and s_vals:
            columns += ", "
            s_vals += ", "
        columns += key
        s_vals += "%s"
        value_list.append(var_dict[key])
    if return_value:
        return sql.format(table, columns, s_vals, "RETURNING " + return_value), tuple(value_list)
    else:
        return sql.format(table, columns, s_vals, ""), tuple(value_list)


def generate_update_sql(var_dict, pk, pk_name, table):
    """
    Generates a valid query for Updating an entry in a table.
    :param var_dict: The values that should go into the table. Keys are columns.
    :param pk: The primary key value of the entry.
    :param pk_name: The Primary Key column of the table.
    :param table: The table name.
    :return: A valid SQL query, in addition to a list of values that should safely be inserted.
    """
    sql = "UPDATE {} SET {} WHERE {} = {};"
    s_vals = ""
    new_values = []
    for key in var_dict.keys():
        if s_vals:
            s_vals += ","
        s_vals += "{} = %s".format(key)
        new_values.append(var_dict[key])

    return sql.format(table, s_vals, pk_name, pk), tuple(new_values)


def generate_delete_sql(pk, pk_name, table):
    """
    Generates a valid query for Deleting an entry in a table.
    :param pk: The primary key value of the entry.
    :param pk_name: The Primary Key column of the table.
    :param table: The table name.
    :return: A valid SQL query.
    """
    sql = "DELETE FROM {} WHERE {} = {};".format(table, pk_name, pk)
    return sql


def generate_column_sql(table):
    """
    Generates a valid query for getting each column name of a table.
    :param table: The table name.
    :return: A valid SQL query.
    """
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';".format(table)
    return sql


def generate_all_rows_sql(table, sort=None):
    """
    Generates a valid query for getting all information from a table.
    :param table: The table name.
    :param sort: What the data should be sorted by, if any.
    :return: A valid SQL query.
    """
    sql = "SELECT * FROM {}".format(table)
    if sort:
        sql += " ORDER BY {}".format(sort)
    sql += ";"
    return sql


def generate_get_row_sql(pk, pk_name, table):
    """
    Generates a valid query for Reading a single entry in table
    :param pk: The primary key value of the entry.
    :param pk_name: The Primary Key column of the table.
    :param table: The table name.
    :return: A valid SQL query.
    """
    sql = "SELECT * FROM {} WHERE {}={};".format(table, pk_name,pk)
    return sql
