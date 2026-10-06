from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Teacher, Role, TeamMember, Course
from extensions import db
from utils.logger import log_action

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teachers')


@teacher_bp.route('/', methods=['GET'])
@jwt_required()
def list_teachers():
    """获取教师列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权访问'}), 403
        else:
            return jsonify({'error': '无权访问'}), 403

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        status = request.args.get('status', 'all')
        name = request.args.get('name', '')
        teacher_no = request.args.get('teacher_no', '')
        department = request.args.get('department', '')
        role = request.args.get('role', '')

        query = Teacher.query

        if status != 'all':
            query = query.filter_by(status=status)
        if name:
            query = query.join(User).filter(User.name.like(f'%{name}%'))
        if teacher_no:
            query = query.filter(Teacher.teacher_no.like(f'%{teacher_no}%'))
        if department:
            query = query.filter(Teacher.department.like(f'%{department}%'))
        if role:
            query = query.filter_by(role=role)

        total = query.count()
        teachers = query.order_by(Teacher.id.desc()).paginate(page=page, per_page=page_size)

        return jsonify({
            'teachers': [{
                'id': t.id,
                'user_id': t.user_id,
                'name': t.user.name,
                'teacher_no': t.teacher_no,
                'department': t.department,
                'title': t.title,
                'role': t.role,
                'phone': t.phone,
                'status': t.status
            } for t in teachers.items],
            'total': total,
            'page': page,
            'page_size': page_size
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teachers/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取教师列表失败: {str(e)}'}), 500


@teacher_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_teacher_statistics():
    """获取教师统计数据：总数、待审核、已通过"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权访问'}), 403
        else:
            return jsonify({'error': '无权访问'}), 403

        total = Teacher.query.count()
        pending = Teacher.query.filter_by(status='pending').count()
        approved = Teacher.query.filter_by(status='approved').count()

        return jsonify({'total': total, 'pending': pending, 'approved': approved})
    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teachers/statistics 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取教师统计失败: {str(e)}'}), 500


@teacher_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_teacher(id):
    """获取教师详情"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权访问'}), 403
        else:
            return jsonify({'error': '无权访问'}), 403

        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'error': '教师不存在'}), 404

        # 该教师加入的团队（通过 team_members 关联表，含成员角色）
        joined_members = TeamMember.query.filter_by(teacher_id=teacher.id).all()
        teams = []
        for m in joined_members:
            t = m.team
            if not t:
                continue
            teams.append({
                'id': t.id,
                'name': t.name,
                'type': t.type,
                'creator_name': t.creator.user.name if t.creator and t.creator.user else None,
                'member_role': m.role,
                'joined_at': m.joined_at.strftime('%Y-%m-%d %H:%M:%S') if m.joined_at else None,
                'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None
            })

        # 该教师创建的课程
        courses = [c.to_dict() for c in teacher.courses]

        return jsonify({
            'teacher': {
                'id': teacher.id,
                'name': teacher.user.name,
                'teacher_no': teacher.teacher_no,
                'department': teacher.department,
                'title': teacher.title,
                'role': teacher.role,
                'role_name': teacher.role_info.name if teacher.role_info else None,
                'phone': teacher.phone,
                'email': teacher.user.email,
                'status': teacher.status,
                'created_at': teacher.user.created_at.strftime('%Y-%m-%d %H:%M:%S') if teacher.user.created_at else None
            },
            'teams': teams,
            'courses': courses
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teachers/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取教师详情失败: {str(e)}'}), 500


@teacher_bp.route('/', methods=['POST'])
@jwt_required()
def create_teacher():
    """添加教师账号"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权添加教师'}), 403
        else:
            return jsonify({'error': '无权添加教师'}), 403

        data = request.get_json()
        required_fields = ['teacher_no', 'name', 'password']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        if User.query.filter_by(username=data['teacher_no']).first():
            return jsonify({'error': '工号已存在'}), 400

        user = User(
            username=data['teacher_no'],
            role='teacher',
            name=data['name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.flush()

        role_name = data.get('role', '教师')
        role = Role.query.filter_by(name=role_name).first()

        teacher = Teacher(
            user_id=user.id,
            teacher_no=data['teacher_no'],
            department=data.get('department'),
            title=data.get('title'),
            phone=data.get('phone'),
            role=role_name,
            role_id=role.id if role else None,
            department_id=data.get('department_id', 0)
        )
        db.session.add(teacher)
        db.session.commit()

        return jsonify({
            'message': '教师添加成功',
            'teacher': {
                'id': teacher.id,
                'name': teacher.user.name,
                'teacher_no': teacher.teacher_no,
                'department': teacher.department,
                'title': teacher.title,
                'role': teacher.role
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/teachers/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加教师失败: {str(e)}'}), 500


@teacher_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_teacher(id):
    """修改教师信息"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            current_teacher = current_user.teacher
            if not current_teacher or current_teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权修改教师信息'}), 403
        else:
            return jsonify({'error': '无权修改教师信息'}), 403

        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'error': '教师不存在'}), 404

        data = request.get_json()

        if 'name' in data:
            teacher.user.name = data['name']
        if 'department' in data:
            teacher.department = data['department']
        if 'title' in data:
            teacher.title = data['title']
        if 'phone' in data:
            teacher.phone = data['phone']
        if 'role' in data:
            role_name = data['role']
            teacher.role = role_name
            role = Role.query.filter_by(name=role_name).first()
            teacher.role_id = role.id if role else None
        if 'department_id' in data:
            teacher.department_id = data['department_id']

        db.session.commit()

        # 站内信：教师权限/角色变更
        try:
            from models import send_notification
            if 'role' in data and teacher.user_id:
                send_notification(
                    teacher.user_id,
                    '您的权限已更新，请重新登录查看',
                    content=f'您的角色已更新为“{teacher.role}”，请重新登录以应用最新权限。',
                    type='permission_changed'
                )
        except Exception:
            db.session.rollback()
            # 通知失败不影响主流程

        return jsonify({
            'message': '教师信息更新成功',
            'teacher': {
                'id': teacher.id,
                'name': teacher.user.name,
                'teacher_no': teacher.teacher_no,
                'department': teacher.department,
                'title': teacher.title,
                'role': teacher.role
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/teachers/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'修改教师信息失败: {str(e)}'}), 500


@teacher_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_teacher(id):
    """删除教师账号"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'error': '无权删除教师'}), 403
        else:
            return jsonify({'error': '无权删除教师'}), 403

        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'error': '教师不存在'}), 404

        user = teacher.user
        db.session.delete(teacher)
        db.session.delete(user)
        db.session.commit()

        log_action('delete_teacher', f'删除教师账号“{teacher.teacher_no or teacher.id}”', user=current_user)

        return jsonify({'message': '教师删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/teachers/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除教师失败: {str(e)}'}), 500


@teacher_bp.route('/<int:id>/unlock', methods=['PUT'])
@jwt_required()
def unlock_teacher(id):
    """管理员手动解锁教师账号（清除登录失败锁定）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'admin':
            return jsonify({'error': '无权操作'}), 403

        teacher = Teacher.query.get(id)
        if not teacher or not teacher.user:
            return jsonify({'error': '教师不存在'}), 404

        user = teacher.user
        was_locked = bool(user.locked_until and user.locked_until > datetime.now())
        user.login_fail_count = 0
        user.locked_until = None
        db.session.commit()

        log_action('unlock_teacher', f'解锁账号“{user.username}”（登录失败锁定）', user=current_user)
        return jsonify({'message': '账号已解锁', 'was_locked': was_locked}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'解锁失败: {str(e)}'}), 500


@teacher_bp.route('/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_teacher(id):
    """审核教师账号"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ('head', 'teaching_admin', '院系负责人', '教务管理员'):
                return jsonify({'code': 403, 'message': '无权审核教师'}), 403
        else:
            return jsonify({'code': 403, 'message': '无权审核教师'}), 403

        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({'code': 404, 'message': '教师不存在'}), 404

        teacher.status = 'approved'
        db.session.commit()

        # 站内信：通知教师注册审核通过
        try:
            from models import send_notification
            if teacher.user_id:
                send_notification(
                    teacher.user_id,
                    '您的注册申请已通过，可登录系统',
                    content=f'教师账号（工号：{teacher.teacher_no or teacher.id}）已审核通过，请登录系统。',
                    type='teacher_approved'
                )
        except Exception:
            db.session.rollback()
            # 通知失败不影响审核主流程

        return jsonify({'code': 200, 'message': '审核通过'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/teachers/{id}/approve 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'code': 500, 'message': f'审核失败: {str(e)}'}), 500