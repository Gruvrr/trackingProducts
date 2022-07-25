import psycopg2
import scrapping_lerua
from config import host, user, password, db_name


def updateDataEveryday():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT product_url FROM products;"""
        )
        list_urls = cursor.fetchall()
    connection.close()
    try:
        for url in range(len(list_urls) - 1):
            unit_data = scrapping_lerua.get_unit_data(list_urls[url][0])
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO products ( product_articul,product_url,product_price, stock_mega, stock_orbitalnaya, 
                    stock_dovatora, last_change_date) 
                       VALUES(%(product_articul)s,%(product_url)s,%(product_price)s,%(stock_mega)s,%(stock_severniy)s,
                       %(stock_dovatora)s,%(last_change_date)s;""", unit_data)
    except Exception as _ex:
        print("ERROR IN 'updateDataEveryDay'", _ex)
    finally:
        if connection:
            connection.close()
    return



