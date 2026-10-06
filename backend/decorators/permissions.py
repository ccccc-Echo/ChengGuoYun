from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return jsonify({'error': '请先登录'}), 401
            
            user = User.query.get(int(current_user_id))
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            if user.role == 'admin':
                return f(*args, **kwargs)
            
            if user.role == 'teacher':
                teacher = user.teacher
                if teacher and teacher.role in allowed_roles:
                    return f(*args, **kwargs)
            
            return jsonify({'error': '权限不足'}), 403
        return decorated_function
    return decorator


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if user.role != 'admin':
            return jsonify({'error': '仅管理员可访问'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if user.role == 'admin':
            return f(*args, **kwargs)
        
        if user.role != 'teacher':
            return jsonify({'error': '仅教师可访问'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def advisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if user.role == 'admin':
            return f(*args, **kwargs)
        
        if user.role == 'teacher':
            teacher = user.teacher
            if teacher and teacher.role == 'advisor':
                return f(*args, **kwargs)
        
        return jsonify({'error': '仅辅导员可访问'}), 403
    return decorated_function


def head_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'error': '请先登录'}), 401
        
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if user.role == 'admin':
            return f(*args, **kwargs)
        
        if user.role == 'teacher':
            teacher = user.teacher
            if teacher and teacher.role == 'head':
                return f(*args, **kwargs)
        
        return jsonify({'error': '仅院系负责人可访问'}), 403
    return decorated_function