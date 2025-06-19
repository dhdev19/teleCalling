from app.models import Admin, Users, UserCallData, Calls
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, make_response
from functools import wraps

bp = Blueprint('admin_routes', __name__)


def no_cache(view):
    @wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache_impl


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)
        if 'admin_id' not in session:
            return redirect(url_for('admin_routes.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/api/adminLogin', methods=['POST', 'OPTIONS'])
@no_cache
def admin_login():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify(message='Username and password are required'), 400
    
    admin = Admin.get_by_username(username)
    
    if not admin or not check_password_hash(admin['admin_password'], password):
        return jsonify(message='Invalid credentials'), 401
    
    
    session['admin_id'] = admin['id']
    
    return jsonify(message='Login successful', admin_id=admin['id']), 200


@bp.route('/api/adminLogout', methods=['POST', 'OPTIONS'])
@admin_required
@no_cache
def admin_logout():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    session.pop('admin_id', None)
    
    return jsonify(message='Logout successful'), 200


@bp.route('/api/admin/addAdmin', methods=['POST', 'OPTIONS'])
@admin_required
def add_admin():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    admin_name = data.get('admin_name')
    admin_email = data.get('admin_email')
    admin_password = data.get('admin_password')
    admin_whatsapp_number = data.get('admin_whatsapp_number', None)
    
    
    if not admin_name or not admin_email or not admin_password:
        return jsonify(message='All fields are required'), 400
    
    hashed_password = generate_password_hash(admin_password)
    
    
    Admin.add_admin(admin_name=admin_name,admin_email=admin_email,admin_password=hashed_password,whatsapp_number=admin_whatsapp_number)
    
    return jsonify(message='Admin added successfully'), 201

@bp.route('/api/admin/getAdmins', methods=['GET', 'OPTIONS'])
@admin_required
def get_admins():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    admins = Admin.get_admins()
    
    return jsonify(admins=admins), 200

@bp.route('/api/admin/deleteAdmin', methods=['POST', 'OPTIONS'])
@admin_required
def delete_admin():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    admin_id = data.get('admin_id')
    
    
    if not admin_id:
        return jsonify(message='Admin ID is required'), 400
    
    admin = Admin.get_by_id(admin_id)
    
    if not admin:
        return jsonify(message='Admin not found'), 404
    
    Admin.delete_admin(admin_id)
    
    return jsonify(message='Admin deleted successfully'), 200

@bp.route('/api/admin/addUser', methods=['POST', 'OPTIONS'])
@admin_required
def add_user():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')
    company_name = data.get('company_name', None)
    whatsapp_number = data.get('whatsapp_number', None)
    twilio_phone_number = data.get('twilio_phone_number', None)
    
    if not user_name or not email or not password:
        return jsonify(message='All fields are required'), 400
    
    hashed_password = generate_password_hash(password)
    
    Users.add_user(
        user_name=user_name,
        email=email,
        password=hashed_password,
        company_name=company_name,
        whatsapp_number=whatsapp_number
    )
    
    # new_user.add_user()
    
    new_user = Users.get_user_by_email(email)
    if not new_user:
        return jsonify(message='User creation failed'), 500
    try:
        UserCallData.add_user_call_data(
        user_id=new_user['id'],
        twilio_phone_number=twilio_phone_number,
        dataset='',
        greeting_message='Hello! This is an AI Assistant. How may I help you?'
        )
        return jsonify(message='User added successfully'), 201
    # user_call_data.add_user_call_data()
    # if not user_call_data:
    except:
        return jsonify(message='User call data creation failed'), 500    

@bp.route('/api/admin/getUsers', methods=['GET', 'OPTIONS'])
@admin_required
def get_users():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    users = Users.get_users()
    
    return jsonify(users=users), 200

@bp.route('/api/admin/deleteUser', methods=['POST', 'OPTIONS'])
@admin_required
def delete_user():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    user_id = data.get('user_id')
    
    
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    user = Users.get_by_id(user_id)
    
    if not user:
        return jsonify(message='User not found'), 404
    
    Users.delete_user(user_id=user_id)
    
    return jsonify(message='User deleted successfully'), 200

# @bp.route('/api/admin/updateUserInfo', methods=['POST', 'OPTIONS'])
# def update_user_info():
#     if request.method == 'OPTIONS':
#         return jsonify(message='CORS preflight response'), 200
#     data = request.get_json()
#     user_id = data.get('user_id')
#     user_name = data.get('user_name')
#     email = data.get('email')
#     company_name = data.get('company_name', None)
#     whatsapp_number = data.get('whatsapp_number', None)
    
    
#     if not user_id or not user_name or not email:
#         return jsonify(message='All fields are required'), 400
    
#     user = Users.get_by_id(user_id)
    
#     if not user:
#         return jsonify(message='User not found'), 404
    
#     user.user_name = user_name
#     user.email = email
#     user.company_name = company_name
#     user.whatsapp_number = whatsapp_number
#     user.update_user()
    
#     return jsonify(message='User info updated successfully'), 200

@bp.route('/api/admin/getUserCallDataByuserID', methods=['POST', 'OPTIONS'])
@admin_required
def get_user_call_data_by_user_id():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    user_id = data.get('user_id')
    
    
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    user_call_data = UserCallData.get_user_call_data(user_id)
    
    if not user_call_data:
        return jsonify(message='No call data found for this user'), 404
    
    return jsonify(user_call_data=user_call_data), 200

@bp.route('/api/admin/getUserInfo', methods=['POST', 'OPTIONS'])
@admin_required
def get_user_info():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    user_id = data.get('user_id')
    
    
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    user = Users.get_by_id(user_id)
    
    if not user:
        return jsonify(message='User not found'), 404
    
    return jsonify(user=user), 200

