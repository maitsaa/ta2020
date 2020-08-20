from flask import Flask, render_template, jsonify, request, redirect, url_for, session, logging, flash
from flask_mysqldb import MySQL,MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit
import json 

import datetime
import random
import time
engine = create_engine("mysql+pymysql://tajsn2020:ta2020@localhost/monitoringdb")
db = scoped_session(sessionmaker(bind=engine))
#from flask.ext.socketio import SocketIO, emit

import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tajsn2020'
app.config['MYSQL_PASSWORD'] = 'ta2020'
app.config['MYSQL_DB'] = 'monitoringdb'
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

data = [0,0,'00:00:00']
mysql = MySQL(app)

def begin_mysql_connection():
    conn = mysql.connector.connect(host='localhost',database='monitoringdb',user='tajsn2020',password='ta2020')
    return conn

#main route
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur3 = mysql.connection.cursor()
    cur4 = mysql.connection.cursor()
    cur5 = mysql.connection.cursor()
    cur.execute("SELECT fusi_temperature from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur2.execute("SELECT fusi_humidity from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur3.execute("SELECT fusi_co from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur4.execute("SELECT fusi_co2 from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur5.execute("SELECT Kualitas_udara from fusi where fusi_id in (select max(fusi_id) from fusi)")
    
    data = cur.fetchall()
    data2 = cur2.fetchall()
    data3 = cur3.fetchall()
    data4 = cur4.fetchall()
    data5 = cur5.fetchall()
    cur.close()
    cur2.close()
    cur3.close()
    cur4.close()
    cur5.close()
    return render_template('index.html', value2 = data2, value=data, value3=data3, value4=data4, value5=data5)

@app.route("/monitoring_login")
def monitoring_login():
    cur = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur3 = mysql.connection.cursor()
    cur4 = mysql.connection.cursor()
    cur5 = mysql.connection.cursor()
    cur.execute("SELECT fusi_temperature from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur2.execute("SELECT fusi_humidity from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur3.execute("SELECT fusi_co from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur4.execute("SELECT fusi_co2 from fusi where fusi_id in (select max(fusi_id) from fusi)")
    cur5.execute("SELECT Kualitas_udara from fusi where fusi_id in (select max(fusi_id) from fusi)")
    data = cur.fetchall()
    data2 = cur2.fetchall()
    data3 = cur3.fetchall()
    data4 = cur4.fetchall()
    data5 = cur5.fetchall()
    cur.close()
    cur2.close()
    cur3.close()
    cur4.close()
    cur5.close()
    return render_template('monitoring_login.html', value2 = data2, value=data, value3=data3, value4=data4, value5=data5)

@app.route("/database")
def Node1():
    cur = mysql.connection.cursor()
    cur.execute("select Node1.DATE, Node1.TX, Node1.RSSI, Node1.temperature, Node1.humidity, Node1.co, Node1.co2, Node1.from_node, Node2.DATE, Node2.TX_2, Node2.RSSI_2, Node2.temperature_2, Node2.humidity_2, Node2.co_2, Node2.co2_2, Node2.from_node_2, Node3.DATE, Node3.TX_3, Node3.RSSI_3, Node3.temperature_3, Node3.humidity_3, Node3.co_3, Node3.co2_3, Node3.from_node_3, Node4.DATE, Node4.TX_4, Node4.RSSI_4, Node4.temperature_4, Node4.humidity_4, Node4.co_4, Node4.co2_4, Node4.from_node_4 FROM Node1 INNER JOIN Node2, Node3, Node4")
    data = cur.fetchall()
    cur.close()
    return render_template('database.html', value=data)

@app.route("/login")
def login():
    return render_template("login.html", tittle="data")

@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/tabel_login")
def tabel_login():
    cur = mysql.connection.cursor()
    cur.execute("select Node1.DATE, Node1.TX, Node1.RSSI, Node1.temperature, Node1.humidity, Node1.co, Node1.co2, Node1.from_node, Node2.DATE, Node2.TX_2, Node2.RSSI_2, Node2.temperature_2, Node2.humidity_2, Node2.co_2, Node2.co2_2, Node2.from_node_2, Node3.DATE, Node3.TX_3, Node3.RSSI_3, Node3.temperature_3, Node3.humidity_3, Node3.co_3, Node3.co2_3, Node3.from_node_3, Node4.DATE, Node4.TX_4, Node4.RSSI_4, Node4.temperature_4, Node4.humidity_4, Node4.co_4, Node4.co2_4, Node4.from_node_4 FROM Node1 INNER JOIN Node2, Node3, Node4")
    data = cur.fetchall()
    cur.close()
    return render_template("tabel_login.html", value=data)

@app.route("/checkUser", methods=["POST"])
def check():
    confirm = None
    username = str(request.form["username"])
    password = str(request.form["password"])
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username='" + username + "' and password='" + password + "'")
    data = cur.fetchone()
    
    if data is None:
        
        return (render_template("login.html"))
    else:
        return redirect(url_for("tabel_login"))

@app.route('/delete', methods=['GET','POST'])
def delete():
    cur = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur3 = mysql.connection.cursor()
    cur4 = mysql.connection.cursor()
    cur5 = mysql.connection.cursor()
    cur.execute("DELETE FROM Node1")
    cur2.execute("DELETE FROM Node2")
    cur3.execute("DELETE FROM Node3")
    cur4.execute("DELETE FROM Node4")
    cur5.execute("DELETE FROM fusi")
    mysql.connection.commit()
    return redirect(url_for('tabel_login'))

def get_data_1():
#     cur = mysql.connection.cursor()
#     #cur.execute("select Node1.DATE, Node1.TX, Node1.RSSI, Node1.temperature, Node1.humidity, Node1.co, Node1.co2, Node1.from_node, Node2.DATE, Node2.TX_2, Node2.RSSI_2, Node2.temperature_2, Node2.humidity_2, Node2.co_2, Node2.co2_2, Node2.from_node_2, Node3.DATE, Node3.TX_3, Node3.RSSI_3, Node3.temperature_3, Node3.humidity_3, Node3.co_3, Node3.co2_3, Node3.from_node_3, Node4.DATE, Node4.TX_4, Node4.RSSI_4, Node4.temperature_4, Node4.humidity_4, Node4.co_4, Node4.co2_4, Node4.from_node_4 FROM Node1 INNER JOIN Node2, Node3, Node4")
#     cur.execute("select TX FROM Node1")
#     data = cur.fetchall()
#     cur.close()
#     return data

    data = [random.randint(0,100), random.randint(0,100)]
    return data

@socketio.on('status')
def tes_message(message):
    emit('data-receiver', data)

@socketio.on('data-access-new')
def access_new_data(latest_data):
    data = get_data_1()
    data.append(timenow)
    time.sleep(1)
    emit('data-receiver', data)
  
if __name__ == "__main__":
    app.secret_key="12345678dailywebcoding"
    app.run(host="0.0.0.0", port=5000, debug=True)
