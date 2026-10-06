from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Teacher, Team, TeamMember
from extensions import db
import random
import string

team_bp = Blueprint('team', __name__, url_prefix='/api/teams')


def generate_invite_code():
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(8))
    while Team.query.filter_by(invite_code=code).first():
        code = ''.join(random.choice(chars) for _ in range(8))
    return code


@team_bp.route('/', methods=['GET'])
@jwt_required()
def get_teams():
    """获取团队列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        tab = request.args.get('tab', 'my_created')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        name_filter = request.args.get('name', '').strip()
        creator_filter = request.args.get('creator', '').strip()

        if current_user.role == 'admin':
            query = Team.query
            if name_filter:
                query = query.filter(Team.name.contains(name_filter))
            if creator_filter:
                query = query.join(Team.creator).join(User).filter(User.name.contains(creator_filter))
            all_teams = query.all()
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({'teams': [], 'pagination': {'total': 0, 'page': 1, 'page_size': 20}}), 200

            if tab == 'my_created':
                query = Team.query.filter_by(creator_id=teacher.id)
                if name_filter:
                    query = query.filter(Team.name.contains(name_filter))
                if creator_filter:
                    query = query.join(Team.creator).join(User).filter(User.name.contains(creator_filter))
                all_teams = query.all()
            elif tab == 'joined':
                my_team_ids = [tm.team_id for tm in TeamMember.query.filter_by(teacher_id=teacher.id).all()]
                query = Team.query.filter(Team.id.in_(my_team_ids))
                if name_filter:
                    query = query.filter(Team.name.contains(name_filter))
                if creator_filter:
                    query = query.join(Team.creator).join(User).filter(User.name.contains(creator_filter))
                all_teams = query.all()
            else:
                my_team_ids = [tm.team_id for tm in TeamMember.query.filter_by(teacher_id=teacher.id).all()]
                query = Team.query.filter(Team.id.not_in(my_team_ids), Team.creator_id != teacher.id)
                if name_filter:
                    query = query.filter(Team.name.contains(name_filter))
                if creator_filter:
                    query = query.join(Team.creator).join(User).filter(User.name.contains(creator_filter))
                all_teams = query.all()
        else:
            return jsonify({'teams': [], 'pagination': {'total': 0, 'page': 1, 'page_size': 20}}), 200

        total = len(all_teams)
        start = (page - 1) * page_size
        end = start + page_size
        teams_page = all_teams[start:end]

        result = []
        for team in teams_page:
            member_count = TeamMember.query.filter_by(team_id=team.id).count()
            is_leader = team.creator_id == (current_user.teacher.id if current_user.role == 'teacher' else -1)
            include_joined = (tab == 'joined')
            teacher_id = teacher.id if current_user.role == 'teacher' else None
            team_data = team.to_dict(include_joined_at=include_joined, teacher_id=teacher_id)
            team_data['member_count'] = member_count
            team_data['is_leader'] = is_leader
            result.append(team_data)

        return jsonify({
            'teams': result,
            'pagination': {'total': total, 'page': page, 'page_size': page_size}
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取团队列表失败: {str(e)}'}), 500


@team_bp.route('/', methods=['POST'])
@jwt_required()
def create_team():
    """创建团队"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if current_user.role not in ['teacher', 'admin']:
            return jsonify({'error': '无权限创建团队'}), 403

        teacher = None
        if current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({'error': '教师信息不存在'}), 404
        else:
            data = request.get_json()
            creator_id = data.get('creator_id')
            if creator_id:
                teacher = Teacher.query.get(creator_id)
                if not teacher:
                    return jsonify({'error': '指定的创建者不存在'}), 404
            else:
                return jsonify({'error': '管理员创建团队需指定创建者'}), 400

        data = request.get_json()
        name = data.get('name')
        team_type = data.get('type', 'department')
        description = data.get('description', '')
        join_method = data.get('join_method', 'code')

        if not name:
            return jsonify({'error': '团队名称不能为空'}), 400

        if Team.query.filter_by(name=name).first():
            return jsonify({'error': '团队名称已存在'}), 400

        invite_code = generate_invite_code()

        team = Team(
            name=name,
            type=team_type,
            description=description,
            creator_id=teacher.id,
            invite_code=invite_code,
            join_method=join_method
        )
        db.session.add(team)
        db.session.flush()

        team_member = TeamMember(
            team_id=team.id,
            teacher_id=teacher.id,
            role='leader'
        )
        db.session.add(team_member)
        db.session.commit()

        return jsonify({
            'message': '团队创建成功',
            'team': team.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建团队失败: {str(e)}'}), 500


@team_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_team(id):
    """删除团队"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        team = Team.query.get(id)
        if not team:
            return jsonify({'error': '团队不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or team.creator_id != teacher.id:
                return jsonify({'error': '无权删除该团队'}), 403
        else:
            return jsonify({'error': '无权删除团队'}), 403

        db.session.delete(team)
        db.session.commit()

        return jsonify({'message': '团队删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除团队失败: {str(e)}'}), 500


@team_bp.route('/<int:id>/members', methods=['GET'])
@jwt_required()
def get_team_members(id):
    """获取团队成员"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        team = Team.query.get(id)
        if not team:
            return jsonify({'error': '团队不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({'error': '教师信息不存在'}), 404
            is_member = TeamMember.query.filter_by(team_id=id, teacher_id=teacher.id).first()
            if not is_member:
                return jsonify({'error': '您不是该团队成员'}), 403
        else:
            return jsonify({'error': '无权查看团队成员'}), 403

        members = TeamMember.query.filter_by(team_id=id).all()
        result = []
        for member in members:
            result.append(member.to_dict())

        return jsonify({'members': result, 'total': len(result)}), 200

    except Exception as e:
        return jsonify({'error': f'获取团队成员失败: {str(e)}'}), 500


@team_bp.route('/<int:id>/members/<int:member_id>', methods=['DELETE'])
@jwt_required()
def remove_member(id, member_id):
    """移除团队成员"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        team = Team.query.get(id)
        if not team:
            return jsonify({'error': '团队不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or team.creator_id != teacher.id:
                return jsonify({'error': '只有团队负责人可以移除成员'}), 403
        else:
            return jsonify({'error': '无权移除成员'}), 403

        member = TeamMember.query.filter_by(team_id=id, teacher_id=member_id).first()
        if not member:
            return jsonify({'error': '成员不存在'}), 404

        if member.role == 'leader':
            return jsonify({'error': '不能移除团队负责人'}), 403

        db.session.delete(member)
        db.session.commit()

        return jsonify({'message': '成员移除成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'移除成员失败: {str(e)}'}), 500


@team_bp.route('/join', methods=['POST'])
@jwt_required()
def join_team():
    """加入团队"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if current_user.role != 'teacher':
            return jsonify({'error': '只有教师可以加入团队'}), 403

        teacher = current_user.teacher
        if not teacher:
            return jsonify({'error': '教师信息不存在'}), 404

        data = request.get_json()
        invite_code = data.get('invite_code')

        if not invite_code:
            return jsonify({'error': '邀请码不能为空'}), 400

        team = Team.query.filter_by(invite_code=invite_code).first()
        if not team:
            return jsonify({'error': '邀请码无效'}), 404

        if TeamMember.query.filter_by(team_id=team.id, teacher_id=teacher.id).first():
            return jsonify({'error': '您已加入该团队'}), 400

        team_member = TeamMember(
            team_id=team.id,
            teacher_id=teacher.id,
            role='member'
        )
        db.session.add(team_member)
        db.session.commit()

        return jsonify({
            'message': '加入团队成功',
            'team': team.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'加入团队失败: {str(e)}'}), 500


@team_bp.route('/<int:id>/leave', methods=['POST'])
@jwt_required()
def leave_team(id):
    """退出团队"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        team = Team.query.get(id)
        if not team:
            return jsonify({'error': '团队不存在'}), 404

        if current_user.role != 'teacher':
            return jsonify({'error': '只有教师可以退出团队'}), 403

        teacher = current_user.teacher
        if not teacher:
            return jsonify({'error': '教师信息不存在'}), 404

        member = TeamMember.query.filter_by(team_id=id, teacher_id=teacher.id).first()
        if not member:
            return jsonify({'error': '您不是该团队成员'}), 400

        if member.role == 'leader':
            return jsonify({'error': '团队负责人不能退出，请先删除团队或转让负责人'}), 403

        db.session.delete(member)
        db.session.commit()

        return jsonify({'message': '退出团队成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'退出团队失败: {str(e)}'}), 500