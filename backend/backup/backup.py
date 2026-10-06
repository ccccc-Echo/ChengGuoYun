#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库自动备份脚本
- 使用 mysqldump 导出数据库到 backup/ 目录，文件名格式：achievement_db_YYYY-MM-DD.sql
- 支持传入日期参数（便于测试历史清理）：python backup.py 或 python backup.py 2026-09-15
- 执行后自动删除 30 天前的备份文件

用法：
  python backup.py              # 用当天日期生成备份并清理过期文件
  python backup.py 2026-01-01   # 用指定日期生成备份（供测试 30 天清理用）

依赖：
  - mysqldump 需在系统 PATH 中，或通过 MySQL_BIN 环境变量指定完整路径
  - 数据库连接参数读取 backend/.env（DATABASE_URL）
"""
import os
import re
import sys
import glob
import datetime
import subprocess
from pathlib import Path

# backend 目录（本文件位于 backend/backup/backup.py 时，脚本通常从 backend 目录调用）
SCRIPT_DIR = Path(__file__).resolve().parent        # .../backend/backup
BACKEND_DIR = SCRIPT_DIR.parent                     # .../backend
BACKUP_DIR = SCRIPT_DIR                             # .../backend/backup

RETENTION_DAYS = 30


def load_db_config():
    """从 backend/.env 读取 DATABASE_URL，解析出 host/port/user/password/database"""
    env_path = BACKEND_DIR / '.env'
    env_vars = {}
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            env_vars[key.strip()] = value.strip()

    url = env_vars.get('DATABASE_URL', '')
    # 匹配 mysql+pymysql://user:pass@host:port/db?charset=...
    m = re.match(
        r'mysql(?:://|(?:\+pymysql)?://)([^:]+):([^@]+)@([^:]+):(\d+)/([^?]+)',
        url
    )
    if not m:
        raise RuntimeError(f'无法解析 DATABASE_URL: {url}')

    user, password, host, port, database = m.groups()
    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
    }


def find_mysqldump():
    """定位 mysqldump 可执行文件"""
    # 1) 环境变量指定
    mysql_bin = os.getenv('MySQL_BIN', '')
    # 2) 常见默认安装路径
    common_paths = [
        r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.3\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.2\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.1\bin\mysqldump.exe',
        r'C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe',
        r'C:\mysql\bin\mysqldump.exe',
    ]
    candidates = [mysql_bin] + common_paths
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    # 3) 依赖 PATH
    return 'mysqldump'


def run_backup(date_str=None):
    """执行一次备份，返回 (成功与否, 文件路径或错误信息)"""
    db = load_db_config()
    mysqldump = find_mysqldump()

    if date_str:
        target_date = date_str
    else:
        target_date = datetime.date.today().strftime('%Y-%m-%d')

    backup_file = BACKUP_DIR / f"achievement_db_{target_date}.sql"

    # cmd 命令（避免密码出现在进程列表可用 --password=，这里直接参数方式）
    cmd = [
        mysqldump,
        f'-h{db["host"]}',
        f'-P{db["port"]}',
        f'-u{db["user"]}',
        f'-p{db["password"]}',
        '--default-character-set=utf8mb4',
        '--single-transaction',
        '--routines',
        '--triggers',
        db['database'],
    ]

    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
        if result.returncode != 0:
            return False, f'mysqldump 失败: {result.stderr.strip()}'

        if not backup_file.exists() or backup_file.stat().st_size == 0:
            return False, '备份文件生成失败（文件为空）'

        # 清理 30 天前的备份
        cleanup_old_backups()
        return True, str(backup_file)
    except FileNotFoundError as e:
        return False, f'未找到 mysqldump，请安装 MySQL 或设置 MySQL_BIN 环境变量: {e}'
    except Exception as e:
        return False, f'备份失败: {e}'


def cleanup_old_backups():
    """删除备份目录中超过 RETENTION_DAYS 天（默认30天）的备份文件"""
    cutoff = datetime.date.today() - datetime.timedelta(days=RETENTION_DAYS)
    cutoff_str = cutoff.strftime('%Y-%m-%d')
    removed = 0
    for f in glob.glob(str(BACKUP_DIR / 'achievement_db_*.sql')):
        name = os.path.basename(f)
        m = re.match(r'achievement_db_(\d{4}-\d{2}-\d{2})\.sql$', name)
        if m:
            try:
                file_date = datetime.datetime.strptime(m.group(1), '%Y-%m-%d').date()
            except ValueError:
                continue
            if file_date < cutoff:
                try:
                    os.remove(f)
                    removed += 1
                except OSError:
                    pass
    if removed:
        print(f'已清理 {removed} 个过期备份文件（早于 {cutoff_str}）')
    return removed


if __name__ == '__main__':
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    ok, msg = run_backup(date_arg)
    print(msg)
    sys.exit(0 if ok else 1)