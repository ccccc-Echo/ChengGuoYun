from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

# 接口限流：按 IP 维度，内存存储（重启后重置）
# 注：default_limits 通过构造传但 init_app 后不绑定，全局 60/min 由 app.py 中的
# 手动 before_request 实现（见 apply_global_rate_limit 引用）。此处仅承载显式
# @limiter.limit 装饰，用于登录/注册等特定接口的严格限流。
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
)


def init_extensions(app):
    """初始化所有 Flask 扩展"""
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    limiter.init_app(app)

    return app