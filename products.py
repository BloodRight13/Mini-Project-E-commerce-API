from flask import jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from mysql.connector import Error
from app import ma
from databse_connection import get_db_connection


class ProductSchema(ma.Schema):
    price = fields.String(required=True)

    class Meta:
        fields = ('price', 'product_number')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


def get_products():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary = True)

        query = 'SELECT * FROM Products'

        cursor.execute(query)

        products = cursor.fetchall()

        return products_schema.jsonify(products)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_products():
    try:
        product_data = product_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    # Add Product
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        new_product = (product_data['price'])

        query = "INSERT INTO Products (price) VALUES (%s)"

        cursor.execute(query, new_product)
        conn.commit()

        return jsonify({'message': 'New product added successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def update_products(product_number):
    try:
        product_data = product_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    #Update Products
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        updated_product = (product_data['price'], product_number)

        query = 'UPDATE Products SET price = %s WHERE product_number = %s'

        cursor.execute(query, updated_product)
        conn.commit()

        return jsonify({'message': 'Updated product successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def delete_products(product_number):    
    #Delete product
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        product_to_remove = (product_number,) #is a tuple comma is needed

        cursor.execute('SELECT * FROM Products where product_number = %s', product_to_remove)
        product = cursor.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        query = "DELETE FROM Products WHERE id = %s"
        cursor.execute(query, product_to_remove)
        conn.commit()
        
        return jsonify({'message': 'Product removed successfully'}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()