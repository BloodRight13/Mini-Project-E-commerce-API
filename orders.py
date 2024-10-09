from flask import jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from mysql.connector import Error
from app import ma
from databse_connection import get_db_connection


class OrderSchema(ma.Schema):
    customer_id = fields.String(required=True)
    product_number = fields.String(required=True, many = True)
    class Meta:
        fields = ('customer_id', 'product_number', 'order_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

def get_orders():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary = True)

        query = 'SELECT * FROM Orders'

        cursor.execute(query)

        orders = cursor.fetchall()

        return orders_schema.jsonify(orders)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_orders():
    try:
        order_data = order_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    # Add order
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        new_order = (order_data['customer_id'], order_data['product_id'])

        query = "INSERT INTO Orders (customer_id, product_id) VALUES (%s, %s)"

        cursor.execute(query, new_order)
        conn.commit()

        return jsonify({'message': 'New order added successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def update_order(order_id):
    try:
        order_data = order_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    #Update Order
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        updated_order = (order_data['customer_id'], order_data['product_id'], order_id)

        query = 'UPDATE Orders SET customer_id = %s, product_id = %s WHERE order_id = %s'

        cursor.execute(query, updated_order)
        conn.commit()

        return jsonify({'message': 'Updated order successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def delete_orders(order_id):    
    #Delete Order
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        order_to_remove = (order_id,) #is a tuple comma is needed

        cursor.execute('SELECT * FROM Orders where order_id = %s', order_to_remove)
        order = cursor.fetchone()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        query = "DELETE FROM Orders WHERE order_id = %s"
        cursor.execute(query, order_to_remove)
        conn.commit()
        
        return jsonify({'message': 'Order removed successfully'}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()