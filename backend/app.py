from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os
from dotenv import load_dotenv

# 兼容补丁：本机 venv 为 Python 3.8，而 reportlab(>=4.x) 调用了 hashlib.md5(..., usedforsecurity=...)
# 该关键字参数仅 Python 3.9+ 支持，故为低版本 Python 包装 md5 以忽略该参数，修复 PDF 导出
import hashlib
if 'usedforsecurity' not in __import__('inspect').signature(hashlib.md5).parameters:
    _orig_md5 = hashlib.md5
    def _md5_shim(arg=b'', **kw):
        kw.pop('usedforsecurity', None)
        return _orig_md5(arg, **kw)
    hashlib.md5 = _md5_shim

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from config import config
from extensions import init_extensions, limiter
from models import db
from routes.auth import auth_bp
from routes.achievements import achievement_bp
from routes.stats import stats_bp
from routes.students import student_bp
# from routes.classes import class_bp  # TODO(未来) 接入学校系统重建“班级”功能时恢复
from routes.teachers import teacher_bp
from routes.knowledge import knowledge_bp
from routes.settings import settings_bp
from routes.courses import course_bp
from routes.permissions import permission_bp, init_default_roles
from routes.teams import team_bp
from routes.register import register_bp
from routes.knowledge_base import knowledge_base_bp
from routes.export import export_bp, teacher_export_bp
from routes.user import user_bp
from routes.logs import logs_bp
from routes.backup import backup_bp
from routes.notifications import notification_bp
from routes.ai import ai_bp
from routes.competitions import competition_bp
from utils.logger import setup_logger

# 初始化文件日志（按天分割，保留30天自动清理）
setup_logger()

app = Flask(__name__)

app.url_map.strict_slashes = False

env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

init_extensions(app)

app.register_blueprint(auth_bp)
app.register_blueprint(achievement_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(student_bp)
# app.register_blueprint(class_bp)  # TODO(未来) 恢复班级功能时启用
app.register_blueprint(teacher_bp)
app.register_blueprint(knowledge_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(course_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(team_bp)
app.register_blueprint(register_bp)
app.register_blueprint(knowledge_base_bp)
app.register_blueprint(export_bp)
app.register_blueprint(teacher_export_bp)
app.register_blueprint(user_bp)
app.register_blueprint(logs_bp)
app.register_blueprint(backup_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(competition_bp)

# Swagger 接口文档
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': '成果云系统API文档'}
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)


@app.route('/')
def index():
    """根路径"""
    return jsonify({
        'message': '成果云系统 API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'achievements': '/api/achievements',
            'stats': '/api/stats',
            'students': '/api/students',
            'teachers': '/api/teachers',
            'knowledge': '/api/knowledge',
            'courses': '/api/courses'
        }
    })


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """提供上传文件访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/health')
def health():
    """健康检查"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 500


# 统一 JSON 错误响应
def error_response(code, message):
    return jsonify({'code': code, 'message': message}), code


# 覆盖 flask_jwt_extended 默认的 {'msg': ...} 错误格式，统一为项目 JSON 结构
from flask_jwt_extended.exceptions import (
    JWTExtendedException, NoAuthorizationError, InvalidHeaderError,
    InvalidQueryParamError, JWTDecodeError, FreshTokenRequired,
    RevokedTokenError, WrongTokenError, UserLookupError,
    UserClaimsVerificationError,
)
def _jwt_error(error):
    return error_response(401, '未登录或登录已过期')
for _exc in (
    JWTExtendedException, NoAuthorizationError, InvalidHeaderError,
    InvalidQueryParamError, JWTDecodeError, FreshTokenRequired,
    RevokedTokenError, WrongTokenError, UserLookupError,
    UserClaimsVerificationError,
):
    app.errorhandler(_exc)(_jwt_error)


@app.errorhandler(404)
def not_found(error):
    """404 资源不存在"""
    return error_response(404, '请求的资源不存在')


@app.errorhandler(400)
def bad_request(error):
    """400 请求参数错误"""
    return error_response(400, '请求参数错误')


@app.errorhandler(401)
def unauthorized(error):
    """401 未登录或登录已过期"""
    return error_response(401, '未登录或登录已过期')


@app.errorhandler(403)
def forbidden(error):
    """403 无权限访问"""
    return error_response(403, '无权限访问')


@app.errorhandler(429)
def ratelimit_handler(error):
    """429 请求过于频繁"""
    return error_response(429, '请求过于频繁，请稍后重试')


# ============ 全局默认限流：普通接口每分钟最多 60 次（按 IP + 接口维度） ============
from collections import defaultdict
from time import time as _time
_rate_window = 60.0     # 窗口：秒
_rate_max = 60          # 窗口内最大请求数
_rate_logs = defaultdict(list)  # (ip, endpoint) -> [timestamp, ...]


@app.before_request
def global_rate_limit():
    from flask import request as _req
    ip = _req.remote_addr or 'unknown'
    endpoint = _req.endpoint or _req.path
    key = (ip, endpoint)
    now = _time()
    window = _rate_logs[key]
    while window and now - window[0] > _rate_window:
        window.pop(0)
    if len(window) >= _rate_max:
        return error_response(429, '请求过于频繁，请稍后重试')
    window.append(now)


@app.errorhandler(422)
def unprocessable_entity(error):
    """422 请求无法处理（统一视为参数错误）"""
    return error_response(400, '请求参数错误')


@app.errorhandler(500)
def internal_error(error):
    """500 服务器内部错误"""
    import logging
    logging.getLogger('app').error(
        f'500 错误: {error!r}', exc_info=True
    )
    db.session.rollback()
    return error_response(500, '服务器内部错误，请稍后重试')


@app.errorhandler(Exception)
def handle_exception(error):
    """全局兜底：捕获所有未处理异常，记录日志并返回友好提示"""
    import logging
    logging.getLogger('app').error(
        f'未捕获异常: {error!r}', exc_info=True
    )
    try:
        db.session.rollback()
    except Exception:
        pass
    return error_response(500, '服务器内部错误，请稍后重试')


def create_app(config_name='default'):
    """应用工厂函数"""
    global app
    app.config.from_object(config[config_name])
    return app


if __name__ == '__main__':
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'achievements'), exist_ok=True)

    with app.app_context():
        db.create_all()

        from models import User
        init_default_roles()
        
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print(f"发现管理员账号: {admin_user.username}")
            print(f"当前密码哈希: {admin_user.password_hash}")
            
            try:
                from werkzeug.security import check_password_hash
                password_valid = check_password_hash(admin_user.password_hash, '123456')
                print(f"密码验证结果: {password_valid}")
                
                if not password_valid:
                    print("密码验证失败，重新设置密码...")
                    admin_user.set_password('123456')
                    db.session.commit()
                    print("管理员密码已重置为: 123456")
            except Exception as e:
                print(f"密码验证出错: {e}")
                print("重新设置密码...")
                admin_user.set_password('123456')
                db.session.commit()
                print("管理员密码已重置为: 123456")
        else:
            print("创建默认管理员账号...")
            admin_user = User(
                username='admin',
                role='admin',
                name='系统管理员',
                email='admin@school.edu.cn'
            )
            admin_user.set_password('123456')
            db.session.add(admin_user)
            db.session.commit()
            print("默认管理员账号创建成功: admin / 123456")

    app.debug = True
    print(f"DEBUG mode: {app.debug}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    try:
        print(f"LIMITER default_limits: {[str(x) for x in limiter.limit_manager.default_limits]}")
    except Exception as e:
        print(f"LIMITER debug: {e!r}")

    app.run(host='0.0.0.0', port=5000, debug=True)