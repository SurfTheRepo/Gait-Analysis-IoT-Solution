#import pandas as pd
import sqlalchemy 
import mysql.connector
#"mysql+mysqlconnector://mgysel:205LeBron!205@database-1.cdezsf3cj776.us-east-2.rds.amazonaws.com:3306"
#mysql_engine = sqlalchemy.create_engine("mysql://username:password@dbname.xxxxxxxxxxxx.eu-central-1.rds.amazonaws.com:3306")

#pd.read_sql_query("create database dbname", con=mysql_engine)

mydb = mysql.connector.connect(
  host="database-1.cdezsf3cj776.us-east-2.rds.amazonaws.com",
  user="mgysel",
  password="205LeBron!205",
  database="database-1"
)