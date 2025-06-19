from app.models import Users, UserCallData, Calls, Credits
from flask import Blueprint, request, jsonify, session, make_response
from functools import wraps
from app.routes.user_routes import user_required
from app.routes.admin_routes import admin_required, no_cache
bp = Blueprint('credit_routes', __name__)




@bp.route('/api/admin/addCredits', methods=['POST', 'OPTIONS'])
@admin_required
@no_cache
def add_credits():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    user_id = data.get('user_id')
    credits = data.get('credits')
    
    if not user_id or not credits:
        return jsonify(message='User ID and credits are required'), 400
    
    try:
        Credits.add_credits(user_id, credits)
        return jsonify(message='Credits added successfully'), 200
    except Exception as e:
        return jsonify(message=str(e)), 500
    
@bp.route('/api/user/getCredits', methods=['POST', 'OPTIONS'])
def get_credits():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    # user_id = request.args.get('user_id')
    user_id = session.get('user_id') or request.get_json().get('user_id')
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    try:
        credits = Credits.get_credits(user_id)
        return jsonify(credits=credits), 200
    except Exception as e:
        return jsonify(message=str(e)), 500
    
@bp.route('/api/user/deductCredits', methods=['POST', 'OPTIONS'])
def deduct_credits():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    user_id = data.get('user_id')
    credits = data.get('credits')
    
    if not user_id or not credits:
        return jsonify(message='User ID and credits are required'), 400
    
    try:
        Credits.deduct_credits(user_id, credits)
        return jsonify(message='Credits deducted successfully'), 200
    except ValueError as e:
        return jsonify(message=str(e)), 400
    except Exception as e:
        return jsonify(message=str(e)), 500
    
@bp.route('/api/user/resetCredits', methods=['POST', 'OPTIONS'])
@admin_required
@no_cache
def reset_credits():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    try:
        Credits.reset_credits(user_id)
        return jsonify(message='Credits reset successfully'), 200
    except Exception as e:
        return jsonify(message=str(e)), 500


@bp.route('/api/user/ViewInfo', methods=['POST', 'OPTIONS'])
@admin_required
@no_cache
def view_user_credit_info():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify(message='Email is required'), 400 
    
    user_data = .get_user_data_by_email(email)
    if not user_data:
        return jsonify(message='User data not found for given email'), 404
    return jsonify(user_data=user_data), 200
