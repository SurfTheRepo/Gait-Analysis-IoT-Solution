from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from json import dumps
import pymysql
# Will use in configuration and class code.
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# database
db = pymysql.connect('database-1.cdezsf3cj776.us-east-2.rds.amazonaws.com', 'mgysel', '205LeBron!205')
cursor = db.cursor()

# Use gait_data database
sql = '''use gait_data'''
cursor.execute(sql)

def insert_details(ip_address,mean,median,skewness,standard_deviation):
    sql = '''
    insert into user(ip_address, mean, median, skewness, standard_deviation) values('%s', '%s', '%s', '%s', '%s')
    ''' % ('127.0.0.1', 1.1, 1.2, 1.3, 1.4)
    cursor.execute(sql)
    db.commit()

def get_details():
    sql = '''select * from user'''
    cursor.execute(sql)
    details = cursor.fetchall()
    return details

@app.route('/')
def index():
    return render_template('index.html')

'''
Displays input data received
Used to test that data can be sent from SensorTag
'''
@app.route('/inputData', methods=['POST'])
def input_data():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return render_template('inputdata.html', var=data)
        #return dumps(data)


'''
Inserts ip_address, mean, median, skewness, and standard_deviation data into database
Used to test database functionality
'''
@app.route('/insert',methods = ['post'])
def insert():
    if request.method == 'POST':
        ip_address = request.form['ip_address']
        mean = request.form['mean']
        median = request.form['median']
        skewness = request.form['skewness']
        standard_deviation = request.form['standard_deviation']
        insert_details(ip_address, mean, median, skewness, standard_deviation)
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
    app.debug = True
    app.run(host='127.0.0.1', port=8003)
    #app.run()