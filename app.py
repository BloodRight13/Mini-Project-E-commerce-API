from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from customers import get_customers, add_customer, update_customer, delete_customer
from orders import get_orders, add_orders, update_orders, delete_orders
from products import get_products, add_products, update_products, delete_products



app = Flask(__name__)
ma = Marshmallow(app)

@app.route('/') # This is the default route in web servers
def home():
    return 'Welcome to the Flask Music Festival'

@app.route('/customers', methods = ["GET"])
def funciton():
    get_customers()

@app.route('/customers', methods = ["POST"])
def funciton():
    add_customer()

@app.route('/customers/<int:id>', methods = ["POST"])
def funciton():
    update_customer(id)

@app.route('/customers/<int:id>', methods = ["POST"])
def funciton():
    delete_customer(id)

@app.route('/orders', methods = ["POST"])
def funciton():
    get_orders()

@app.route('/orders', methods = ["POST"])
def funciton():
    add_orders()

@app.route('/orders/<int:order_id>', methods = ["POST"])
def funciton():
    update_orders()

@app.route('/orders/<int:order_id>', methods = ["POST"])
def funciton():
    delete_orders()

@app.route('/products', methods = ["POST"])
def funciton():
    get_products()

@app.route('/products', methods = ["POST"])
def funciton():
    add_products()

@app.route('/products/<int:product_number>', methods = ["POST"])
def funciton():
    update_products()

@app.route('/products/<int:product_number>', methods = ["POST"])
def funciton():
    delete_products()
