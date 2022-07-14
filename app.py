import psycopg2
from flask import Flask, render_template, request
import scrapping_lerua
from config import host, user, password, db_name


app = Flask(__name__)


@app.route('/', methods=['GET'])
def getAllProducts():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM products;"""
            )
            data = cursor.fetchall()
            data_list = []
            for el in data:
                values = {

                    'product_articul': el[1],
                    'product_url': el[2],
                    "product_price": el[3],
                    'stock_mega': el[4],
                    'stock_severniy': el[5],
                    'stock_dovatora': el[6],
                    'last_change_date': el[7]
                }
                data_list.append(values)
            print(type(data_list))
            print(data_list)
    except Exception as _ex:
        print("ERROR", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO]DATABASE Connection closed")
        print("[INFO] ITS ALL OK")
        return render_template('index.html', the_title='Главная страница', data=data_list)

@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        req_url = request.form['url']
        data = scrapping_lerua.get_unit_data(req_url)

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO products ( product_articul,product_url,product_price, stock_mega, stock_orbitalnaya, stock_dovatora,last_change_date) 
                   VALUES(%(product_articul)s,%(product_url)s,%(product_price)s,%(stock_mega)s,%(stock_severniy)s,%(stock_dovatora)s,%(last_change_date)s;""",data)
            print("[INFO] INSERT GOOOOOOOD")
    except Exception as _ex:
        print("ERROR", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO]DATABASE Connection closed")
        print("[INFO] ITS ALL OK")
        return render_template('addProduct.html', the_title='Главная страница', Message='Товар добавлен успешно')


if __name__ == '__main__':
    app.run(debug=True)
