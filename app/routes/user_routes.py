from app.models import Users, UserCallData, Calls
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, make_response
from functools import wraps


bp = Blueprint('user_routes', __name__)


def no_cache(view):
    @wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache_impl


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user_routes.user_login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/api/userLogin', methods=['POST', 'OPTIONS'])
@no_cache
def user_login():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify(message='Username and password are required'), 400
    
    user = Users.get_by_username(username)
    
    if not user or not check_password_hash(user['user_password'], password):
        return jsonify(message='Invalid credentials'), 401
    
    session['user_id'] = user['id']
    return jsonify(message='Login successful', user_id=user['id']), 200


@bp.route('/api/userLogout', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def user_logout():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    session.pop('user_id', None)
    return jsonify(message='Logout successful'), 200


@bp.route('/api/user/viewInfo', methods=['GET', 'OPTIONS'])
@user_required
@no_cache
def view_info():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    # user_id = request.args.get('user_id')
    # data = request.get_json()
    # user_id = data.get('user_id')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(message='User ID is required'), 400
    user = Users.get_by_id(user_id)
    if not user:
        return jsonify(message='User not found'), 404
    return jsonify(user=user), 200


@bp.route('/api/user/updateGreetingMessage', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def update_greeting_message():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    # user_id = data.get('user_id')
    user_id = session.get('user_id')
    greeting_message = data.get('greeting_message')
    
    if not user_id or not greeting_message:
        return jsonify(message='User ID and greeting message are required'), 400
    
    UserCallData.update_greeting_message(user_id, greeting_message)
    return jsonify(message='Greeting message updated successfully'), 200

@bp.route('/api/user/updateDataset', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def update_dataset():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    data = request.get_json()
    # user_id = data.get('user_id')
    user_id = session.get('user_id')
    dataset = data.get('dataset')
    
    if not user_id or not dataset:
        return jsonify(message='User ID and dataset are required'), 400
    
    UserCallData.update_dataset(user_id, dataset)
    return jsonify(message='Dataset updated successfully'), 200

@bp.route('/api/user/viewCallHistory', methods=['GET', 'OPTIONS'])
@user_required
@no_cache
def view_call_history():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    # user_id = request.args.get('user_id')
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    calls = Calls.get_by_user_id(user_id,"all")
    if not calls:
        return jsonify(message='No call history found for this user'), 404
    
    return jsonify(calls=[call.to_dict() for call in calls]), 200

@bp.route('/api/user/getCallsByFilter', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def get_calls_by_filter():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    # user_id = request.args.get('user_id')
    user_id = session.get('user_id')
    data = request.get_json()
    filter_type = data.get('filter_type')
    # filter_type = request.args.get('filter_type')
    if not user_id or not filter_type:
        return jsonify(message='User ID and filter type are required'), 400
    calls = Calls.filter_calls(user_id, filter_type)
    if not calls:
        return jsonify(message='No calls found for this user with the specified filter'), 404
    return jsonify(calls=[call.to_dict() for call in calls]), 200


@bp.route('/api/user/uploadClientData', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def upload_client_data():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200

    data = request.get_json()
    # user_id = data.get('user_id')
    user_id = session.get('user_id')
    client_data = data.get('client_data')
    call_type = data.get('call_type', '1way')  # Default to '1way' if not provided
    ai_transmission_message = data.get('ai_transmission_message', '')
    
    
    if not user_id or not client_data:
        return jsonify(message='User ID and client data are required'), 400

    if not isinstance(client_data, list):
        return jsonify(message='Client data must be a list of dictionaries'), 400

    bulk_calls = []
    for client in client_data:
        if not isinstance(client, dict) or 'name' not in client or 'phone' not in client:
            return jsonify(message='Each client must be a dictionary with name and phone'), 400

        # Prepare data for each client for insertion
        call_tuple = (
            user_id,                   # user_id
            client['name'],          # receiver_name
            client['phone'],           # receiver_phone
            '1way',                # call_type (default value or change as needed)
            '',                        # conversation_history (empty initially)
            ai_transmission_message,   # ai_transmission_message (empty initially)
            'no',                 # callback_status (default)
            0                          # call_done (0 = not done)
        )
        bulk_calls.append(call_tuple)

    try:
        Calls.add_bulk_calls(bulk_calls)
        return jsonify(message='Client data uploaded successfully'), 200
    except Exception as e:
        return jsonify(message='Failed to upload client data', error=str(e)), 500
    
    
@bp.route('/api/user/viewRealtimeSnapshot', methods=['POST', 'OPTIONS'])
@user_required
@no_cache
def view_realtime_snapshot():
    if request.method == 'OPTIONS':
        return jsonify(message='CORS preflight response'), 200
    
    # user_id = request.args.get('user_id')
    user_id = session.get('user_id')
    data = request.get_json()
    filter_type = data.get('filter_type') 
    # filter_type = request.args.get('filter_type', 'all')
    if not user_id:
        return jsonify(message='User ID is required'), 400
    
    snapshot = Calls.filter_calls(user_id)
    if not snapshot:
        return jsonify(message='No realtime snapshot found for this user'), 404
    
    return jsonify(snapshot=snapshot), 200
