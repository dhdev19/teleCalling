from flask import Flask
from app.models import Admin, Users, UserCallData, Calls, Credits
from flask_cors import CORS
import os
from dotenv import load_dotenv
# import pymysql


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

with app.app_context():
    Admin.create_table()
    Users.create_table()
    UserCallData.create_table()
    Calls.create_table()
    Credits.create_table()
        
from app.routes import admin_routes, user_routes, credit_routes

app.register_blueprint(admin_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(credit_routes.bp)
