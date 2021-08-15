from flask import Flask
from flask_mysqldb import MySQL
from flask_jsonrpc import JSONRPC
from jsonrpcclient import request

'''
Сервис платежей
    Запись платежей
    Изменение статуса платежей
    Получение платежа по id
'''

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db_payments'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testSQL'
app.config['MYSQL_DB'] = 'payments_test'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

jsonrpc = JSONRPC(app, '/payments', enable_web_browsable_api=False)

@jsonrpc.method('App.add_payment')
def add_payment(id_order: int, cost: float) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO payment(id_order, cost) VALUES (%s, %s)""", [id_order, cost])
        conn.commit()
        cursor.execute("""SELECT id FROM payment WHERE id_order = %s""", [id_order])
        data = cursor.fetchall()
        res_change = request("http://localhost:5001/orders", "App.change_status", id_order=id_order, new_status="Оплачен").data.result
        if res_change == "success":
            return str(data[0][0]) #return id_payment
        else:
            return res_change
    except Exception as e:
        return str("Server problem")

@jsonrpc.method('App.get_payment')
def get_payment(id_payment: int) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM payment WHERE id = %s""", [id_payment])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'id_order': data[0][1],
                'cost': data[0][2],
                'status': data[0][3]
                }
            return data_dict
        else:
            return {"error": "Payment not found"}
    except Exception as e:
        return {"error": "Server problem"}


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5004, debug=True)
