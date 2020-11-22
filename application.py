from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from json import dumps
import pymysql
import re
# Will use in configuration and class code.
from sqlalchemy.ext.declarative import declarative_base
from app_ml import classify

application = Flask(__name__)

# database
db = pymysql.connect('database-1.cdezsf3cj776.us-east-2.rds.amazonaws.com', 'mgysel', '205LeBron!205')
cursor = db.cursor()

# Use gait_data database
sql = '''use gait'''
cursor.execute(sql)

'''
Insert details into user gait database
'''
def insert_details(ip_address,data):
    sql = '''
    insert into user_gait_data(ip_address, data) values('%s', '%s')
    ''' % (ip_address, data)
    cursor.execute(sql)
    db.commit()

'''
Get details from user gait database
'''
def get_details():
    sql = '''select * from user_gait_data'''
    cursor.execute(sql)
    details = cursor.fetchall()
    return details

'''
Gives last gait verification value
'''
def get_last_detail():
    sql = '''SELECT * FROM user_gait_data ORDER BY ID DESC LIMIT 1'''
    cursor.execute(sql)
    details = cursor.fetchall()
    return details[0][2]

'''
Page to display data in database
'''
@application.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        details = get_details()
        return render_template('index.html', var=details)
    elif request.method == 'POST':
        # Get data
        raw_data = request.get_json()

        # Parse data
        ip_address = raw_data['ip_address']
        data = raw_data['data']

        '''
        # TODO - Clean data
        # 1. Turn data into ax, ay, az
        # 2. Check who data is
        '''
        # Insert data into database
        insert_details(ip_address, data)

        # Return index page with variables
        print(f'IP Address: {ip_address}')
        print(f'Data: {data}')
        #return render_template('inputdata.html', var=data)
        details = get_details()
        print(details)
        return render_template('index.html',var=details)

'''
Application homepage
'''
@application.route('/homepage', methods=['GET'])
def homepage():
    if request.method == 'GET':
        details = get_details()
        return render_template('homepage.html', var=details)

'''
Inserts ip_address and raw data into database
Used to test database functionality
'''
@application.route('/insert',methods = ['GET','POST'])
def insert():
    if request.method == 'GET':
        details = get_details()
        return render_template('inputdata.html',var=details)
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        data = request.form['data']
        insert_details(ip_address, data)
        details = get_details()
        print(details)
        '''
        for detail in details:
            var = detail
            print(f"Data: {detail}")
        '''
        return render_template('index.html',var=details)

'''
Authenticates user data sent 
'''
@application.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        detail = get_last_detail()
        return render_template('results.html', var=detail)
    if request.method == 'POST':
        # Get data
        raw_data = request.get_json()

        # Parse data
        ip_address = raw_data['ip_address']
        data = raw_data['data']

        template = re.compile('ax(-?\d+)ay(-?\d+)az(-?\d+)gx(-?\d+)gy(-?\d+)gz(-?\d+)')
        readings = template.findall(data)

        ax_array = []
        ay_array = []
        az_array = []
        gx_array = []
        gy_array = []
        gz_array = []
        sqrsTotal = []
        for line in readings:
            ax, ay, az, gx, gy, gz = line
            ax_array.append(int(ax))
            ay_array.append(int(ay))
            az_array.append(int(az))
            gx_array.append(int(gx))
            gy_array.append(int(gy))
            gz_array.append(int(gz))
            sqrsTotal.append(int(ax)**2 +int(ay)**2 +int(az)**2)

        results = classify(ax_array, ay_array, az_array)
        #results = ax_array
        print(results)

        if (results):
            who = "Otto"
        else:
            who = "Hasaru"

        insert_details('ip_address', who)
        return render_template('results.html', var=who)
        # Test data with ML algorithm
        # TEST ML HERE

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='127.0.0.1', port=8011)
    #application.run()
    #application.run(host='0.0.0.0')