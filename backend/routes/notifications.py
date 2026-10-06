from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Notification, User
from extensions import db

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')


def _denied():
    return jsonify({'code': 403, 'message': '管理员无消息通知功能'}), 403


@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """获取当前用户的消息列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        if current_user.role == 'admin':
            return _denied()

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        unread_only = request.args.get('unread_only', '').lower() in ('true', '1')

        query = Notification.query.filter_by(user_id=current_user.id)
        if unread_only:
            query = query.filter_by(is_read=0)

        pagination = query.order_by(Notification.created_at.desc(), Notification.id.desc()).paginate(
            page=page, per_page=page_size, error_out=False)

        return jsonify({
            'code': 200,
            'data': {
                'notifications': [n.to_dict() for n in pagination.items],
                'pagination': {
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'current_page': page,
                    'per_page': page_size,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                },
                'unread_count': Notification.query.filter_by(user_id=current_user.id, is_read=0).count()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'获取消息失败: {str(e)}'}), 500


@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def unread_count():
    """获取未读消息数量"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        if current_user.role == 'admin':
            return _denied()

        count = Notification.query.filter_by(user_id=current_user.id, is_read=0).count()
        return jsonify({'code': 200, 'data': {'unread_count': count}}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'获取未读消息数量失败: {str(e)}'}), 500


@notification_bp.route('/<int:id>/read', methods=['PUT'])
@jwt_required()
def mark_read(id):
    """将单条消息标记为已读"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        if current_user.role == 'admin':
            return _denied()

        notification = Notification.query.filter_by(id=id, user_id=current_user.id).first()
        if not notification:
            return jsonify({'code': 404, 'message': '消息不存在'}), 404

        notification.is_read = 1
        db.session.commit()

        return jsonify({'code': 200, 'message': '已标记为已读'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'标记已读失败: {str(e)}'}), 500


@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def read_all():
    """将该用户全部消息标记为已读"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        if current_user.role == 'admin':
            return _denied()

        Notification.query.filter_by(user_id=current_user.id, is_read=0).update({'is_read': 1})
        db.session.commit()

        return jsonify({'code': 200, 'message': '全部已标记为已读'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'全部标记已读失败: {str(e)}'}), 500