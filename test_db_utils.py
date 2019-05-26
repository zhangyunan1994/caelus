from db_util import get_databases, get_tables


def test_get_database():
    result = get_databases('127.0.0.1', 3306, 'root', '123456')
    print(result)


def test_get_table():
    result = get_tables('127.0.0.1', 3306, 'root', '123456', 'ecm')
    print(result)


if __name__ == '__main__':
    test_get_database()
    test_get_table()
