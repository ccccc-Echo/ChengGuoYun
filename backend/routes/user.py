from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Student, Teacher
from extensions import db
import os
import uuid

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

ALLOWED_AVATAR_EXT = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AVATAR_EXT


@user_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传用户头像"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if 'avatar' not in request.files:
            return jsonify({'error': '请选择图片文件'}), 400

        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'error': '请选择图片文件'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的图片格式，请上传 png/jpg/jpeg/gif 文件'}), 400

        # 检查文件大小 (限制 5MB)
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        if file_size > 5 * 1024 * 1024:
            return jsonify({'error': '图片大小不能超过5MB'}), 400

        # 创建头像存储目录
        avatar_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)

        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{current_user_id}_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(avatar_dir, filename)

        # 保存文件
        file.save(filepath)

        # 更新数据库
        avatar_url = f"/uploads/avatars/{filename}"

        if current_user.role == 'student' and current_user.student:
            # 删除旧头像
            old_avatar = current_user.student.avatar
            if old_avatar and old_avatar.startswith('/uploads/'):
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_avatar.replace('/uploads/', ''))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass
            current_user.student.avatar = avatar_url
        elif current_user.role == 'teacher' and current_user.teacher:
            # 删除旧头像（如果有）
            old_avatar = getattr(current_user.teacher, 'avatar', None)
            if old_avatar and old_avatar.startswith('/uploads/'):
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_avatar.replace('/uploads/', ''))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass
            if not hasattr(current_user.teacher, 'avatar'):
                # 如果Teacher模型还没有avatar字段，暂时跳过
                pass
            else:
                current_user.teacher.avatar = avatar_url

        db.session.commit()

        return jsonify({
            'message': '头像上传成功',
            'avatar': avatar_url
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/user/avatar 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'上传失败: {str(e)}'}), 500


@user_bp.route('/avatar', methods=['GET'])
@jwt_required()
def get_avatar():
    """获取当前用户头像"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        avatar_url = None
        if current_user.role == 'student' and current_user.student:
            avatar_url = current_user.student.avatar
        elif current_user.role == 'teacher' and current_user.teacher:
            avatar_url = getattr(current_user.teacher, 'avatar', None)

        return jsonify({
            'avatar': avatar_url
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取头像失败: {str(e)}'}), 500
