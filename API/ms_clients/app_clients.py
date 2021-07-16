from flask import Flask
from flask_mysqldb import MySQL
from flask_jsonrpc import JSONRPC

'''
Сервис клиентов
    Регистрация
    Авторизация
    Поиск пользователя по id
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
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

jsonrpc = JSONRPC(app, '/clients', enable_web_browsable_api=False)

@jsonrpc.method('App.login_user')
def login_user(email: str, password: str) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM clients WHERE email=%s AND password=%s""", [email, password])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'full_name': data[0][1],
                'email': data[0][2],
                'password': data[0][3],
                'phone': data[0][4],
                'error':''
                }
            return data_dict
        else:
            return {"error": "Пользователь не найден в системе. Проверьте корректность введенных данных"}
    except Exception as e:
        return {"error": "Ошибка на сервере"}


@jsonrpc.method('App.reg_user')
def reg_user(full_name: str, email: str, password: str, phone: str) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM clients WHERE email=%s OR phone_num=%s""", [email, phone])
        data = cursor.fetchall()
        if len(data) > 0:
            return "error"
        else:
            cursor.execute("""INSERT INTO clients(full_name, email, password, phone_num) VALUES (%s, %s, %s, %s)""", [full_name, email, password, phone])
            conn.commit()
            return "success"
    except Exception as e:
        return str(e)


@jsonrpc.method('App.get_user')
def get_user(id_user: int) -> dict:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM clients WHERE id=%s""", [id_user])
        data = cursor.fetchall()
        if len(data) > 0:
            data_dict = {
                'id': data[0][0],
                'full_name': data[0][1],
                'email': data[0][2],
                'password': data[0][3],
                'phone': data[0][4],
                'error':''
                }
            return data_dict
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

@jsonrpc.method('App.change_user_data')
def change_user(id_user: int,full_name: str, email: str, password: str, phone: str) -> str:
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM clients WHERE (email=%s or phone_num=%s) and id!=%s""", [email,phone,id_user])
        data = cursor.fetchall()
        if len(data) > 0:
            return "error"
        else:
            cursor.execute("""UPDATE clients SET full_name=%s,email=%s,phone_num=%s,password=%s WHERE id=%s""",[full_name, email, phone, password, id_user])
            conn.commit()
            return "success"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()
