"""数据备份接口（管理员）"""
import os
import re
import sys
import glob
import datetime
import time
from flask import Blueprint, request, jsonify, send_from_directory, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from utils.logger import log_action

backup_bp = Blueprint('backup', __name__, url_prefix='/api/backup')

# 备份目录固定为 backend/backup
BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backup')


def require_admin():
    """校验当前用户是否为管理员，返回 User 或抛 401/403"""
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    if not current_user:
        abort(404, description='用户不存在')
    if current_user.role != 'admin':
        abort(403, description='无权访问')
    return current_user


def get_backup_files():
    """读取备份目录下的备份文件列表，按修改时间倒序"""
    files = []
    if not os.path.isdir(BACKUP_DIR):
        return files
    for f in glob.glob(os.path.join(BACKUP_DIR, 'achievement_db_*.sql')):
        name = os.path.basename(f)
        if not re.match(r'achievement_db_\d{4}-\d{2}-\d{2}\.sql$', name):
            continue
        stat = os.stat(f)
        files.append({
            'filename': name,
            'size': stat.st_size,
            'size_display': format_size(stat.st_size),
            'backup_time': datetime.datetime.fromtimestamp(
                stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'date': name.replace('achievement_db_', '').replace('.sql', ''),
        })
    files.sort(key=lambda x: x['date'], reverse=True)
    return files


def format_size(num):
    """格式化文件大小为可读文本"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num < 1024:
            return f'{num:.1f}{unit}' if unit != 'B' else f'{num}B'
        num /= 1024
    return f'{num:.1f}TB'


def sanitize_filename(filename):
    """校验并规范化备份文件名，防止路径穿越"""
    name = os.path.basename(filename)
    if not re.match(r'^achievement_db_\d{4}-\d{2}-\d{2}\.sql$', name):
        return None
    return name


@backup_bp.route('/list', methods=['GET'])
@jwt_required()
def backup_list():
    """获取备份列表"""
    try:
        require_admin()
        return jsonify({'code': 200, 'data': get_backup_files()}), 200
    except Exception as e:
        return jsonify({'error': f'获取备份列表失败: {e}'}), 500


@backup_bp.route('/create', methods=['POST'])
@jwt_required()
def backup_create():
    """手动触发一次备份"""
    admin = None
    try:
        admin = require_admin()
        sys_path = os.path.join(BACKUP_DIR, 'backup.py')
        sys.path.insert(0, BACKUP_DIR)
        import importlib.util
        spec = importlib.util.spec_from_file_location('bak_module', sys_path)
        bak = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bak)

        date_arg = request.get_json(silent=True) or {}
        target_date = date_arg.get('date') if isinstance(date_arg, dict) else None
        # 仅允许今天日期或合法历史日期，用于测试清理逻辑
        if target_date and not re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
            target_date = None

        ok, msg = bak.run_backup(target_date)
        log_action(
            'create_backup',
            f'手动备份数据库，结果：{"成功" if ok else "失败"}',
            level='INFO' if ok else 'ERROR',
            result='success' if ok else 'fail',
            user=admin,
        )
        if ok:
            return jsonify({'code': 200, 'message': '备份成功', 'data': {'path': msg}}), 200
        return jsonify({'error': msg}), 500
    except Exception as e:
        log_action('create_backup', f'手动备份数据库失败：{e}', level='ERROR',
                   result='fail', user=admin)
        return jsonify({'error': f'备份失败: {e}'}), 500


@backup_bp.route('/download/<path:filename>', methods=['GET'])
@jwt_required()
def backup_download(filename):
    """下载备份文件"""
    try:
        require_admin()
    except Exception as e:
        return jsonify({'error': str(e)}), (403 if '无权' in str(e) else 404)

    safe_name = sanitize_filename(filename)
    if not safe_name:
        return jsonify({'error': '非法文件名'}), 400
    file_path = os.path.join(BACKUP_DIR, safe_name)
    if not os.path.isfile(file_path):
        return jsonify({'error': '备份文件不存在'}), 404
    return send_from_directory(BACKUP_DIR, safe_name, as_attachment=True)


@backup_bp.route('/delete/<path:filename>', methods=['DELETE'])
@jwt_required()
def backup_delete(filename):
    """删除指定备份文件"""
    admin = None
    try:
        admin = require_admin()
        safe_name = sanitize_filename(filename)
        if not safe_name:
            return jsonify({'error': '非法文件名'}), 400
        file_path = os.path.join(BACKUP_DIR, safe_name)
        if not os.path.isfile(file_path):
            return jsonify({'error': '备份文件不存在'}), 404
        # Windows 下文件可能被短暂占用（如正在下载），做有限重试
        for attempt in range(3):
            try:
                os.remove(file_path)
                break
            except PermissionError:
                if attempt == 2:
                    raise
                time.sleep(0.3)
        log_action('delete_backup', f'删除备份文件"{safe_name}"', user=admin)
        return jsonify({'code': 200, 'message': '删除成功'}), 200
    except Exception as e:
        return jsonify({'error': f'删除失败: {e}'}), 500