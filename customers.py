from flask import jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from mysql.connector import Error
from app import ma
from databse_connection import get_db_connection

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ('name', 'email', 'phone', 'id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


def get_customers():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor(dictionary = True)

        query = 'SELECT * FROM Customers'

        cursor.execute(query)

        customers = cursor.fetchall()

        return customers_schema.jsonify(customers)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_customer():
    try:
        customer_data = customer_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    # Add customer
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone'])

        query = "INSERT INTO Customers (name, email, phone) VALUES (%s, %s, %s)"

        cursor.execute(query, new_customer)
        conn.commit()

        return jsonify({'message': 'New customer added successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json) # Recieve data
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    #Update Customer
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        updated_customer = (customer_data['name'], customer_data['email'], customer_data['phone'], id)

        query = 'UPDATE Customers SET name = %s, email = %s, phone = %s WHERE id = %s'

        cursor.execute(query, updated_customer)
        conn.commit()

        return jsonify({'message': 'Updated Customer successfully'}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()


def delete_customer(id):    
    #Delete Customer
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
    
        customer_to_remove = (id,) #is a tuple comma is needed

        cursor.execute('SELECT * FROM Customers where id = %s', customer_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        query = "DELETE FROM Customers WHERE id = %s"
        cursor.execute(query, customer_to_remove)
        conn.commit()
        
        return jsonify({'message': 'Customer removed successfully'}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error' : 'Internal Server Error' }), 500
    
    finally:
         if conn and conn.is_connected():
            cursor.close()
            conn.close()