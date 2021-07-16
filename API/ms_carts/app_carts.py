from flask import Flask
from flask_mysqldb import MySQL
from flask_jsonrpc import JSONRPC

'''
Сервис корзины
    Запись корзины
    Добавление товара в корзину
    Изменение кол-ва товара в корзине
    Удаление товара из корзины
    Получить id корзины по id клиента 
    Получить список товаров корзины по id
    Обновить корзину по id
    Удалить корзину по id
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

jsonrpc = JSONRPC(app, '/carts', enable_web_browsable_api=False)

@jsonrpc.method('App.add_cart')
def add_cart(id_client: int) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO carts(id_client, cost) VALUES (%s, %s)""", [id_client, 0])
        conn.commit()
        cursor.execute("""SELECT id FROM carts WHERE id_client = %s""", [id_client])
        data = cursor.fetchall()
        return str(data[0][0]) #return id_cart
    except Exception as e:
        return str("Server problem")

@jsonrpc.method('App.add_product')
def add_product(id_cart: int, id_product: int, quantity: int) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO products_of_cart(id_cart, id_product, quantity) VALUES (%s, %s, %s)""", [id_cart, id_product, quantity])
        conn.commit()
        return "success"
    except Exception as e:
        return "Server problem"

@jsonrpc.method('App.update_product')
def update_product(id_cart: int, id_product: int, quantity: int) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""UPDATE products_of_cart SET quantity = %s WHERE id_cart = %s AND id_product = %s""", [quantity, id_cart, id_product])
        conn.commit()
        return "success"
    except Exception as e:
        return "Server problem"

@jsonrpc.method('App.delete_product')
def delete_product(id_cart: int, id_product: int) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM products_of_cart WHERE id_cart = %s AND id_product = %s""", [id_cart, id_product])
        conn.commit()
        return "success"
    except Exception as e:
        return "Server problem"

@jsonrpc.method('App.get_cart')
def get_cart(id_client: int) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM carts WHERE id_client = %s""", [id_client])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'id_client': data[0][1],
                'cost': data[0][2],
                'error': ''
                }
            return data_dict
        else:
            return {'error': 'Not found'}
    except Exception as e:
        return {'error': 'Server problem'}

@jsonrpc.method('App.get_list_prod')
def get_list_prod(id_cart: int) -> list:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM products_of_cart WHERE id_cart = %s""", [id_cart])
        data = cursor.fetchall()
        data_list = []
        for prod in data:
            data_dict = {
                'id_cart': prod[0],
                'id_product': prod[1],
                'quantity': prod[2]
                }
            data_list.append(data_dict)
        return data_list
    except Exception as e:
        return ["Server problem"]

@jsonrpc.method('App.update_cart')
def update_cart(id_cart: int, cost: float) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""UPDATE carts SET cost = %s WHERE id = %s""", [cost, id_cart])
        conn.commit()
        return "success"
    except Exception as e:
        return str("Server problem")

@jsonrpc.method('App.delete_cart')
def delete_cart(id_cart: int) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM carts WHERE id = %s""", [id_cart])
        conn.commit()
        return "success"
    except Exception as e:
        return "Server problem"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)