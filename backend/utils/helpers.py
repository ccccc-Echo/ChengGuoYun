import os
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


def generate_password_hash_pbkdf2(password):
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password_hash(password_hash, password):
    return check_password_hash(password_hash, password)


def generate_salt(length=16):
    return os.urandom(length).hex()


def generate_sha256_hash(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def generate_token(length=32):
    return os.urandom(length).hex()


def get_level_priority(level):
    priority_map = {
        '国家级': 3,
        '省级': 2,
        '校级': 1
    }
    return priority_map.get(level, 0)


def normalize_phone(phone):
    if not phone:
        return None
    return ''.join(filter(str.isdigit, phone))


def sanitize_filename(filename):
    import re
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    return filename.strip()


def parse_int_or_none(value):
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_float_or_none(value):
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None