from flask import Flask
from flask_mysqldb import MySQL
from flask_jsonrpc import JSONRPC
from jsonrpcclient import request

'''
Сервис заказов
    Запись заказов
    Изменение статуса заказов
    Отслеживание статуса заказа по id
    Получение неоплаченного заказа клиента по id клиента
    Добавить товар в заказ
    Получение списка заказов (кроме завершенных)
'''

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db_orders'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testSQL'
app.config['MYSQL_DB'] = 'orders_test'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

jsonrpc = JSONRPC(app, '/orders', enable_web_browsable_api=False)

@jsonrpc.method('App.add_order')
def add_order(id_cart: int, id_client: int, cost: float, address: str) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO orders(id_client, cost, status, address) VALUES (%s, %s, %s, %s)""", [id_client, cost, "Ожидает оплаты", address])
        conn.commit()
        cursor.execute("""SELECT id FROM orders WHERE id_client = %s ORDER BY id DESC LIMIT 1""", [id_client])
        data = cursor.fetchall()
        list_prod = request("http://localhost:5002/carts", "App.get_list_prod", id_cart=id_cart).data.result
        id_order = data[0][0]
        add_product(id_order, list_prod)
        return str(id_order) #return id_order
    except Exception as e:
        return str(e)

@jsonrpc.method('App.change_status')
def change_status(id_order: int, new_status: str) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""UPDATE orders SET status = %s WHERE id = %s""", [new_status, id_order])
        conn.commit()
        return "success"
    except Exception as e:
        return str(e)

@jsonrpc.method('App.get_order')
def get_order(id_order: int) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM orders WHERE id = %s""", [id_order])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'id_client': data[0][1],
                'cost': data[0][2],
                'status': data[0][3],
                'address': data[0][4]
                }
            return data_dict
        else:
            return {"error": "Order not found"}
    except Exception as e:
        return {"error": str(e)}

@jsonrpc.method('App.get_unpaid_order')
def get_unpaid_order(id_client: int) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM orders WHERE id_client = %s AND status = %s""", [id_client, "Ожидает оплаты"])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'id_client': data[0][1],
                'cost': data[0][2],
                'status': data[0][3],
                'address': data[0][4]
                }
            return data_dict
        else:
            return {"error": "Order not found"}
    except Exception as e:
        return {"error": str(e)}

@jsonrpc.method('App.add_product')
def add_product(id_order: int, products: list) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        for prod in products:
            cursor.execute("""INSERT INTO products_of_order(id_order, id_product, quantity) VALUES (%s, %s, %s)""", [id_order, prod['id_product'], prod['quantity']])
            conn.commit()
        return "success"
    except Exception as e:
        return str(e)

@jsonrpc.method('App.get_list_orders')
def get_list_orders() -> list:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM orders WHERE status != %s""", ["Выполнен"])
        data = cursor.fetchall()
        data_list = []
        for order in data:
            data_dict = {
                'id': data[0][0],
                'id_client': data[0][1],
                'cost': data[0][2],
                'status': data[0][3],
                'address': data[0][4]
                }
            data_list.append(data_dict)
        return data_list
    except Exception as e:
        return [str(e)]

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5001, debug=True)
