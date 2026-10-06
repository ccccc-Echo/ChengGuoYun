from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, AchievementKnowledge
from extensions import db
from decorators.permissions import admin_required, role_required
from utils.helpers import get_level_priority
from datetime import datetime

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')


@knowledge_bp.route('/', methods=['GET'])
@jwt_required()
def search_knowledge():
    """搜索知识库"""
    try:
        keyword = request.args.get('keyword', '')
        category = request.args.get('category')
        sub_category = request.args.get('sub_category')
        level = request.args.get('level')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        query = AchievementKnowledge.query

        if keyword:
            query = query.filter(
                AchievementKnowledge.name.like(f'%{keyword}%') |
                AchievementKnowledge.keywords.like(f'%{keyword}%')
            )

        if category:
            query = query.filter(AchievementKnowledge.category == category)

        if sub_category:
            query = query.filter(AchievementKnowledge.sub_category == sub_category)

        if level:
            query = query.filter(AchievementKnowledge.level == level)

        query = query.order_by(AchievementKnowledge.level_priority.desc(), AchievementKnowledge.name)
        paginated = query.paginate(page=page, per_page=page_size, error_out=False)

        return jsonify({
            'knowledge': [item.to_dict() for item in paginated.items],
            'pagination': {
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': paginated.page,
                'per_page': paginated.per_page
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/knowledge/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'搜索知识库失败: {str(e)}'}), 500


@knowledge_bp.route('/', methods=['POST'])
@jwt_required()
def add_knowledge():
    """管理员添加知识条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role != 'head':
                return jsonify({'error': '无权添加知识条目'}), 403
        else:
            return jsonify({'error': '无权添加知识条目'}), 403

        data = request.get_json()
        required_fields = ['name', 'category', 'level']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        if AchievementKnowledge.query.filter_by(name=data['name']).first():
            return jsonify({'error': '成果名称已存在'}), 400

        knowledge = AchievementKnowledge(
            name=data['name'],
            category=data['category'],
            sub_category=data.get('sub_category'),
            level=data['level'],
            level_priority=get_level_priority(data['level']),
            keywords=data.get('keywords', ''),
            proof_required=data.get('proof_required', ''),
            school_id=data.get('school_id', 0)
        )

        db.session.add(knowledge)
        db.session.commit()

        return jsonify({
            'message': '知识条目添加成功',
            'knowledge': knowledge.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/knowledge/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加知识条目失败: {str(e)}'}), 500


@knowledge_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_knowledge(id):
    """管理员修改知识条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role != 'head':
                return jsonify({'error': '无权修改知识条目'}), 403
        else:
            return jsonify({'error': '无权修改知识条目'}), 403

        knowledge = AchievementKnowledge.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识条目不存在'}), 404

        data = request.get_json()

        if 'name' in data:
            knowledge.name = data['name']
        if 'category' in data:
            knowledge.category = data['category']
        if 'sub_category' in data:
            knowledge.sub_category = data['sub_category']
        if 'level' in data:
            knowledge.level = data['level']
            knowledge.level_priority = get_level_priority(data['level'])
        if 'keywords' in data:
            knowledge.keywords = data['keywords']
        if 'proof_required' in data:
            knowledge.proof_required = data['proof_required']
        if 'school_id' in data:
            knowledge.school_id = data['school_id']

        knowledge.updated_at = datetime.now()

        db.session.commit()

        return jsonify({
            'message': '知识条目更新成功',
            'knowledge': knowledge.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/knowledge/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新知识条目失败: {str(e)}'}), 500


@knowledge_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge(id):
    """管理员删除知识条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role != 'head':
                return jsonify({'error': '无权删除知识条目'}), 403
        else:
            return jsonify({'error': '无权删除知识条目'}), 403

        knowledge = AchievementKnowledge.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识条目不存在'}), 404

        db.session.delete(knowledge)
        db.session.commit()

        return jsonify({'message': '知识条目删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/knowledge/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除知识条目失败: {str(e)}'}), 500


@knowledge_bp.route('/import', methods=['POST'])
@jwt_required()
def import_knowledge():
    """批量导入 Excel"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role != 'head':
                return jsonify({'error': '无权导入知识条目'}), 403
        else:
            return jsonify({'error': '无权导入知识条目'}), 403

        if 'file' not in request.files:
            return jsonify({'error': '请上传文件'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400

        if not file.filename.endswith('.xlsx') and not file.filename.endswith('.xls'):
            return jsonify({'error': '仅支持 Excel 文件'}), 400

        try:
            import pandas as pd
            df = pd.read_excel(file.stream)

            required_columns = ['name', 'category', 'level']
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                return jsonify({'error': f'Excel文件缺少必要列: {", ".join(missing_cols)}'}), 400

            success_count = 0
            fail_count = 0

            for _, row in df.iterrows():
                try:
                    if AchievementKnowledge.query.filter_by(name=row['name']).first():
                        fail_count += 1
                        continue

                    knowledge = AchievementKnowledge(
                        name=row['name'],
                        category=row['category'],
                        sub_category=row.get('sub_category'),
                        level=row['level'],
                        level_priority=get_level_priority(row['level']),
                        keywords=str(row.get('keywords', '')),
                        proof_required=str(row.get('proof_required', '')),
                        school_id=int(row.get('school_id', 0))
                    )
                    db.session.add(knowledge)
                    success_count += 1
                except Exception as row_error:
                    fail_count += 1
                    print(f"导入第{_+1}行失败: {str(row_error)}")

            db.session.commit()

            return jsonify({
                'message': '导入完成',
                'success_count': success_count,
                'fail_count': fail_count
            }), 200

        except ImportError:
            return jsonify({'error': '请安装 pandas 库'}), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'导入失败: {str(e)}'}), 500

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/knowledge/import 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导入失败: {str(e)}'}), 500