import pymysql


_select_column_database_sql = "select \
    TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, IS_NULLABLE, COLUMN_TYPE, COLUMN_COMMENT \
    FROM information_schema.`COLUMNS` \
    where COLUMN_NAME = %s"

_select_database_sql = "SELECT SCHEMA_NAME from information_schema.SCHEMATA"

_select_table_sql = "SELECT TABLE_NAME, TABLE_COMMENT from information_schema.`TABLES` where TABLE_SCHEMA = %s"

_select_column_sql = "SELECT \
    TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, IS_NULLABLE, COLUMN_TYPE, COLUMN_COMMENT, COLUMN_DEFAULT \
    from information_schema.`COLUMNS`\
    where TABLE_SCHEMA = %s and TABLE_NAME = %s"

_select_connection_column_sql = "select \
    TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, IS_NULLABLE, COLUMN_TYPE, COLUMN_COMMENT, COLUMN_DEFAULT \
FROM information_schema.`COLUMNS` \
where COLUMN_NAME like %s"


def get_databases(host, port, user, password):
    connect = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = connect.cursor()
    cursor.execute(_select_database_sql)
    all_database = cursor.fetchall()
    connect.close()
    return all_database


def get_tables(host, port, user, password, database):
    connect = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = connect.cursor()
    cursor.execute(_select_table_sql, (database))
    all_database = cursor.fetchall()
    connect.close()
    return all_database


def get_columns(host, port, user, password, database, table):
    connect = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = connect.cursor()
    cursor.execute(_select_column_sql, (database, table))
    all_database = cursor.fetchall()
    connect.close()
    return all_database


def get_connection_columns(host, port, user, password, column):
    connect = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = connect.cursor()
    cursor.execute(_select_connection_column_sql, ("%" + column + "%"))
    all_database = cursor.fetchall()
    connect.close()
    return all_database