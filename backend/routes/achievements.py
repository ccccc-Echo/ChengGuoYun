from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Achievement, AchievementAttachment, User, Student, Teacher, Course, CourseStudent, TeamMember
from extensions import db
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from utils.logger import log_action

achievement_bp = Blueprint('achievement', __name__, url_prefix='/api/achievements')


def get_auditor_team_name(teacher_id):
    """获取审核教师所属的科组团队名称（type=subject_group）"""
    if not teacher_id:
        return None
    memberships = TeamMember.query.filter_by(teacher_id=teacher_id).all()
    for m in memberships:
        if m.team and m.team.type == 'subject_group':
            return m.team.name
    return None


def build_auditor_display(achievement):
    """构造审核人显示文本：姓名（院系/科组）"""
    auditor = achievement.auditor
    if not auditor:
        return None
    name = auditor.user.name if auditor.user else ''
    parts = []
    if auditor.department:
        parts.append(auditor.department)
    team_name = get_auditor_team_name(auditor.id)
    if team_name:
        parts.append(team_name)
    if parts:
        return f"{name}（{'/'.join(parts)}）"
    return name or None


def get_accessible_student_ids(user):
    """获取用户可访问的学生ID列表（由教师所授课程派生）"""
    from models import Course, CourseStudent
    
    if user.role == 'admin':
        return [s.id for s in Student.query.all()]
    elif user.role == 'teacher' and user.teacher:
        teacher = user.teacher
        student_ids = set()
        
        courses = Course.query.filter(Course.teacher_id == teacher.id).all()
        for course in courses:
            course_students = CourseStudent.query.filter(CourseStudent.course_id == course.id).all()
            student_ids.update([cs.student_id for cs in course_students])
        
        return list(student_ids)
    elif user.role == 'student' and user.student:
        return [user.student.id]
    return []


@achievement_bp.route('/', methods=['GET'])
@jwt_required()
def get_achievements():
    """获取成果列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        title = request.args.get('title')
        main_category = request.args.get('main_category')
        sub_category = request.args.get('sub_category')
        level = request.args.get('level')
        status = request.args.get('status')
        course_id = request.args.get('course_id', type=int)
        student_id = request.args.get('student_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        include_auditor_team = request.args.get('include_auditor_team', 'false').lower() == 'true'

        query = Achievement.query

        if current_user.role == 'student':
            if not current_user.student:
                return jsonify({
                    'achievements': [],
                    'pagination': {
                        'total': 0,
                        'pages': 0,
                        'current_page': page,
                        'per_page': page_size
                    }
                }), 200
            query = query.filter_by(student_id=current_user.student.id)
        elif current_user.role == 'teacher':
            accessible_student_ids = get_accessible_student_ids(current_user)
            teacher = current_user.teacher
            if accessible_student_ids:
                query = query.filter(Achievement.student_id.in_(accessible_student_ids))
            else:
                return jsonify({
                    'achievements': [],
                    'pagination': {
                        'total': 0,
                        'pages': 0,
                        'current_page': page,
                        'per_page': page_size
                    }
                }), 200

        if title:
            query = query.filter(Achievement.title.like(f'%{title}%'))

        if main_category:
            query = query.filter(Achievement.main_category == main_category)

        if sub_category:
            query = query.filter(Achievement.sub_category == sub_category)

        if level:
            query = query.filter(Achievement.level == level)

        if status:
            query = query.filter(Achievement.status == status)

        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Achievement.achieved_date >= start_dt.date())
            except ValueError:
                pass

        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                query = query.filter(Achievement.achieved_date <= end_dt.date())
            except ValueError:
                pass

        if course_id:
            course_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id == course_id).all()]
            if course_student_ids:
                query = query.filter(Achievement.student_id.in_(course_student_ids))
            else:
                query = query.filter(Achievement.student_id == -1)

        if student_id:
            query = query.filter_by(student_id=student_id)

        query = query.order_by(Achievement.submitted_at.desc())
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        achievements = []
        for ach in pagination.items:
            ach_dict = ach.to_dict()
            ach_dict['student_name'] = ach.student.user.name if ach.student and ach.student.user else ''
            ach_dict['class_name'] = ach.student.class_name() if ach.student else ''
            if include_auditor_team:
                ach_dict['auditor_display'] = build_auditor_display(ach)
                ach_dict['auditor_department'] = ach.auditor.department if ach.auditor else None
                ach_dict['auditor_team'] = get_auditor_team_name(ach.auditor_id) if ach.auditor_id else None
            achievements.append(ach_dict)

        return jsonify({
            'achievements': achievements,
            'pagination': {
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': page_size,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/achievements/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取成果列表失败: {str(e)}'}), 500


@achievement_bp.route('/', methods=['POST'])
@jwt_required()
def create_achievement():
    """录入成果"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        data = request.get_json()

        if not data:
            return jsonify({'error': '请求体为空'}), 400

        if current_user.role == 'student':
            student = current_user.student
            if not student:
                return jsonify({'error': '学生信息不存在'}), 404
        elif current_user.role == 'teacher' or current_user.role == 'admin':
            student_id = data.get('student_id')
            if student_id:
                student = Student.query.get(student_id)
                if not student:
                    return jsonify({'error': '指定的学生不存在'}), 404
            else:
                return jsonify({'error': '管理员/辅导员创建成果需要指定 student_id'}), 400
        else:
            return jsonify({'error': '无权创建成果'}), 403

        required_fields = ['main_category', 'title', 'level']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        achievement = Achievement(
            student_id=student.id,
            main_category=data['main_category'],
            sub_category=data.get('sub_category'),
            title=data['title'],
            level=data['level'],
            achieved_date=data.get('achieved_date'),
            description=data.get('description'),
            keywords=data.get('keywords'),
            status='pending'
        )

        db.session.add(achievement)
        db.session.flush()

        # 关联已上传的附件
        attachment_ids = data.get('attachment_ids', [])
        if attachment_ids:
            for att_id in attachment_ids:
                attachment = AchievementAttachment.query.get(att_id)
                if attachment and attachment.achievement_id is None:
                    attachment.achievement_id = achievement.id

        db.session.commit()

        log_action('add_achievement', f'提交成果“{achievement.title}”，状态：待审核', user=current_user)

        return jsonify({
            'message': '成果录入成功',
            'achievement': achievement.to_dict(include_attachments=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/achievements/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'录入成果失败: {str(e)}'}), 500


@achievement_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_achievement(id):
    """获取成果详情"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        achievement = Achievement.query.get(id)
        if not achievement:
            return jsonify({'error': '成果不存在'}), 404

        if current_user.role == 'student':
            if achievement.student_id != current_user.student.id:
                return jsonify({'error': '无权查看此成果'}), 403
        elif current_user.role == 'teacher':
            accessible_student_ids = get_accessible_student_ids(current_user)
            teacher = current_user.teacher
            if teacher and teacher.role == 'faculty':
                pass
            elif not accessible_student_ids or achievement.student_id not in accessible_student_ids:
                return jsonify({'error': '无权查看此成果'}), 403

        ach_dict = achievement.to_dict(include_attachments=True)
        ach_dict['student_name'] = achievement.student.user.name if achievement.student and achievement.student.user else ''
        ach_dict['class_name'] = achievement.student.class_name() if achievement.student else ''

        return jsonify({
            'achievement': ach_dict
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取成果详情失败: {str(e)}'}), 500


@achievement_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_achievement(id):
    """修改成果信息"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        achievement = Achievement.query.get(id)
        if not achievement:
            return jsonify({'error': '成果不存在'}), 404

        if current_user.role == 'student':
            if achievement.student_id != current_user.student.id:
                return jsonify({'error': '无权修改此成果'}), 403
            if achievement.status != 'pending':
                return jsonify({'error': '只能修改待审核的成果'}), 403
        elif current_user.role == 'teacher':
            accessible_student_ids = get_accessible_student_ids(current_user)
            teacher = current_user.teacher
            if teacher and teacher.role == 'faculty':
                pass
            elif not accessible_student_ids or achievement.student_id not in accessible_student_ids:
                return jsonify({'error': '无权修改此成果'}), 403

        data = request.get_json()

        if 'title' in data:
            achievement.title = data['title']
        if 'main_category' in data:
            achievement.main_category = data['main_category']
        if 'sub_category' in data:
            achievement.sub_category = data['sub_category']
        if 'level' in data:
            achievement.level = data['level']
        if 'achieved_date' in data:
            achievement.achieved_date = data['achieved_date']
        if 'description' in data:
            achievement.description = data['description']
        if 'keywords' in data:
            achievement.keywords = data['keywords']

        db.session.commit()

        return jsonify({
            'message': '成果信息更新成功',
            'achievement': achievement.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新成果失败: {str(e)}'}), 500


@achievement_bp.route('/<int:id>/audit', methods=['PUT'])
@jwt_required()
def audit_achievement(id):
    """审核成果"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            if not current_user.teacher:
                return jsonify({'error': '教师信息不存在'}), 404
        else:
            return jsonify({'error': '无权审核成果'}), 403

        achievement = Achievement.query.get(id)
        if not achievement:
            return jsonify({'error': '成果不存在'}), 404

        if achievement.status != 'pending':
            return jsonify({'error': '只能审核待审核的成果'}), 400

        if current_user.role == 'teacher':
            accessible_student_ids = get_accessible_student_ids(current_user)
            teacher = current_user.teacher
            if teacher and teacher.role == 'faculty':
                pass
            elif not accessible_student_ids or achievement.student_id not in accessible_student_ids:
                return jsonify({'error': '无权审核此成果'}), 403

        data = request.get_json()
        if 'status' not in data or data['status'] not in ['approved', 'rejected']:
            return jsonify({'error': '无效的审核状态'}), 400

        achievement.status = data['status']
        achievement.review_comment = data.get('review_comment')
        achievement.reviewed_at = datetime.now()

        if current_user.role == 'admin':
            auditor_id = data.get('auditor_id')
            if auditor_id:
                auditor = Teacher.query.get(auditor_id)
                if not auditor:
                    return jsonify({'error': '指定的审核人不存在'}), 400
                achievement.auditor_id = auditor_id
            else:
                return jsonify({'error': '管理员审核必须指定审核人'}), 400
        elif current_user.role == 'teacher':
            achievement.auditor_id = current_user.teacher.id

        db.session.commit()

        if data['status'] == 'approved':
            from routes.knowledge_base import add_to_knowledge_base
            add_to_knowledge_base(achievement)

        # 站内信：通知学生审核结果
        try:
            from models import send_notification
            student_user_id = achievement.student.user_id if achievement.student and achievement.student.user else None
            if student_user_id:
                if data['status'] == 'approved':
                    send_notification(
                        student_user_id,
                        f'您的成果“{achievement.title}”已通过审核',
                        content=f'您提交的成果“{achievement.title}”已通过审核，可在个人成果中查看。',
                        type='achievement_approved'
                    )
                else:
                    reason = data.get('review_comment') or '未填写原因'
                    send_notification(
                        student_user_id,
                        f'您的成果“{achievement.title}”被驳回',
                        content=f'原因：{reason}。请修改后重新提交。',
                        type='achievement_rejected'
                    )
        except Exception:
            db.session.rollback()
            # 通知失败不影响审核主流程

        audit_result = '通过' if data['status'] == 'approved' else '驳回'
        log_action('audit_achievement', f'审核成果“{achievement.title}”，结果：{audit_result}', user=current_user)

        return jsonify({
            'message': '审核成功',
            'achievement': achievement.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'审核失败: {str(e)}'}), 500


@achievement_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_achievement(id):
    """删除成果"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        achievement = Achievement.query.get(id)
        if not achievement:
            return jsonify({'error': '成果不存在'}), 404

        if current_user.role == 'student':
            if achievement.student_id != current_user.student.id:
                return jsonify({'error': '无权删除此成果'}), 403
            if achievement.status != 'pending':
                return jsonify({'error': '只能删除待审核的成果'}), 403
        elif current_user.role == 'teacher':
            accessible_student_ids = get_accessible_student_ids(current_user)
            teacher = current_user.teacher
            if teacher and teacher.role == 'faculty':
                pass
            elif not accessible_student_ids or achievement.student_id not in accessible_student_ids:
                return jsonify({'error': '无权删除此成果'}), 403

        for attachment in achievement.attachments:
            file_path = attachment.file_path
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(achievement)
        db.session.commit()

        return jsonify({'message': '删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


@achievement_bp.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers_for_audit():
    """获取可作为审核人的教师列表（供管理员审核使用）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role not in ['admin', 'teacher']:
            return jsonify({'error': '无权访问'}), 403

        teachers = Teacher.query.filter_by(status='approved').all()

        teacher_list = []
        for teacher in teachers:
            teacher_list.append({
                'id': teacher.id,
                'name': teacher.user.name if teacher.user else '',
                'teacher_no': teacher.teacher_no,
                'department': teacher.department,
                'title': teacher.title
            })

        return jsonify({
            'teachers': teacher_list
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/achievements/teachers 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取教师列表失败: {str(e)}'}), 500


@achievement_bp.route('/reviewers', methods=['GET'])
@jwt_required()
def get_reviewers():
    """获取当前学生的可选审核教师列表"""
    try:
        from models import Course, CourseStudent

        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'student':
            return jsonify({'error': '仅学生可获取审核教师列表'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        reviewer_ids = set()

        course_students = CourseStudent.query.filter_by(student_id=student.id).all()
        for cs in course_students:
            course = cs.course
            if course and course.teacher:
                reviewer_ids.add(course.teacher.id)

        teachers = Teacher.query.filter(Teacher.id.in_(list(reviewer_ids))).all()

        reviewers = []
        for teacher in teachers:
            reviewers.append({
                'id': teacher.id,
                'user_id': teacher.user_id,
                'name': teacher.user.name if teacher.user else '',
                'title': teacher.title,
                'department': teacher.department,
                'teacher_no': teacher.teacher_no
            })

        return jsonify({
            'reviewers': reviewers
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/achievements/reviewers 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取审核教师列表失败: {str(e)}'}), 500


@achievement_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """上传成果附件"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400

        # 检查文件扩展名
        allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
        ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        if ext not in allowed_extensions:
            return jsonify({'error': f'不支持的文件类型: .{ext}'}), 400

        # 生成唯一文件名
        safe_name = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"

        # 保存文件
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_name)
        file.save(file_path)

        # 创建附件记录
        file_size = os.path.getsize(file_path)
        attachment = AchievementAttachment(
            achievement_id=None,  # 稍后关联
            file_name=file.filename,
            file_path=f'/uploads/{unique_name}',
            file_size=file_size,
            file_type=file.content_type
        )
        db.session.add(attachment)
        db.session.commit()

        return jsonify({
            'message': '上传成功',
            'attachment': attachment.to_dict()
        }), 201

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/achievements/upload 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500