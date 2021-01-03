# Functions and variables
import os
import sys
# Come in handy when writing mapper code
from sqlalchemy import Column, ForeignKey, Integer, Float, String
# Will use in configuration and class code.
from sqlalchemy.ext.declarative import declarative_base
# Create foreign key relationship, for mapper
from sqlalchemy.orm import relationship
# Use in config code
from sqlalchemy import create_engine
# Used to create secret_key
import random
import string
import mysql.connector
import pymysql

# make instance of declarative_base() class
# Will let sqlalchemy know that classes are special SQL alchemy classes
# that correspond to tables in database.
Base = declarative_base()

# CLASS
# Classes that represent each table
class User(Base):
	# TABLE
	# Represenation of our table inside the database
	__tablename__ = 'UserData'
	# MAPPER
	# email, username, and password columns with 80 character max, required
	# id column, primary key
	id = Column(
		Integer,
		primary_key = True
		)
	ip_address = Column(
		String,
		unique = True,
		nullable = False
		)
	mean = Column(
		Float,
		nullable = False
		)
	median = Column(
		Float,
		nullable = False
		)
	skewness = Column(
		Float,
		nullable = False
		)
	standard_deviation = Column(
		Float,
		nullable = False
		)

#####INSERT AT END OF FILE######
connection_string = ""


# Create instance of create_engine class
# and point to database we will use
# sqlite will create new engine file below
engine = create_engine(connection_string)

# Goes into database and adds classes that we will soon create
# as new tables in database
Base.metadata.create_all(engine)
