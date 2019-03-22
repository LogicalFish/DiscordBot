

def generate_insert_sql(var_dict, table):
    sql = """INSERT INTO {} ({}) VALUES ({}) RETURNING event_id;"""
    columns = ""
    values = ""
    for key in var_dict.keys():
        if columns and values:
            columns += ", "
            values += ", "
        columns += key
        values += "'{}'".format(var_dict[key])
    return sql.format(table, columns, values)


def generate_column_sql(table):
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}';".format(table)
    return sql


def generate_all_rows_sql(table, sort=None):
    sql = "SELECT * FROM {}".format(table)
    if sort:
        sql += " ORDER BY {]".format(sort)
    sql += ";"
    return sql


def generate_get_row_sql(pk, pk_name, table):
    sql = "SELECT * FROM {} WHERE {}={};".format(table,pk_name,pk)
    return sql

def generate_delete_sql(pk, pk_name, table):
    sql = "DELETE FROM {} WHERE {} = {}".format(table,pk_name,pk)
    return sql