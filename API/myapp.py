#!/home/std/TPIS/env python3
import sys
import datetime
import smtplib

from flask import Flask, jsonify, request, render_template # Использование веб-фреймворка
from flask_restful import Api, Resource, reqparse, abort # Использование веб-фреймворка 
from flaskext.mysql import MySQL # Использование MySQL коннектора
import pathlib

app = Flask(__name__)
application = app
wsgi_app = app.wsgi_app
mysql = MySQL()
# Параметры подключения к БД
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'course_3'
app.config['MYSQL_DATABASE_HOST'] = 'localhost' # 192.168.20.251:22913
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

# Информационная ветка
@app.route('/')
def start():
    return "hello world"

# Метод авторизации
@app.route('/login/<string:email>/<string:password>')
def login(email, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""select full_name, email, phone_num from clients where email=%s and password=%s""", [email, password])
    data = cursor.fetchall()
    # Если длина ответа больше 0 - запись найдена
    if len(data) > 0:
        data_dict = {
            'full_name': data[0][0],
            'email': data[0][1],
            'phone_num': data[0][2]
        }
        return jsonify(data_dict)
    # Если вход не успешен - возвращаем -1
    else:
        return '-1'

@app.route('/login_courier/<string:phone>/<string:password>')
def login_courier(phone, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""select full_name, email, phone_num from couriers where phone_num=%s and password=%s""", [phone, password])
    data = cursor.fetchall()
    # Если длина ответа больше 0 - запись найдена
    if len(data) > 0:
        data_dict = {
            'full_name': data[0][0],
            'email': data[0][1],
            'phone_num': data[0][2]
        }
        return jsonify(data_dict)
    # Если вход не успешен - возвращаем -1
    else:
        return '-1'


@app.route('/reg', methods=['POST'])
def reg():
    # Если пришёл не JSON - возвращаем HTTP ошибку 400
    if not request.json:
        print(request.json)
        abort(400)
    d = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    # Ищем пользователя
    cursor.execute(
        "select email from clients where phone_num = %s or email = %s",
        [d["phone_num"], d["email"]])
    data = cursor.fetchall()
    # Если таких email и username нет
    if len(data) == 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO clients (`full_name`, `email`, `phone_num`, `password`) "
                "values (%s, %s, %s, %s)",
        [d["full_name"], d["email"], d["phone_num"], d["password"]])
        conn.commit()
        return "1"
    # Если пользователь с таким email или username существует
    else:
        return "-1"

@app.route('/get_courier_coords/<string:email>/<string:password>/<int:courier_id>')
def get_courier_coords(email, password, courier_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from clients where email=%s and password=%s""", [email, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor() 
        cursor.execute("select location_1, location_2 from couriers_locations where id_courier=%s order by time desc limit 1", [courier_id])
        data = cursor.fetchall()
        data_dict.append({"location_1": data[0][0], "location_2": data[0][1]})
        return jsonify(data_dict)
    return "-1"

@app.route('/get_products/')
def get_products():
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select products.id,products.name,number,price,description,image_name,units.name from products,units  where products.unit_id = units.id""")
    data = cursor.fetchall()
    data_dict = []
    for row in data:
        data_dict.append({
            'product_num':row[0],
            'name': row[1],
            'number': row[2],
            'price': row[3],
            'description': row[4],
            'image_name': row[5],
            'unit': row[6],
            'counter':0
        })
    return jsonify(data_dict)

@app.route('/get_orders/<string:email>/<string:password>')
def get_orders(email, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from clients where email=%s and password=%s""", [email, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        # Запрос на поиск пользователя
        cursor.execute("""select order_num_from as order_num, order_date, full_name_from, adr_from, full_name, order_status, status_date, cost, client_id from
(select * from (select * from
    order_details
    left join couriers on courier_id = couriers.id) as t1
    left join (select num, order_status, status_date
            from (
               select order_statuses.order_num as num, max(status_date) latestDate
               from order_statuses
               inner join orders on order_statuses.order_num = orders.order_num
               group by order_statuses.order_num
               ) a
            inner join order_statuses on order_statuses.order_num = a.num
            where order_statuses.status_date = a.latestDate) as status on num = order_num_from) as t where client_id =%s""", [data[0][0]])
        data = cursor.fetchall()
        for row in data:
            data_dict.append({
                'order_num': row[0],
                'order_date': row[1],
                'receiver': row[2],
                'address': row[3],
                'courier_name': row[4],
                'last_status': row[5],
                'status_date': row[6],
                'cost': str(row[7]),
            })
        return jsonify(data_dict)    
    return "-1"

@app.route('/post_order/<string:email>/<string:password>', methods=["POST"])
def post_order(email, password):
    if not request.json:
        print(request.json)
        abort(400)
    d = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from clients where email=%s and password=%s""", [email, password])
    data = cursor.fetchall()
    data_dict = []
    print(len(data))
    if len(data) > 0:
        try:
            client_id = data[0][0]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO addresses (id_client, str_adr, comment, full_name, geo_code_1, geo_code_2, phone)
                                VALUES (%s, %s, %s, %s, %s, %s, %s);""", [client_id, d["sender"]["str_adr"], d["sender"]["comment"], d["sender"]["name"], d["sender"]["coord1"], d["sender"]["coord2"], d["sender"]["phone"]])
            conn.commit()
            cursor.execute("""SELECT max(id) from addresses""")
            id_from = cursor.fetchall()[0][0]
            cursor.execute("""INSERT INTO addresses (id_client, str_adr, comment, full_name, geo_code_1, geo_code_2, phone)
                                VALUES (%s, %s, %s, %s, %s, %s, %s);""", [client_id, d["receiver"]["str_adr"], d["receiver"]["comment"], d["receiver"]["name"], d["receiver"]["coord1"], d["receiver"]["coord2"], d["receiver"]["phone"]])
            conn.commit()
            cursor.execute("""SELECT max(id) from addresses""")
            id_to = cursor.fetchall()[0][0]
            cursor.execute("""INSERT INTO orders (client_id, courier_id, sent_from_id, sent_to_id, order_date, cost)
                                VALUES (%s, null, %s, %s, DEFAULT, %s);""", [client_id, id_from, id_to, d["cost"]])
            conn.commit()
            cursor.execute("""SELECT max(order_num) from orders""")
            data = cursor.fetchall()
            if len(data) > 0:
                cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Заказ создан', DEFAULT, null, %s);""", [data[0][0]])
                conn.commit()
                print(str(data[0][0]))                    
                return str(data[0][0])
            else:
                return "0"
        except Exception as e:
            return str(e)

@app.route('/get_courier_free_orders/<string:phone_num>/<string:password>')
def get_courier_free_orders(phone_num, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select order_num_from, adr_from, geo_code_1_from, geo_code_2_from from courier_orders where courier_id is null")            
        data = cursor.fetchall()
        for row in data:
            data_dict.append({
                'order_num': row[0],
                'adr': row[1],
                'geo_code_1': row[2],
                'geo_code_2': row[3]
            })
        return jsonify(data_dict)    
    return "-1"

@app.route('/get_order_details/<string:phone_num>/<string:password>/<int:order_num>')
def get_order_details(phone_num, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select order_num_from, adr_from, geo_code_1_from, geo_code_2_from, adr_to, geo_code_1_to, geo_code_2_to, full_name_from, full_name_to from courier_orders where order_num_from=%s", [int(order_num)])            
        data = cursor.fetchall()
        for row in data:
            data_dict.append({
                'order_num': row[0],
                'adr_from': row[1],
                'geo_code_1_from': row[2],
                'geo_code_2_from': row[3],
                'adr_to': row[4],
                'geo_code_1_to': row[5],
                'geo_code_2_to': row[6],
                'full_name_from': row[7],
                'full_name_to': row[8]
            })
        return jsonify(data_dict)    
    return "-1"

@app.route('/get_order_details_client/<string:email>/<string:password>/<int:order_num>')
def get_order_details_client(email, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from clients where email=%s and password=%s""", [email, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select order_num_from, adr_from, geo_code_1_from, geo_code_2_from, adr_to, geo_code_1_to, geo_code_2_to, full_name_from, full_name_to, phone_from, phone_to, cost, ifnull(courier_id, 0) as courier_id, order_date, client_id from order_details where order_num_from=%s and client_id=%s", [int(order_num), data[0][0]])            
        data = cursor.fetchall()
        for row in data:
            data_dict.append({
                'order_num': row[0],
                'adr_from': row[1],
                'geo_code_1_from': row[2],
                'geo_code_2_from': row[3],
                'adr_to': row[4],
                'geo_code_1_to': row[5],
                'geo_code_2_to': row[6],
                'full_name_from': row[7],
                'full_name_to': row[8],
                'phone_from': row[9],
                'phone_to': row[10],
                'cost': str(row[11]),
                'courier_id': row[12],
                'order_date': row[13]
            })
        return jsonify(data_dict)    
    return "-1"

@app.route('/take_order/<string:phone_num>/<string:password>/<int:order_num>')
def take_order(phone_num, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from orders where order_num=%s and courier_id is null", [int(order_num)])            
        data = cursor.fetchall()
        if len(data) > 0:
            #try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("""UPDATE orders SET courier_id = 1 WHERE order_num = %s;""", [int(order_num)])
                cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Курьер найден', DEFAULT, null, %s);""", [int(order_num)])
                conn.commit() 
                return "1"
            #except:
                return "-3"
        else:
            return "-2"   
    return "-1"



@app.route('/take_parcel/<string:phone_num>/<string:password>/<int:order_num>')
def take_parcel(phone_num, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from orders where order_num=%s and courier_id = %s", [int(order_num), data[0][0]])            
        data = cursor.fetchall()
        if len(data) > 0:
            #try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Посылка принята курьером', DEFAULT, null, %s);""", [int(order_num)])
                conn.commit() 
                return "1"
            #except:
                return "-3"
        else:
            return "-2"   
    return "-1"

@app.route('/close_order/<string:phone_num>/<string:password>/<int:order_num>')
def close_order(phone_num, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from orders where order_num=%s and courier_id = %s", [int(order_num), data[0][0]])            
        data = cursor.fetchall()
        if len(data) > 0:
            #try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO order_statuses (order_status, status_date, status_reason, order_num)
                                    VALUES ('Заказ выполнен', DEFAULT, null, %s);""", [int(order_num)])
                conn.commit() 
                return "1"
            #except:
                return "-3"
        else:
            return "-2"   
    return "-1"

@app.route('/send_location/<string:phone_num>/<string:password>', methods=['POST'])
def send_location(phone_num, password):
    if not request.json:
        print(request.json)
        abort(400)
    d = request.json
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
    data = cursor.fetchall()
    data_dict = []
    if len(data) > 0:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            # Запрос на поиск пользователя
            cursor.execute("""INSERT INTO couriers_locations (id_courier, time, location_1, location_2) 
                VALUES (%s, DEFAULT, %s, %s)""", [data[0][0], d["geo_code_1"], d["geo_code_2"]])
            conn.commit()
            return "1"
        except:
            return "-3"
    else:
        return "-1"

@app.route('/save_sign/<string:phone_num>/<string:password>/<int:order_num>', methods=['POST'])
def save_sign(phone_num, password, order_num):
    try:
        # Если пришёл не JSON - возвращаем HTTP ошибку 400
        if not request.json:
            print(request.json)
            abort(400)
        d = request.json
        conn = mysql.connect()
        cursor = conn.cursor()
        # Запрос на поиск пользователя
        cursor.execute("""select id from couriers where phone_num=%s and password=%s""", [phone_num, password])
        data = cursor.fetchall()
        data_dict = []
        if len(data) > 0:
            import base64
            filepath = "/home/std/TPIS/signs/" + str(order_num) + ".png"
            with open(filepath, "wb") as fh:
                fh.write(base64.decodebytes(d["sign_file"].encode()))
            key = open("/home/std/TPIS/key.key", "rb").read()
            f = Fernet(key)
            with open(filepath, "rb") as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)
            with open(filepath, "wb") as file:
                file.write(encrypted_data)
            return take_parcel(phone_num, password, order_num)
        else:
            return "-1"
        return "-1"
    except Exception as e:
        return str(e)


@app.route('/send_email/<string:email>/<string:password>/<int:order_num>')
def send_email(email, password, order_num):
    conn = mysql.connect()
    cursor = conn.cursor()
    # Запрос на поиск пользователя
    cursor.execute("""select order_num, full_name, email, clients.id 
                    from orders, clients 
                    where orders.client_id = clients.id and order_num =%s and email = %s and password = %s""", [order_num, email, password])
    data = cursor.fetchall()
    if len(data) > 0:
        try:
            import datetime
            name=data[0][1]
            now = datetime.datetime.now()
            date=str(now.day)+str(now.month)+str(now.year)
            filename=str(data[0][3])+"_"+str(date)+"_"+str(data[0][0])
            my_file = open("/home/std/TPIS/templates/"+ filename+".txt", "w+")
            my_file.write('Договор на оказание платных услуг\n'+'Дата и время совершения заказа: '+str(now)+'\n'+'Отправитель: '+name)
            my_file.close()

            import smtplib
            from email.mime.multipart import MIMEMultipart
            HOST = "smtp.gmail.com" # Из настроек твоей почты (smtp сервер)
            SUBJECT = "Договор на оказание услуг" # Тема письма
            TO = data[0][2]
            FROM = "amrrchnk@gmail.com" # Твой адрес - от кого
            text = "Договор на оказание услуг"
            from email.message import EmailMessage

            msg = EmailMessage()
            msg['Subject'] = SUBJECT
            msg['From'] = FROM
            msg['To'] = TO
            msg.add_attachment(open(my_file.name, "r").read(), filename=filename)

            server = smtplib.SMTP(HOST, 587)
            server.starttls()
            server.login("amrrchnk@gmail.com", "D2eM6n12A") 
            server.sendmail(FROM, TO, msg.as_string())
            server.quit()
            return "1"
        except Exception as e:
            return str(e)
    return "-1"

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

# Добавление заголовка для корректной работы CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    #response.headers.add('Access-Control-Allow-Origin', 'http://tpis-site.std-913.ist.mospolytech.ru')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



# Точка входа
if __name__ == '__main__':
    app.run()
