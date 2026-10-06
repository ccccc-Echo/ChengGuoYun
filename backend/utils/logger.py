"""日志系统：文件日志 + 数据库操作日志

- 文件日志：按天分割，保存于 backend/logs/app-YYYY-MM-DD.log，保留 30 天自动清理
- 数据库日志：记录关键操作到 system_logs 表，供管理端「系统日志」页面查询
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request
from flask_jwt_extended import get_jwt_identity

_initialized = False


def setup_logger():
    """初始化文件日志（按天分割、保留 30 天）"""
    global _initialized
    if _initialized:
        return logging.getLogger('app')

    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    handler = TimedRotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    handler.suffix = '%Y-%m-%d'

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)
    # 避免重复添加 handler
    if logger.handlers:
        logger.handlers = []
    logger.addHandler(handler)
    # 防止日志向上传播导致重复输出
    logger.propagate = False

    _initialized = True
    return logger


def get_client_ip():
    """获取客户端 IP"""
    try:
        ip = request.headers.get('X-Forwarded-For', '')
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        if not ip:
            ip = request.remote_addr or ''
        return ip
    except Exception:
        return ''


def _get_current_user():
    """从 JWT 解析当前登录用户"""
    try:
        uid = get_jwt_identity()
        if uid:
            uid = int(uid)
            from models import User
            return User.query.get(uid)
    except Exception:
        pass
    return None


def log_action(action_type, action_detail, level='INFO', result='success', user=None):
    """记录一条操作日志：写文件日志 + 写入 system_logs 表

    参数:
        action_type: 操作类型（如 login、add_achievement）
        action_detail: 操作详情（如 提交成果"XXX"，状态：待审核）
        level: 日志级别 INFO / ERROR
        result: 操作结果 success / fail
        user: 操作者 User 对象（未登录场景如登录成功时显式传入；否则从 JWT 解析）
    """
    logger = logging.getLogger('app')
    ip = get_client_ip()

    # 1) 文件日志
    logger.log(
        getattr(logging, level.upper(), logging.INFO),
        "%s | %s | IP:%s | result:%s",
        action_type, action_detail, ip, result
    )

    # 2) 数据库日志
    if user is None:
        user = _get_current_user()

    try:
        from extensions import db
        from models import SystemLog

        oplog = SystemLog(
            user_id=user.id if user else None,
            username=user.username if user else '',
            role=user.role if user else '',
            action_type=action_type,
            action_detail=action_detail,
            ip_address=ip,
            result=result,
            level=level,
        )
        db.session.add(oplog)
        db.session.commit()
    except Exception as e:
        try:
            db.session.rollback()
        except Exception:
            pass
        logger.error("写入系统日志失败: %s", str(e))