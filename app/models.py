import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# MySQL connection configuration
db_config = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

class Admin:
    def __init__(self, admin_name, admin_email, admin_password, whatsapp_number=None,id=None, created_at=None):
        self.id = id
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.whatsapp_number = whatsapp_number
        self.created_at = created_at or datetime.now()
        
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                admin_name VARCHAR(255) NOT NULL,
                admin_email VARCHAR(255) NOT NULL UNIQUE,
                admin_password VARCHAR(255) NOT NULL,
                whatsapp_number VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_admin(admin_name, admin_email, admin_password, whatsapp_number=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO admins (admin_name, admin_email, admin_password, whatsapp_number)
            VALUES (%s, %s, %s, %s)
        ''', (admin_name, admin_email, admin_password, whatsapp_number))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_admins():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT admin_name, admin_email, whatsapp_number, created_at FROM admins')
        admins = cursor.fetchall()
        cursor.close()
        conn.close()
        return admins
    
    @staticmethod
    def get_by_id(admin_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE id = %s', (admin_id,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        return admin
    
    @staticmethod
    def delete_admin(admin_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE id = %s', (admin_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def view_info(admin_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE id = %s', (admin_id,))
        admin_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return admin_info
    
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE admin_email = %s', (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        return admin
    
    
class Users:
    def __init__(self, user_name, email, password, company_name=None, whatsapp_number=None, id=None, registered_on=None, calls_made=0):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.company_name = company_name
        self.whatsapp_number = whatsapp_number
        self.registered_on = registered_on or datetime.now()
        self.calls_made = calls_made
        
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                registered_on DATETIME DEFAULT CURRENT_TIMESTAMP,
                company_name VARCHAR(255),
                whatsapp_number VARCHAR(20),
                calls_made INT DEFAULT 0
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_user(user_name, email, password, company_name=None, whatsapp_number=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_name, email, password, company_name, whatsapp_number)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_name, email, password, company_name, whatsapp_number))
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def get_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    
    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, user_name, email, registered_on, company_name, whatsapp_number, calls_made FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE users, user_call_data, calls
            FROM users
            LEFT JOIN user_call_data ON users.id = user_call_data.user_id
            LEFT JOIN calls ON users.id = calls.user_id
            WHERE users.id = %s
        ''', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def update_user_info(user_id, user_name, email, company_name=None, whatsapp_number=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET user_name = %s, email = %s, company_name = %s, whatsapp_number = %s
            WHERE id = %s
        ''', (user_name, email, company_name, whatsapp_number, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_user_info(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user_info = cursor.fetchone()
        cursor.close()
        conn.close()
        return user_info
    
class UserCallData:
    def __init__(self, user_id, twilio_phone_number, dataset, greeting_message='Hello! This is an AI Assistant. How may I help you?', id=None):
        self.id = id
        self.user_id = user_id
        self.twilio_phone_number = twilio_phone_number
        self.dataset = dataset
        self.greeting_message = greeting_message
        
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_call_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                twilio_phone_number VARCHAR(20),
                dataset TEXT,
                greeting_message TEXT DEFAULT 'Hello! This is an AI Assistant. How may I help you?',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_user_call_data(user_id, twilio_phone_number, dataset, greeting_message='Hello! This is an AI Assistant. How may I help you?'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_call_data (user_id, twilio_phone_number, dataset, greeting_message)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, twilio_phone_number, dataset, greeting_message))
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def get_user_call_data(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_call_data WHERE user_id = %s', (user_id,))
        call_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return call_data
    
    @staticmethod
    def update_dataset(user_id, dataset):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_call_data
            SET dataset = %s
            WHERE user_id = %s
        ''', (dataset, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_user_dataset(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT dataset FROM user_call_data WHERE user_id = %s', (user_id,))
        dataset = cursor.fetchone()
        cursor.close()
        conn.close()
        return dataset['dataset'] if dataset else None
    
    @staticmethod
    def update_greeting_message(user_id, greeting_message):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_call_data
            SET greeting_message = %s
            WHERE user_id = %s
        ''', (greeting_message, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_user_greeting_message(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT greeting_message FROM user_call_data WHERE user_id = %s', (user_id,))
        greeting_message = cursor.fetchone()
        cursor.close()
        conn.close()
        return greeting_message['greeting_message'] if greeting_message else None
    
class Calls:
    def __init__(self, user_id, receiver_phone, call_type, conversation_history=None, ai_transmission_message=None, callback_status='no', call_done=False, call_timestamp=None, id=None, receiver_name=None):
        self.id = id
        self.user_id = user_id
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.call_type = call_type
        self.conversation_history = conversation_history or ''
        self.ai_transmission_message = ai_transmission_message or ''
        self.callback_status = callback_status
        self.call_done = call_done
        self.call_timestamp = call_timestamp or datetime.now()
        
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                receiver_name VARCHAR(255),
                receiver_phone VARCHAR(20) NOT NULL,
                call_type ENUM('1way', '2way') NOT NULL,
                conversation_history TEXT,
                ai_transmission_message TEXT,
                callback_status ENUM('yes', 'no', 'callback_done', 'callback_needed') DEFAULT 'no',
                call_done BOOLEAN DEFAULT FALSE,
                call_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_call(user_id, receiver_phone, call_type, conversation_history=None, ai_transmission_message=None, callback_status='no', call_done=False, receiver_name=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO calls (user_id, receiver_phone, call_type, conversation_history, ai_transmission_message, callback_status, call_done, receiver_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, receiver_phone, call_type, conversation_history, ai_transmission_message, callback_status, call_done, receiver_name))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_calls(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM calls WHERE user_id = %s', (user_id,))
        calls = cursor.fetchall()
        cursor.close()
        conn.close()
        return calls
    
    @staticmethod
    def update_call_status(call_id, callback_status, call_done):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE calls
            SET callback_status = %s, call_done = %s
            WHERE id = %s
        ''', (callback_status, call_done, call_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_bulk_calls(calls_data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO calls (user_id, receiver_phone, call_type, conversation_history, ai_transmission_message, callback_status, call_done, receiver_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', calls_data)
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def filter_calls(user_id, filter_type):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if filter_type == 'all':
            cursor.execute('SELECT * FROM calls WHERE user_id = %s', (user_id,))
        else:
            cursor.execute('SELECT * FROM calls WHERE user_id = %s AND callback_status = %s', (user_id, filter_type))
        filtered_calls = cursor.fetchall()
        cursor.close()
        conn.close()
        return filtered_calls
    
    
    
    
class Credits:
    def __init__(self, user_id, credits, id=None):
        self.id = id
        self.user_id = user_id
        self.credits = credits
        
    @staticmethod
    def create_table():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                credits INT DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def add_credits(user_id, credits):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO credits (user_id, credits)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE credits = credits + %s
        ''', (user_id, credits, credits))
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def get_credits(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT credits FROM credits WHERE user_id = %s', (user_id,))
        credits = cursor.fetchone()
        cursor.close()
        conn.close()
        return credits['credits'] if credits else 0
    
    @staticmethod
    def deduct_credits(user_id, credits):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE credits
            SET credits = credits - %s
            WHERE user_id = %s AND credits >= %s
        ''', (credits, user_id, credits))
        if cursor.rowcount == 0:
            raise ValueError("Insufficient credits")
        conn.commit()
        cursor.close()
        conn.close()
        
    @staticmethod
    def reset_credits(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE credits
            SET credits = 0
            WHERE user_id = %s
        ''', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()