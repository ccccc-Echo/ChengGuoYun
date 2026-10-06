"""系统日志查询接口（管理员）"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, SystemLog

logs_bp = Blueprint('logs', __name__, url_prefix='/api/logs')


@logs_bp.route('/', methods=['GET'])
@jwt_required()
def get_system_logs():
    """分页查询系统日志，支持日期范围 / 操作类型 / 用户筛选"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'admin':
            return jsonify({'code': 403, 'message': '无权限访问'}), 403

        # 分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        page_size = min(max(page_size, 1), 100)

        query = SystemLog.query

        # 操作类型
        action_type = request.args.get('action_type', '').strip()
        if action_type:
            query = query.filter(SystemLog.action_type == action_type)
        # 用户（支持模糊匹配）
        username = request.args.get('username', '').strip()
        if username:
            query = query.filter(SystemLog.username.like(f'%{username}%'))
        # 日期范围
        start_date = request.args.get('start_date', '').strip()
        if start_date:
            query = query.filter(SystemLog.created_at >= start_date)
        end_date = request.args.get('end_date', '').strip()
        if end_date:
            query = query.filter(SystemLog.created_at <= f'{end_date} 23:59:59')

        total = query.count()
        logs = (
            query.order_by(SystemLog.created_at.desc(), SystemLog.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return jsonify({
            'code': 200,
            'data': {
                'items': [lg.to_dict() for lg in logs],
                'total': total,
                'page': page,
                'page_size': page_size,
                'action_types': get_action_types()
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== 查询系统日志错误 ===")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'查询系统日志失败: {str(e)}'}), 500


def get_action_types():
    """返回已记录的去重操作类型列表，供前端筛选项使用"""
    types = [r[0] for r in
             SystemLog.query.with_entities(SystemLog.action_type).distinct().all()]
    return [t for t in types if t]