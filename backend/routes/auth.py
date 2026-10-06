from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, decode_token
from models import User, Student, Teacher, Role
from extensions import db, limiter
from utils.logger import log_action
import re
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        required_fields = ['username', 'password', 'role', 'name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '缺少必填字段'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': '用户名已存在'}), 400

        if len(data['password']) < 6:
            return jsonify({'error': '密码长度不少于6位'}), 400

        if data['role'] not in ['student', 'teacher']:
            return jsonify({'error': '无效的角色类型'}), 400

        user = User(
            username=data['username'],
            role=data['role'],
            name=data['name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.flush()

        if data['role'] == 'student':
            student = Student(
                user_id=user.id,
                student_no=data.get('student_no', data['username']),
                school=data.get('school', ''),
                id_card=data.get('id_card', ''),
                phone=data.get('phone', '')
            )
            db.session.add(student)
        elif data['role'] == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_no=data.get('teacher_no', data['username']),
                department=data.get('school', ''),
                title=data.get('title', ''),
                phone=data.get('phone', ''),
                role='faculty'
            )
            db.session.add(teacher)

        db.session.commit()

        access_token = create_access_token(identity=str(user.id))

        user_data = user.to_dict()
        
        if user.role == 'student':
            if user.student:
                user_data.update({
                    'student_id': user.student.id,
                    'student_no': user.student.student_no,
                    'class_id': user.student.class_id,
                    'class_name': user.student.class_name(),
                    'major': user.student.major,
                    'phone': user.student.phone,
                    'avatar': user.student.avatar
                })
            else:
                user_data.update({
                    'student_id': None,
                    'student_no': '',
                    'class_id': '',
                    'class_name': '',
                    'major': '',
                    'phone': '',
                    'avatar': ''
                })
        elif user.role == 'teacher':
            if user.teacher:
                user_data.update({
                    'teacher_id': user.teacher.id,
                    'teacher_no': user.teacher.teacher_no,
                    'department': user.teacher.department,
                    'title': user.teacher.title,
                    'phone': user.teacher.phone,
                    'teacher_role': user.teacher.role
                })
            else:
                user_data.update({
                    'teacher_id': None,
                    'teacher_no': '',
                    'department': '',
                    'title': '',
                    'phone': '',
                    'teacher_role': ''
                })

        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': user_data
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== 注册错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取当前用户个人信息"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        user_data = user.to_dict()
        
        if user.role == 'student':
            if user.student:
                user_data.update({
                    'student_id': user.student.id,
                    'student_no': user.student.student_no,
                    'class_id': user.student.class_id,
                    'class_name': user.student.class_name(),
                    'major': user.student.major,
                    'phone': user.student.phone,
                    'avatar': user.student.avatar
                })
            else:
                user_data.update({
                    'student_id': None,
                    'student_no': '',
                    'class_id': '',
                    'class_name': '',
                    'major': '',
                    'phone': '',
                    'avatar': ''
                })
        elif user.role == 'teacher':
            if user.teacher:
                user_data.update({
                    'teacher_id': user.teacher.id,
                    'teacher_no': user.teacher.teacher_no,
                    'department': user.teacher.department,
                    'title': user.teacher.title,
                    'phone': user.teacher.phone,
                    'teacher_role': user.teacher.role
                })
            else:
                user_data.update({
                    'teacher_id': None,
                    'teacher_no': '',
                    'department': '',
                    'title': '',
                    'phone': '',
                    'teacher_role': ''
                })

        return jsonify({
            'user': user_data
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== 获取个人信息错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取个人信息失败: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新当前用户个人信息"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        if user.role == 'student':
            student = user.student
            if not student:
                student = Student(user_id=user.id)
                db.session.add(student)
            
            if 'student_no' in data:
                if data['student_no'] and Student.query.filter(
                    Student.student_no == data['student_no'],
                    Student.id != student.id
                ).first():
                    db.session.rollback()
                    return jsonify({'error': '学号已存在'}), 400
                student.student_no = data['student_no']
            
            if 'major' in data:
                student.major = data['major']
            
            if 'phone' in data:
                student.phone = data['phone']

        elif user.role == 'teacher':
            teacher = user.teacher
            if not teacher:
                teacher = Teacher(user_id=user.id)
                db.session.add(teacher)
            
            if 'teacher_no' in data:
                if data['teacher_no'] and Teacher.query.filter(
                    Teacher.teacher_no == data['teacher_no'],
                    Teacher.id != teacher.id
                ).first():
                    db.session.rollback()
                    return jsonify({'error': '工号已存在'}), 400
                teacher.teacher_no = data['teacher_no']
            
            if 'department' in data:
                teacher.department = data['department']
            
            if 'title' in data:
                teacher.title = data['title']
            
            if 'phone' in data:
                teacher.phone = data['phone']

        else:
            return jsonify({'error': '管理员无需修改个人资料'}), 403

        db.session.commit()

        user_data = user.to_dict()
        
        if user.role == 'student' and user.student:
            user_data.update({
                'student_id': user.student.id,
                'student_no': user.student.student_no,
                'class_id': user.student.class_id,
                'class_name': user.student.class_name(),
                'major': user.student.major,
                'phone': user.student.phone,
                'avatar': user.student.avatar
            })
        elif user.role == 'teacher' and user.teacher:
            user_data.update({
                'teacher_id': user.teacher.id,
                'teacher_no': user.teacher.teacher_no,
                'department': user.teacher.department,
                'title': user.teacher.title,
                'phone': user.teacher.phone,
                'teacher_role': user.teacher.role
            })

        return jsonify({
            'message': '更新成功',
            'user': user_data
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== 更新个人信息错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新个人信息失败: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """用户登录"""
    try:
        print("\n=== 登录请求开始 ===")
        
        data = request.get_json()
        print(f"请求数据: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            print("错误: 用户名和密码不能为空")
            return jsonify({'error': '用户名和密码不能为空'}), 400

        username = data['username']
        password = data['password']
        print(f"用户名: {username}")
        print(f"密码长度: {len(password)}")

        user = User.query.filter_by(username=username).first()
        print(f"查询到的用户: {user.to_dict() if user else None}")

        if not user:
            print("错误: 用户不存在")
            return jsonify({'code': 404, 'message': '用户名不存在'}), 404

        # 检查账号是否处于锁定期
        if user.locked_until and user.locked_until > datetime.now():
            remain = int((user.locked_until - datetime.now()).total_seconds() // 60) + 1
            print(f"错误: 账号已锁定，剩余{remain}分钟")
            return jsonify({'code': 403, 'message': f'账号已锁定，请{remain}分钟后重试'}), 403

        password_check = user.check_password(password)
        print(f"密码验证结果: {password_check}")

        if not password_check:
            print("错误: 密码不正确")
            user.login_fail_count = (user.login_fail_count or 0) + 1
            if user.login_fail_count >= 5:
                user.locked_until = datetime.now() + timedelta(minutes=10)
                user.login_fail_count = 0
                db.session.commit()
                return jsonify({'code': 403, 'message': '密码错误次数过多，账号已锁定10分钟'}), 403
            db.session.commit()
            return jsonify({'code': 401, 'message': f'密码错误，还可尝试{5 - user.login_fail_count}次'}), 401

        # 登录成功，重置失败计数和锁定状态
        if user.login_fail_count or user.locked_until:
            user.login_fail_count = 0
            user.locked_until = None
            db.session.commit()

        if user.role == 'teacher' and user.teacher and user.teacher.status != 'approved':
            print("错误: 教师账号待审核")
            return jsonify({'error': '账号待审核，请联系管理员'}), 401

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=2))
        refresh_token = create_refresh_token(identity=str(user.id), expires_delta=timedelta(days=7))
        print(f"生成的 access_token: {access_token[:50]}...")

        user_data = user.to_dict()
        
        if user.role == 'student':
            if user.student:
                print(f"学生信息: {user.student.to_dict()}")
                user_data.update({
                    'student_id': user.student.id,
                    'student_no': user.student.student_no,
                    'class_id': user.student.class_id,
                    'major': user.student.major
                })
            else:
                print("警告: 学生用户没有对应的学生记录")
                user_data['student_id'] = None
        elif user.role == 'teacher':
            if user.teacher:
                print(f"教师信息: {user.teacher.to_dict()}")
                user_data.update({
                    'teacher_id': user.teacher.id,
                    'teacher_no': user.teacher.teacher_no,
                    'department': user.teacher.department,
                    'title': user.teacher.title,
                    'teacher_role': user.teacher.role,
                    'role_id': user.teacher.role_id
                })
                
                if user.teacher.role_info and user.teacher.role_info.permissions:
                    import json
                    permissions = json.loads(user.teacher.role_info.permissions)
                    user_data['permissions'] = permissions
                elif user.teacher.role_id:
                    role = Role.query.get(user.teacher.role_id)
                    if role and role.permissions:
                        import json
                        permissions = json.loads(role.permissions)
                        user_data['permissions'] = permissions
                    else:
                        user_data['permissions'] = []
                else:
                    user_data['permissions'] = []
            else:
                print("警告: 教师用户没有对应的教师记录")
                user_data['teacher_id'] = None
                user_data['permissions'] = []

        if user.role == 'admin':
            user_data['teacher_role'] = 'admin'
            user_data['permissions'] = []

        print("登录成功")
        log_action('login', f'用户登录成功（{user.role}）', user=user)
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_expires': 2 * 3600,
            'refresh_expires': 7 * 24 * 3600,
            'user': user_data
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== 登录错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'登录失败: {str(e)}', 'detail': traceback.format_exc()}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """使用 refresh_token 换取新的 access_token"""
    data = request.get_json() or {}
    rt = (data.get('refresh_token') or '').strip()
    if not rt:
        return jsonify({'error': '缺少 refresh_token'}), 400

    try:
        decoded = decode_token(rt)
    except Exception:
        return jsonify({'error': 'refresh_token 无效或已过期'}), 401

    if decoded.get('type') != 'refresh':
        return jsonify({'error': '无效的 token 类型'}), 401

    try:
        user_id = int(decoded['sub'])
    except (KeyError, ValueError):
        return jsonify({'error': 'refresh_token 无效'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    new_access = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=2))
    return jsonify({
        'access_token': new_access,
        'access_expires': 2 * 3600
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        if 'old_password' not in data or 'new_password' not in data:
            return jsonify({'error': '缺少旧密码或新密码'}), 400

        if not user.check_password(data['old_password']):
            return jsonify({'error': '旧密码不正确'}), 401

        if len(data['new_password']) < 6:
            return jsonify({'error': '新密码长度不少于6位'}), 400

        if not re.search(r'[A-Za-z]', data['new_password']) or not re.search(r'\d', data['new_password']):
            return jsonify({'error': '密码必须包含字母和数字'}), 400

        user.set_password(data['new_password'])
        db.session.commit()

        return jsonify({'message': '密码修改成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== 修改密码错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'修改密码失败: {str(e)}'}), 500


@auth_bp.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers_list():
    """获取教师列表（仅管理员），支持按权限过滤"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.role != 'admin':
            return jsonify({'error': '无权限访问'}), 403

        permission_filter = request.args.get('permission')

        teachers = Teacher.query.join(User, User.id == Teacher.user_id).filter(
            User.role == 'teacher',
            Teacher.status == 'approved'
        ).all()

        result = []
        for teacher in teachers:
            has_permission = True
            
            if permission_filter:
                has_permission = False
                
                if teacher.role_info and teacher.role_info.permissions:
                    import json
                    permissions = json.loads(teacher.role_info.permissions)
                    if permission_filter in permissions:
                        has_permission = True
            
            if has_permission:
                result.append({
                    'id': teacher.id,
                    'name': teacher.user.name,
                    'teacher_no': teacher.teacher_no,
                    'department': teacher.department,
                    'title': teacher.title
                })

        return jsonify({'teachers': result}), 200

    except Exception as e:
        import traceback
        print(f"\n=== 获取教师列表错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取教师列表失败: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': '用户不存在'}), 404

        user_data = user.to_dict()
        
        if user.role == 'student':
            if user.student:
                user_data.update({
                    'student_id': user.student.id,
                    'student_no': user.student.student_no,
                    'class_id': user.student.class_id,
                    'class_name': user.student.class_name(),
                    'major': user.student.major,
                    'phone': user.student.phone,
                    'avatar': user.student.avatar
                })
            else:
                user_data.update({
                    'student_id': None,
                    'student_no': '',
                    'class_id': '',
                    'class_name': '',
                    'major': '',
                    'phone': '',
                    'avatar': ''
                })
        elif user.role == 'teacher':
            if user.teacher:
                user_data.update({
                    'teacher_id': user.teacher.id,
                    'teacher_no': user.teacher.teacher_no,
                    'department': user.teacher.department,
                    'title': user.teacher.title,
                    'phone': user.teacher.phone,
                    'teacher_role': user.teacher.role
                })
                if user.teacher.role_info and user.teacher.role_info.permissions:
                    import json
                    permissions = json.loads(user.teacher.role_info.permissions)
                    user_data['permissions'] = permissions
                elif user.teacher.role_id:
                    role = Role.query.get(user.teacher.role_id)
                    if role and role.permissions:
                        import json
                        permissions = json.loads(role.permissions)
                        user_data['permissions'] = permissions
                    else:
                        user_data['permissions'] = []
                else:
                    user_data['permissions'] = []
            else:
                user_data.update({
                    'teacher_id': None,
                    'teacher_no': '',
                    'department': '',
                    'title': '',
                    'phone': '',
                    'teacher_role': '',
                    'permissions': []
                })
        elif user.role == 'admin':
            user_data.update({
                'teacher_role': 'admin',
                'permissions': []
            })

        return jsonify({
            'user': user_data
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500