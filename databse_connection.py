from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

def get_db_connection():
   """Connect to the MySQL database and return the connection object"""
   db_name = 'grocery_store_db'
   user = 'root'
   password = 'your password'
   host ='localhost'
   
   try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print('Connected to MySQL database successfully')
        return conn
   
   except Error as e:
        print(f"Error: {e}")
        return None

