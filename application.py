from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from json import dumps
import pymysql
# Will use in configuration and class code.
from sqlalchemy.ext.declarative import declarative_base

application = Flask(__name__)

# database
db = pymysql.connect('database-1.cdezsf3cj776.us-east-2.rds.amazonaws.com', 'mgysel', '205LeBron!205')
cursor = db.cursor()

# Use gait_data database
sql = '''use gait'''
cursor.execute(sql)

def insert_details(ip_address,mean,median,skewness,standard_deviation,data):
    sql = '''
    insert into user(ip_address, mean, median, skewness, standard_deviation, data) values('%s', '%s', '%s', '%s', '%s', '%s')
    ''' % (ip_address, mean, median, skewness, standard_deviation, data)
    cursor.execute(sql)
    db.commit()

def get_details():
    sql = '''select * from user'''
    cursor.execute(sql)
    details = cursor.fetchall()
    return details

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        details = get_details()
        return render_template('index.html', var=details)
    elif request.method == 'POST':
        ip_address = request.remote_addr
        data = dumps(request.get_json())
        insert_details(ip_address, 100, 100, 1, 1, data)
        print(ip_address)
        print(f'Data: {data}')
        #return render_template('inputdata.html', var=data)
        details = get_details()
        print(details)
        return render_template('index.html',var=details)

'''
Displays input data received
Used to test that data can be sent from SensorTag
'''
@application.route('/inputData', methods=['POST'])
def input_data():
    if request.method == 'POST':
        ip_address = request.remote_addr
        data = request.get_json()
        insert_details(ip_address, 100, 100, 1, 1, 'data')
        print(ip_address)
        print(data)
        #return render_template('inputdata.html', var=data)
        return dumps(data)

'''
Inserts ip_address, mean, median, skewness, and standard_deviation data into database
Used to test database functionality
'''
@application.route('/insert',methods = ['POST'])
def insert():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        mean = request.form['mean']
        median = request.form['median']
        skewness = request.form['skewness']
        standard_deviation = request.form['standard_deviation']
        data = request.form['data']
        insert_details(ip_address, mean, median, skewness, standard_deviation, data)
        details = get_details()
        print(details)
        '''
        for detail in details:
            var = detail
            print(f"Data: {detail}")
        '''
        return render_template('index.html',var=details)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    #application.run(host='127.0.0.1', port=8004)
    application.run()
    #application.run(host='0.0.0.0')