"""竞赛信息接口（第二课堂）"""
import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Competition, CompetitionFavorite, User
from extensions import db

competition_bp = Blueprint('competition', __name__, url_prefix='/api/competitions')


@competition_bp.route('', methods=['GET'])
@jwt_required()
def list_competitions():
    """获取竞赛列表，支持 month / category / keyword 筛选"""
    try:
        current_user_id = int(get_jwt_identity())
        month = request.args.get('month', '').strip()
        category = request.args.get('category', '').strip()
        keyword = request.args.get('keyword', '').strip()

        query = Competition.query

        if month:
            query = query.filter(Competition.month == month)
        if category:
            query = query.filter(Competition.category == category)
        if keyword:
            like = f'%{keyword}%'
            query = query.filter(Competition.name.like(like))

        competitions = query.order_by(Competition.month, Competition.id).all()

        # 附带当前用户已收藏的竞赛 id，用于前端标记“想参加”状态
        fav_ids = {
            f.competition_id
            for f in CompetitionFavorite.query.filter_by(user_id=current_user_id).all()
        }

        return jsonify({
            'competitions': [c.to_dict(favorited=c.id in fav_ids) for c in competitions],
            'total': len(competitions)
        }), 200
    except Exception as e:
        return jsonify({'error': f'获取竞赛列表失败: {str(e)}'}), 500


@competition_bp.route('/categories', methods=['GET'])
@jwt_required()
def list_categories():
    """获取全部竞赛分类（去重）"""
    try:
        rows = (
            Competition.query
            .with_entities(Competition.category)
            .distinct()
            .order_by(Competition.category)
            .all()
        )
        categories = [r[0] for r in rows if r[0]]
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': f'获取竞赛分类失败: {str(e)}'}), 500


@competition_bp.route('/recommend', methods=['GET'])
@jwt_required()
def recommend_competitions():
    """广告牌推荐：随机取比赛用于轮播推荐"""
    try:
        limit = int(request.args.get('limit', 5))
        # 热度为 0 阶段：随机抽取；后续可按热度/专业匹配扩展
        ids = [c.id for c in Competition.query.with_entities(Competition.id).all()]
        random.shuffle(ids)
        pick = ids[:limit]
        competitions = Competition.query.filter(Competition.id.in_(pick)).all()
        random.shuffle(competitions)
        return jsonify({'competitions': [c.to_dict() for c in competitions]}), 200
    except Exception as e:
        return jsonify({'error': f'获取推荐失败: {str(e)}'}), 500


@competition_bp.route('/hot', methods=['GET'])
@jwt_required()
def hot_competitions():
    """热搜榜：按热度排序取前 N；热度均为 0 时随机抽取"""
    try:
        limit = int(request.args.get('limit', 5))
        competitions = Competition.query.order_by(Competition.heat.desc(), Competition.id).limit(limit * 3).all()
        if competitions and all(c.heat == 0 for c in competitions):
            random.shuffle(competitions)
            competitions = competitions[:limit]
        else:
            competitions = competitions[:limit]
        return jsonify({'competitions': [c.to_dict() for c in competitions]}), 200
    except Exception as e:
        return jsonify({'error': f'获取热搜失败: {str(e)}'}), 500


@competition_bp.route('/favorites', methods=['GET'])
@jwt_required()
def my_favorites():
    """我的比赛：当前用户收藏的竞赛列表"""
    try:
        current_user_id = int(get_jwt_identity())
        favorites = (
            CompetitionFavorite.query
            .filter_by(user_id=current_user_id)
            .order_by(CompetitionFavorite.created_at.desc())
            .all()
        )
        return jsonify({
            'favorites': [f.to_dict() for f in favorites],
            'total': len(favorites)
        }), 200
    except Exception as e:
        return jsonify({'error': f'获取我的比赛失败: {str(e)}'}), 500


@competition_bp.route('/favorites/<int:competition_id>', methods=['POST'])
@jwt_required()
def add_favorite(competition_id):
    """收藏比赛（想参加）"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        competition = Competition.query.get(competition_id)
        if not competition:
            return jsonify({'error': '比赛不存在'}), 404

        exists = CompetitionFavorite.query.filter_by(
            user_id=current_user_id, competition_id=competition_id
        ).first()
        if exists:
            return jsonify({'error': '已在我的比赛中'}), 400

        fav = CompetitionFavorite(user_id=current_user_id, competition_id=competition_id)
        db.session.add(fav)
        competition.heat += 1
        db.session.commit()
        return jsonify({'favorite': fav.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'收藏失败: {str(e)}'}), 500


@competition_bp.route('/favorites/<int:competition_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(competition_id):
    """取消收藏比赛"""
    try:
        current_user_id = int(get_jwt_identity())
        fav = CompetitionFavorite.query.filter_by(
            user_id=current_user_id, competition_id=competition_id
        ).first()
        if not fav:
            return jsonify({'error': '未收藏该比赛'}), 404

        db.session.delete(fav)
        competition = Competition.query.get(competition_id)
        if competition and competition.heat > 0:
            competition.heat -= 1
        db.session.commit()
        return jsonify({'message': '已取消收藏'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'取消收藏失败: {str(e)}'}), 500
