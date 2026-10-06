from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import User, Student, Teacher, VerificationCode
from extensions import db, limiter
from sqlalchemy.exc import IntegrityError
import random
import string
import re


def _check_password_strength(password):
    """校验密码强度：长度不少于6位，且必须同时包含字母和数字"""
    if len(password) < 6:
        return False, '密码长度不能少于6位'
    if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return False, '密码必须包含字母和数字'
    return True, ''

register_bp = Blueprint('register', __name__)

ALLOWED_SCHOOLS = ['a校', 'b校', 'c校']


@register_bp.route('/api/check/username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({'code': 400, 'message': '用户名不能为空'}), 400

    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'code': 200, 'data': {'exists': exists}}), 200


@register_bp.route('/api/register/normal', methods=['POST'])
@limiter.limit("5 per minute")
def normal_register():
    data = request.get_json()

    required_fields = ['username', 'password', 'confirmPassword', 'name', 'role', 'school']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'code': 400, 'message': f'{field}不能为空'}), 400

    if data['role'] == 'student' and 'studentId' not in data:
        return jsonify({'code': 400, 'message': '学生注册必须填写学号'}), 400

    if data['role'] == 'teacher' and 'teacherId' not in data:
        return jsonify({'code': 400, 'message': '教师注册必须填写教工号'}), 400

    if data['role'] not in ('student', 'teacher'):
        return jsonify({'code': 400, 'message': 'role 只能是 student 或 teacher'}), 400

    if data['password'] != data['confirmPassword']:
        return jsonify({'code': 400, 'message': '两次输入的密码不一致'}), 400

    ok, msg = _check_password_strength(data['password'])
    if not ok:
        return jsonify({'code': 400, 'message': msg}), 400

    if data['school'] not in ALLOWED_SCHOOLS:
        return jsonify({'code': 400, 'message': '学校选项不正确'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400

    # 学号/工号查重，避免插入时唯一约束冲突导致 500
    if data['role'] == 'student' and Student.query.filter_by(student_no=data['studentId']).first():
        return jsonify({'code': 400, 'message': '该学号已被注册'}), 400
    if data['role'] == 'teacher' and Teacher.query.filter_by(teacher_no=data['teacherId']).first():
        return jsonify({'code': 400, 'message': '该工号已被注册'}), 400

    try:
        user = User(
            username=data['username'],
            name=data['name'],
            role=data['role']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()

        if data['role'] == 'student':
            student = Student(
                user_id=user.id,
                student_no=data['studentId'],
                department=data['school'],
                id_card=data.get('idCard', ''),
                phone=data.get('phone', '')
            )
            db.session.add(student)
        elif data['role'] == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_no=data['teacherId'],
                department=data['school'],
                title=data.get('title', ''),
                phone=data.get('phone', ''),
                role='faculty',
                status='pending'
            )
            db.session.add(teacher)

        db.session.commit()
        # 学生注册后直接激活（登录不做审核拦截），教师仍需管理员审核
        message = '注册成功，请登录' if data['role'] == 'student' else '注册成功，等待审核'
        return jsonify({'code': 200, 'message': message}), 200

    except IntegrityError as e:
        # 唯一约束兜底：用户名/学号/工号已被占用时不返回 500
        db.session.rollback()
        return jsonify({'code': 400, 'message': '用户名、学号或工号已被占用'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'注册失败: {str(e)}'}), 500


@register_bp.route('/api/register/phone', methods=['POST'])
@limiter.limit("5 per minute")
def phone_register():
    data = request.get_json()

    required_fields = ['name', 'role', 'school', 'phone', 'smsCode', 'password', 'confirmPassword']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'code': 400, 'message': f'{field}不能为空'}), 400

    if data['role'] == 'student' and 'studentId' not in data:
        return jsonify({'code': 400, 'message': '学生注册必须填写学号'}), 400

    if data['role'] == 'teacher' and 'teacherId' not in data:
        return jsonify({'code': 400, 'message': '教师注册必须填写教工号'}), 400

    if data['role'] not in ('student', 'teacher'):
        return jsonify({'code': 400, 'message': 'role 只能是 student 或 teacher'}), 400

    if data['password'] != data['confirmPassword']:
        return jsonify({'code': 400, 'message': '两次输入的密码不一致'}), 400

    ok, msg = _check_password_strength(data['password'])
    if not ok:
        return jsonify({'code': 400, 'message': msg}), 400

    if data['school'] not in ALLOWED_SCHOOLS:
        return jsonify({'code': 400, 'message': '学校选项不正确'}), 400

    code_record = VerificationCode.query.filter_by(
        phone=data['phone'],
        code=data['smsCode']
    ).order_by(VerificationCode.created_at.desc()).first()

    if not code_record:
        return jsonify({'code': 400, 'message': '验证码错误'}), 400

    if datetime.now() > code_record.expires_at:
        return jsonify({'code': 400, 'message': '验证码已过期'}), 400

    username = data['studentId'] if data['role'] == 'student' else data['teacherId']
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400

    # 学号/工号查重，避免插入时唯一约束冲突导致 500
    if data['role'] == 'student' and Student.query.filter_by(student_no=data['studentId']).first():
        return jsonify({'code': 400, 'message': '该学号已被注册'}), 400
    if data['role'] == 'teacher' and Teacher.query.filter_by(teacher_no=data['teacherId']).first():
        return jsonify({'code': 400, 'message': '该工号已被注册'}), 400

    try:
        user = User(
            username=username,
            name=data['name'],
            role=data['role']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()

        if data['role'] == 'student':
            student = Student(
                user_id=user.id,
                student_no=data['studentId'],
                department=data['school'],
                phone=data['phone'],
                id_card=data.get('idCard', '')
            )
            db.session.add(student)
        elif data['role'] == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                teacher_no=data['teacherId'],
                department=data['school'],
                phone=data['phone'],
                title=data.get('title', ''),
                role='faculty',
                status='pending'
            )
            db.session.add(teacher)

        db.session.commit()
        # 学生注册后直接激活（登录不做审核拦截），教师仍需管理员审核
        message = '注册成功，请登录' if data['role'] == 'student' else '注册成功，等待审核'
        return jsonify({'code': 200, 'message': message}), 200

    except IntegrityError as e:
        # 唯一约束兜底：用户名/学号/工号已被占用时不返回 500
        db.session.rollback()
        return jsonify({'code': 400, 'message': '用户名、学号或工号已被占用'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'注册失败: {str(e)}'}), 500


@register_bp.route('/api/sms/send', methods=['POST'])
def send_sms():
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({'code': 400, 'message': '手机号不能为空'}), 400

    if not phone.isdigit() or len(phone) != 11:
        return jsonify({'code': 400, 'message': '手机号格式不正确'}), 400

    try:
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = datetime.now() + timedelta(minutes=5)

        existing_code = VerificationCode.query.filter_by(phone=phone).first()
        if existing_code:
            db.session.delete(existing_code)

        verification_code = VerificationCode(
            phone=phone,
            code=code,
            expires_at=expires_at
        )
        db.session.add(verification_code)
        db.session.commit()

        return jsonify({'code': 200, 'message': '验证码已发送'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'发送失败: {str(e)}'}), 500