from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Role
from extensions import db
import json
from utils.logger import log_action

permission_bp = Blueprint('permission', __name__, url_prefix='/api/roles')

ALL_PERMISSIONS = [
    {
        'group': '学生管理',
        'permissions': [
            {'code': 'student:add', 'name': '添加学生'},
            {'code': 'student:delete', 'name': '删除学生'},
            {'code': 'student:reset_pwd', 'name': '重置学生密码'}
        ]
    },
    {
        'group': '成果管理',
        'permissions': [
            {'code': 'achievement:view', 'name': '查看所授课程成果'},
            {'code': 'achievement:audit', 'name': '审核成果'}
        ]
    },
    {
        'group': '课程管理',
        'permissions': [
            {'code': 'course:create', 'name': '创建课程'},
            {'code': 'course:edit', 'name': '修改课程信息'},
            {'code': 'course:delete', 'name': '删除课程'},
            {'code': 'course:lock', 'name': '锁定/解锁课程'}
        ]
    },
    {
        'group': '教师管理',
        'permissions': [
            {'code': 'teacher:add', 'name': '添加教师'},
            {'code': 'teacher:edit', 'name': '修改教师信息'},
            {'code': 'teacher:delete', 'name': '删除教师'},
            {'code': 'teacher:audit', 'name': '审核教师'}
        ]
    },
    {
        'group': '团队管理',
        'permissions': [
            {'code': 'team:create', 'name': '创建团队'},
            {'code': 'team:delete', 'name': '删除团队'},
            {'code': 'team:remove_member', 'name': '移除团队成员'}
        ]
    },
    {
        'group': '知识库',
        'permissions': [
            {'code': 'knowledge:view', 'name': '查看知识库'},
            {'code': 'knowledge:export', 'name': '导出知识库PDF'}
        ]
    }
]

DEFAULT_ROLES = [
    {
        'name': '院系负责人',
        'permissions': [
            'student:add', 'student:delete', 'student:reset_pwd',
            'achievement:view', 'achievement:audit',
            'course:create', 'course:edit', 'course:delete', 'course:lock',
            'teacher:add', 'teacher:edit', 'teacher:delete', 'teacher:audit',
            'team:create', 'team:delete', 'team:remove_member'
        ]
    },
    {
        'name': '辅导员',
        'permissions': [
            'student:add', 'student:delete', 'student:reset_pwd',
            'achievement:view', 'achievement:audit',
            'team:create', 'team:delete', 'team:remove_member'
        ]
    },
    {
        'name': '教师',
        'permissions': [
            'student:add', 'student:delete', 'student:reset_pwd',
            'achievement:view', 'achievement:audit',
            'course:create', 'course:edit', 'course:delete', 'course:lock',
            'team:create', 'team:delete', 'team:remove_member'
        ]
    },
    {
        'name': '教务管理员',
        'permissions': [
            'student:add', 'student:delete', 'student:reset_pwd',
            'achievement:view', 'achievement:audit',
            'course:create', 'course:edit', 'course:delete', 'course:lock',
            'teacher:add', 'teacher:edit', 'teacher:delete', 'teacher:audit',
            'team:create', 'team:delete', 'team:remove_member'
        ]
    }
]


def init_default_roles():
    """初始化默认角色"""
    try:
        for role_data in DEFAULT_ROLES:
            existing = Role.query.filter_by(name=role_data['name']).first()
            if existing:
                existing.permissions = json.dumps(role_data['permissions'])
            else:
                role = Role(
                    name=role_data['name'],
                    permissions=json.dumps(role_data['permissions'])
                )
                db.session.add(role)
        db.session.commit()
        print("默认角色初始化完成")
    except Exception as e:
        db.session.rollback()
        print(f"初始化默认角色失败: {str(e)}")


@permission_bp.route('/', methods=['GET'])
@jwt_required()
def get_roles():
    """获取所有角色列表（管理员/教师可访问）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role not in ['admin', 'teacher']:
            return jsonify({'error': '无权访问'}), 403

        roles = Role.query.order_by(Role.id).all()

        return jsonify({
            'roles': [role.to_dict() for role in roles],
            'permission_groups': ALL_PERMISSIONS
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/roles/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取角色列表失败: {str(e)}'}), 500


@permission_bp.route('/', methods=['POST'])
@jwt_required()
def create_role():
    """添加角色"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': '请输入角色名称'}), 400

        name = data['name'].strip()

        existing = Role.query.filter_by(name=name).first()
        if existing:
            return jsonify({'error': '角色名称已存在'}), 400

        role = Role(
            name=name,
            permissions=json.dumps([])
        )

        db.session.add(role)
        db.session.commit()

        return jsonify({
            'message': '角色添加成功',
            'role': role.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/roles/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加角色失败: {str(e)}'}), 500


@permission_bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """删除角色"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        role = Role.query.get(role_id)
        if not role:
            return jsonify({'error': '角色不存在'}), 404

        db.session.delete(role)
        db.session.commit()

        return jsonify({'message': '角色删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/roles/{role_id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除角色失败: {str(e)}'}), 500


@permission_bp.route('/<int:role_id>/permissions', methods=['GET'])
@jwt_required()
def get_role_permissions(role_id):
    """获取指定角色的权限列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        role = Role.query.get(role_id)
        if not role:
            return jsonify({'error': '角色不存在'}), 404

        return jsonify({
            'role_id': role.id,
            'role_name': role.name,
            'permissions': role.to_dict()['permissions'],
            'permission_groups': ALL_PERMISSIONS
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/roles/{role_id}/permissions 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取权限列表失败: {str(e)}'}), 500


@permission_bp.route('/<int:role_id>/permissions', methods=['PUT'])
@jwt_required()
def update_role_permissions(role_id):
    """更新指定角色的权限列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        role = Role.query.get(role_id)
        if not role:
            return jsonify({'error': '角色不存在'}), 404

        data = request.get_json()
        if not data or 'permissions' not in data:
            return jsonify({'error': '请提供权限列表'}), 400

        permissions = data['permissions']
        if not isinstance(permissions, list):
            return jsonify({'error': '权限列表必须是数组'}), 400

        role.permissions = json.dumps(permissions)
        db.session.commit()

        # 站内信：角色权限变更，通知所有该角色的教师
        try:
            from models import send_notification, Teacher
            teachers = Teacher.query.filter_by(role_id=role.id).all()
            for t in teachers:
                if t.user_id:
                    send_notification(
                        t.user_id,
                        '您的权限已更新，请重新登录查看',
                        content=f'您的角色“{role.name}”权限已更新，请重新登录以应用最新权限。',
                        type='permission_changed'
                    )
        except Exception:
            db.session.rollback()
            # 通知失败不影响权限更新主流程

        log_action('update_permission', f'修改角色“{role.name}”权限', user=current_user)

        return jsonify({
            'message': '权限更新成功',
            'role': role.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/roles/{role_id}/permissions 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新权限失败: {str(e)}'}), 500


@permission_bp.route('/permissions/all', methods=['GET'])
@jwt_required()
def get_all_permissions():
    """获取所有权限项（用于前端展示）"""
    try:
        return jsonify({
            'permission_groups': ALL_PERMISSIONS
        }), 200
    except Exception as e:
        import traceback
        print(f"\n=== GET /api/roles/permissions/all 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取权限列表失败: {str(e)}'}), 500