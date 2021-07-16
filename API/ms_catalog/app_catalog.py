from flask import Flask
from flask_mysqldb import MySQL
from flask_jsonrpc import JSONRPC

'''
Сервис каталога товаров
    Выдача каталога товаров (включая фильтрацию)
    Выдача значений фильтров
    Получение товара по id
'''

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

jsonrpc = JSONRPC(app, '/catalog', enable_web_browsable_api=False)

@jsonrpc.method('App.get_catalog')
def get_catalog(filter: str) -> list:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        if filter == "Все":
            cursor.execute("""SELECT * FROM products""")
        else:
            cursor.execute("""SELECT * FROM products WHERE category=%s""", [filter])
        data = cursor.fetchall()
        data_list = []
        for prod in data:
            prod_dict = {
                'id': prod[0],
                'name': prod[1],
                'category': prod[2],
                'description': prod[3],
                'image_name': prod[4],
                'unit': prod[5],
                'price': prod[6],
                'number': prod[7],
                'counter': 0,
                'added': False
                }
            data_list.append(prod_dict)
        return data_list
    except Exception as e:
        return ["Server problem"]

@jsonrpc.method('App.get_filters')
def get_filters() -> list:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM categories""")
        data = cursor.fetchall()
        data_list = []
        for item in data:
            data_list.append(item[0])
        return data_list
    except Exception as e:
        return ["Server problem"]

@jsonrpc.method('App.get_product')
def get_product(products: list) -> list:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        data_list = []
        for id_prod in products:
            cursor.execute("""SELECT * FROM products WHERE id = %s""", [id_prod])
            data = cursor.fetchall()
            prod_dict = {
                'id': data[0][0],
                'name': data[0][1],
                'category': data[0][2],
                'description': data[0][3],
                'image_name': data[0][4],
                'unit': data[0][5],
                'price': data[0][6],
                'number': data[0][7],
                'counter': 0,
                'total': 0
                }
            data_list.append(prod_dict)
        return data_list
    except Exception as e:
        return ["Server problem"]

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5003)
