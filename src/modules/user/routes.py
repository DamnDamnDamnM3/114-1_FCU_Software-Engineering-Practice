from flask import request, jsonify, session
from . import user_bp
from services.user_service import UserService

user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
        
    mode = data.get('mode', 'NORMAL')
    budget = data.get('budget', 0)
    target_calories = data.get('targetCalories')
    target_protein = data.get('targetProtein')
    target_fat = data.get('targetFat')
    
    try:
        user_id = user_service.create_user(
            username=username, 
            password=password,
            mode=mode,
            budget=budget,
            target_calories=target_calories,
            target_protein=target_protein,
            target_fat=target_fat
        )
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    print("DEBUG: Login request received")
    try:
        data = request.get_json()
        print(f"DEBUG: Login data: {data}")
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
            
        user = user_service.verify_user(username, password)
        if user:
            print(f"DEBUG: Login successful for {username}")
            session['user_id'] = user['userID']
            session['username'] = user['username']
            return jsonify({'message': 'Login successful', 'user': user}), 200
        else:
            print(f"DEBUG: Login failed for {username}")
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"DEBUG: Login exception: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@user_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
        
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404
