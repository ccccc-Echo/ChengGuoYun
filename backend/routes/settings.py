from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, AchievementKnowledge
from extensions import db

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')


def find_duplicate_category(name, sub_category, exclude_id=None):
    """检查奖项类型是否重复（一级分类 + 二级分类组合），空字符串与 NULL 视为相同"""
    name = (name or '').strip()
    sub = sub_category or ''
    query = AchievementKnowledge.query.filter(AchievementKnowledge.category == name)
    if sub:
        query = query.filter(AchievementKnowledge.sub_category == sub)
    else:
        query = query.filter(
            db.or_(AchievementKnowledge.sub_category == '', AchievementKnowledge.sub_category.is_(None))
        )
    if exclude_id:
        query = query.filter(AchievementKnowledge.id != exclude_id)
    return query.first()


@settings_bp.route('/categories/', methods=['GET'])
@jwt_required()
def list_categories():
    """获取奖项类型列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        query = AchievementKnowledge.query

        # 按一级分类、二级分类的首字母（A-Z）排序：
        # 一级分类按中文拼音；二级分类拉丁字母开头排前、再按中文拼音
        zh_collation = 'utf8mb4_zh_0900_as_cs'
        paginated = query.order_by(
            AchievementKnowledge.category.collate(zh_collation),
            db.text("CASE WHEN sub_category REGEXP '^[a-zA-Z]' THEN 0 ELSE 1 END"),
            AchievementKnowledge.sub_category.collate(zh_collation)
        ).paginate(page=page, per_page=page_size, error_out=False)

        categories = []
        for item in paginated.items:
            categories.append({
                'id': item.id,
                'name': item.category,
                'sub_category': item.sub_category,
                'description': item.proof_required,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else None
            })

        return jsonify({
            'categories': categories,
            'pagination': {
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': paginated.page,
                'per_page': paginated.per_page
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/settings/categories/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取奖项类型失败: {str(e)}'}), 500


@settings_bp.route('/categories/', methods=['POST'])
@jwt_required()
def create_category():
    """添加奖项类型"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        data = request.get_json()
        required_fields = ['name']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        # 唯一性校验：一级分类 + 二级分类组合不可重复
        if find_duplicate_category(data['name'], data.get('sub_category')):
            return jsonify({'error': '该奖项类型已存在（一级分类与二级分类组合重复）'}), 400

        category = AchievementKnowledge(
            name=data['name'],
            category=data['name'],
            sub_category=data.get('sub_category'),
            proof_required=data.get('description'),
            level='校级',
            keywords=''
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            'message': '奖项类型添加成功',
            'category': {
                'id': category.id,
                'name': category.category,
                'sub_category': category.sub_category,
                'description': category.proof_required
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/settings/categories/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加奖项类型失败: {str(e)}'}), 500


@settings_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    """修改奖项类型"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        category = AchievementKnowledge.query.get(id)
        if not category:
            return jsonify({'error': '奖项类型不存在'}), 404

        data = request.get_json()

        # 计算更新后的值（用于唯一性校验）
        new_name = data['name'] if 'name' in data else category.category
        new_sub = data['sub_category'] if 'sub_category' in data else category.sub_category

        # 唯一性校验：一级分类 + 二级分类组合不可与其他记录重复
        if find_duplicate_category(new_name, new_sub, exclude_id=id):
            return jsonify({'error': '该奖项类型已存在（一级分类与二级分类组合重复）'}), 400

        if 'name' in data:
            category.category = data['name']
        if 'sub_category' in data:
            category.sub_category = data['sub_category']
        if 'description' in data:
            category.proof_required = data['description']

        db.session.commit()

        return jsonify({
            'message': '奖项类型更新成功',
            'category': {
                'id': category.id,
                'name': category.category,
                'sub_category': category.sub_category,
                'description': category.proof_required
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/settings/categories/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新奖项类型失败: {str(e)}'}), 500


@settings_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    """删除奖项类型"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        category = AchievementKnowledge.query.get(id)
        if not category:
            return jsonify({'error': '奖项类型不存在'}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': '奖项类型删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/settings/categories/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除奖项类型失败: {str(e)}'}), 500


@settings_bp.route('/knowledge/', methods=['GET'])
@jwt_required()
def list_knowledge():
    """获取成果知识库列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        query = AchievementKnowledge.query

        paginated = query.order_by(AchievementKnowledge.id).paginate(page=page, per_page=page_size, error_out=False)

        knowledge = []
        for item in paginated.items:
            knowledge.append({
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'sub_category': item.sub_category,
                'level': item.level,
                'keywords': item.keywords,
                'proof_required': item.proof_required,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else None
            })

        return jsonify({
            'knowledge': knowledge,
            'pagination': {
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': paginated.page,
                'per_page': paginated.per_page
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/settings/knowledge/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取知识库失败: {str(e)}'}), 500


@settings_bp.route('/knowledge/', methods=['POST'])
@jwt_required()
def create_knowledge():
    """添加知识库条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        data = request.get_json()
        required_fields = ['name', 'category', 'level']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        knowledge = AchievementKnowledge(
            name=data['name'],
            category=data['category'],
            sub_category=data.get('sub_category'),
            level=data['level'],
            keywords=data.get('keywords'),
            proof_required=data.get('proof_required')
        )

        db.session.add(knowledge)
        db.session.commit()

        return jsonify({
            'message': '知识库条目添加成功',
            'knowledge': {
                'id': knowledge.id,
                'name': knowledge.name,
                'category': knowledge.category,
                'sub_category': knowledge.sub_category,
                'level': knowledge.level,
                'keywords': knowledge.keywords,
                'proof_required': knowledge.proof_required
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/settings/knowledge/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加知识库条目失败: {str(e)}'}), 500


@settings_bp.route('/knowledge/<int:id>', methods=['PUT'])
@jwt_required()
def update_knowledge(id):
    """修改知识库条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        knowledge = AchievementKnowledge.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识库条目不存在'}), 404

        data = request.get_json()

        if 'name' in data:
            knowledge.name = data['name']
        if 'category' in data:
            knowledge.category = data['category']
        if 'sub_category' in data:
            knowledge.sub_category = data['sub_category']
        if 'level' in data:
            knowledge.level = data['level']
        if 'keywords' in data:
            knowledge.keywords = data['keywords']
        if 'proof_required' in data:
            knowledge.proof_required = data['proof_required']

        db.session.commit()

        return jsonify({
            'message': '知识库条目更新成功',
            'knowledge': {
                'id': knowledge.id,
                'name': knowledge.name,
                'category': knowledge.category,
                'sub_category': knowledge.sub_category,
                'level': knowledge.level,
                'keywords': knowledge.keywords,
                'proof_required': knowledge.proof_required
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/settings/knowledge/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新知识库条目失败: {str(e)}'}), 500


@settings_bp.route('/knowledge/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge(id):
    """删除知识库条目"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问'}), 403

        knowledge = AchievementKnowledge.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识库条目不存在'}), 404

        db.session.delete(knowledge)
        db.session.commit()

        return jsonify({'message': '知识库条目删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/settings/knowledge/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除知识库条目失败: {str(e)}'}), 500