from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Achievement, Student, User, Teacher, Course, CourseStudent, SystemLog
from extensions import db
from sqlalchemy import func, extract, case
from datetime import datetime, timedelta
import traceback

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


def get_accessible_student_ids(user):
    """获取用户可访问的学生ID列表（由教师所授课程派生）"""
    try:
        student_ids = set()
        if user.role == 'admin':
            return [s.id for s in Student.query.all()]
        elif user.role == 'teacher' and user.teacher:
            teacher = user.teacher
            courses = Course.query.filter(Course.teacher_id == teacher.id).all()
            for course in courses:
                course_students = CourseStudent.query.filter(CourseStudent.course_id == course.id).all()
                student_ids.update([cs.student_id for cs in course_students])
            return list(student_ids)
        return []
    except Exception as e:
        print(f"\n=== get_accessible_student_ids 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return []


def build_trend_data(query_result):
    """构建趋势数据数组"""
    data = []
    for row in query_result:
        try:
            year = int(row.year)
            month = int(row.month)
            data.append({
                'month': f'{year}-{month:02d}',
                'count': row.count
            })
        except Exception as e:
            print(f"\n=== build_trend_data 处理行错误 ===")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
            print(f"行数据: {row}")
    return data


@stats_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """获取仪表盘统计数据"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            query = Achievement.query
            class_query = Course.query
            student_query = Student.query

            total_achievements = query.count()
            pending_achievements = query.filter(Achievement.status == 'pending').count()
            approved_achievements = query.filter(Achievement.status == 'approved').count()
            total_classes = class_query.count()
            total_students = student_query.count()

            category_distribution = db.session.query(
                Achievement.main_category,
                func.count(Achievement.id).label('count')
            ).group_by(Achievement.main_category).all()

            start_date = datetime.now() - timedelta(days=180)
            trend_data = db.session.query(
                extract('year', Achievement.submitted_at).label('year'),
                extract('month', Achievement.submitted_at).label('month'),
                func.count(Achievement.id).label('count')
            ).filter(Achievement.submitted_at >= start_date).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).all()

            level_distribution = db.session.query(
                Achievement.level,
                func.count(Achievement.id).label('count')
            ).group_by(Achievement.level).all()

            pending_list = query.filter(Achievement.status == 'pending').order_by(
                Achievement.submitted_at.desc()
            ).limit(10).all()

            recent_list = query.order_by(Achievement.submitted_at.desc()).limit(10).all()

            category_data = []
            for row in category_distribution:
                if row.main_category:
                    category_data.append({'name': row.main_category, 'count': row.count})

            level_data = []
            for row in level_distribution:
                if row.level:
                    level_data.append({'level': row.level, 'count': row.count})

            return jsonify({
                'total_achievements': total_achievements,
                'pending_achievements': pending_achievements,
                'approved_achievements': approved_achievements,
                'total_classes': total_classes,
                'total_students': total_students,
                'category_distribution': category_data,
                'level_distribution': level_data,
                'trend_data': build_trend_data(trend_data),
                'pending_list': [
                    {
                        'id': row.id,
                        'title': row.title,
                        'category': row.main_category,
                        'student_name': row.student.user.name if row.student and row.student.user else '',
                        'class_name': row.student.class_name() if row.student else '',
                        'status': row.status,
                        'created_at': row.submitted_at.strftime('%Y-%m-%d') if row.submitted_at else ''
                    } for row in pending_list
                ],
                'recent_list': [
                    {
                        'id': row.id,
                        'title': row.title,
                        'category': row.main_category,
                        'student_name': row.student.user.name if row.student and row.student.user else '',
                        'status': row.status,
                        'created_at': row.submitted_at.strftime('%Y-%m-%d') if row.submitted_at else ''
                    } for row in recent_list
                ],
                'ranking_list': []
            }), 200

        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({
                    'total_achievements': 0,
                    'pending_achievements': 0,
                    'approved_achievements': 0,
                    'total_classes': 0,
                    'total_students': 0,
                    'category_distribution': [],
                    'level_distribution': [],
                    'trend_data': [],
                    'pending_list': [],
                    'recent_list': [],
                    'ranking_list': []
                }), 200

            student_ids = get_accessible_student_ids(current_user)

            role_map = {
                'advisor': 'advisor', '辅导员': 'advisor',
                'head': 'head', '院系负责人': 'head',
                'faculty': 'faculty', '教师': 'faculty',
                'teaching_admin': 'teaching_admin', '教务管理员': 'teaching_admin'
            }
            teacher_role = getattr(teacher, 'role', None)
            normalized_role = role_map.get(teacher_role, teacher_role) if teacher_role else teacher_role

            has_student_filter = bool(student_ids)
            has_teacher_filter = teacher.id is not None

            achievement_filters = []
            if has_student_filter:
                achievement_filters.append(Achievement.student_id.in_(student_ids))
            if has_teacher_filter:
                achievement_filters.append(Achievement.teacher_id == teacher.id)

            if achievement_filters:
                combined_filter = db.or_(*achievement_filters) if len(achievement_filters) > 1 else achievement_filters[0]
                query = Achievement.query.filter(combined_filter)

                total_achievements = query.count()
                pending_achievements = query.filter(Achievement.status == 'pending').count()
                approved_achievements = query.filter(Achievement.status == 'approved').count()

                category_distribution = db.session.query(
                    Achievement.main_category,
                    func.count(Achievement.id).label('count')
                ).filter(combined_filter).group_by(Achievement.main_category).all()

                level_distribution = db.session.query(
                    Achievement.level,
                    func.count(Achievement.id).label('count')
                ).filter(combined_filter).group_by(Achievement.level).all()

                start_date = datetime.now() - timedelta(days=180)
                trend_data = db.session.query(
                    extract('year', Achievement.submitted_at).label('year'),
                    extract('month', Achievement.submitted_at).label('month'),
                    func.count(Achievement.id).label('count')
                ).filter(
                    combined_filter,
                    Achievement.submitted_at >= start_date
                ).group_by(
                    extract('year', Achievement.submitted_at),
                    extract('month', Achievement.submitted_at)
                ).order_by(
                    extract('year', Achievement.submitted_at),
                    extract('month', Achievement.submitted_at)
                ).all()

                pending_list = query.filter(Achievement.status == 'pending').order_by(
                    Achievement.submitted_at.desc()
                ).limit(10).all()

                recent_list = query.order_by(Achievement.submitted_at.desc()).limit(10).all()

                ranking_list = db.session.query(
                    User.name,
                    Course.name.label('class_name'),
                    func.count(Achievement.id).label('count')
                ).join(Student, Student.user_id == User.id).join(
                    CourseStudent, CourseStudent.student_id == Student.id
                ).join(Course, Course.id == CourseStudent.course_id).outerjoin(
                    Achievement, Achievement.student_id == Student.id
                ).filter(combined_filter).group_by(User.name, Course.name).order_by(
                    func.count(Achievement.id).desc()
                ).limit(10).all()

                total_classes = Course.query.count()
                total_students = len(student_ids) if has_student_filter else 0
            else:
                total_achievements = 0
                pending_achievements = 0
                approved_achievements = 0
                total_classes = 0
                total_students = 0
                category_distribution = []
                level_distribution = []
                trend_data = []
                pending_list = []
                recent_list = []
                ranking_list = []

            category_data = []
            for row in category_distribution:
                if row.main_category:
                    category_data.append({'name': row.main_category, 'count': row.count})

            level_data = []
            for row in level_distribution:
                if row.level:
                    level_data.append({'level': row.level, 'count': row.count})

            pending_data = []
            for row in pending_list:
                student = row.student
                pending_data.append({
                    'id': row.id,
                    'title': row.title,
                    'category': row.main_category,
                    'student_name': student.user.name if student and student.user else '',
                    'class_name': student.class_name() if student else '',
                    'status': row.status,
                    'created_at': row.submitted_at.strftime('%Y-%m-%d') if row.submitted_at else ''
                })

            recent_data = []
            for row in recent_list:
                student = row.student
                recent_data.append({
                    'id': row.id,
                    'title': row.title,
                    'category': row.main_category,
                    'student_name': student.user.name if student and student.user else '',
                    'status': row.status,
                    'created_at': row.submitted_at.strftime('%Y-%m-%d') if row.submitted_at else ''
                })

            ranking_data = []
            for row in ranking_list:
                ranking_data.append({
                    'name': row.name,
                    'class': row.class_name,
                    'count': row.count
                })

            show_trend = normalized_role in ['admin', 'head', 'advisor', 'teaching_admin']

            return jsonify({
                'total_achievements': total_achievements,
                'pending_achievements': pending_achievements,
                'approved_achievements': approved_achievements,
                'total_classes': total_classes,
                'total_students': total_students,
                'category_distribution': category_data,
                'level_distribution': level_data,
                'trend_data': build_trend_data(trend_data) if show_trend else [],
                'pending_list': pending_data,
                'recent_list': recent_data,
                'ranking_list': ranking_data
            }), 200

        elif current_user.role == 'student':
            student = current_user.student
            if not student:
                return jsonify({
                    'total_achievements': 0,
                    'pending_achievements': 0,
                    'approved_achievements': 0,
                    'rejected_achievements': 0,
                    'total_students': 0,
                    'total_classes': 0,
                    'award_count': 0,
                    'category_distribution': [],
                    'level_distribution': [],
                    'trend_data': [],
                    'recent_list': [],
                    'pending_list': [],
                    'ranking_list': []
                }), 200

            student_id = student.id
            query = Achievement.query.filter(Achievement.student_id == student_id)

            total_achievements = query.count()
            pending_achievements = query.filter(Achievement.status == 'pending').count()
            approved_achievements = query.filter(Achievement.status == 'approved').count()
            rejected_achievements = query.filter(Achievement.status == 'rejected').count()

            award_count = query.filter(
                Achievement.status == 'approved',
                Achievement.level.in_(['Guo Jia Ji', 'Sheng Ji'])
            ).count()

            category_distribution = db.session.query(
                Achievement.main_category,
                func.count(Achievement.id).label('count')
            ).filter(Achievement.student_id == student_id).group_by(Achievement.main_category).all()

            level_distribution = db.session.query(
                Achievement.level,
                func.count(Achievement.id).label('count')
            ).filter(Achievement.student_id == student_id).group_by(Achievement.level).all()

            personal_list = query.order_by(Achievement.submitted_at.desc()).limit(10).all()

            trend_start_date = datetime.now() - timedelta(days=180)
            trend_data = db.session.query(
                extract('year', Achievement.submitted_at).label('year'),
                extract('month', Achievement.submitted_at).label('month'),
                func.count(Achievement.id).label('count')
            ).filter(
                Achievement.student_id == student_id,
                Achievement.submitted_at >= trend_start_date
            ).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).all()

            category_data = []
            for row in category_distribution:
                if row.main_category:
                    category_data.append({'name': row.main_category, 'count': int(row.count)})

            level_data = []
            for row in level_distribution:
                if row.level:
                    level_data.append({'level': row.level, 'count': int(row.count)})

            recent_data = []
            for row in personal_list:
                recent_data.append({
                    'id': row.id,
                    'title': row.title,
                    'category': row.main_category,
                    'status': row.status,
                    'created_at': row.submitted_at.strftime('%Y-%m-%d') if row.submitted_at else ''
                })

            total_classes = len(student.course_students) if student.course_students else 0

            return jsonify({
                'total_achievements': int(total_achievements),
                'pending_achievements': int(pending_achievements),
                'approved_achievements': int(approved_achievements),
                'rejected_achievements': int(rejected_achievements),
                'total_students': 1,
                'total_classes': total_classes,
                'award_count': int(award_count),
                'category_distribution': category_data,
                'level_distribution': level_data,
                'trend_data': build_trend_data(trend_data),
                'pending_list': [],
                'recent_list': recent_data,
                'ranking_list': []
            }), 200

        else:
            return jsonify({'error': '无权查看统计'}), 403

    except Exception as e:
        print(f"\n=== GET /api/stats/dashboard/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈:\n{traceback.format_exc()}")
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500


@stats_bp.route('/screen', methods=['GET'])
@jwt_required()
def get_screen_stats():
    """管理员数据大屏聚合统计接口"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'admin':
            return jsonify({'error': '无权查看'}), 403

        # 1. 基础数据
        total_achievements = Achievement.query.count()
        total_students = Student.query.count()
        total_teachers = Teacher.query.count()
        total_courses = Course.query.count()

        # 2. 成果分类分布
        category_rows = db.session.query(
            Achievement.main_category,
            func.count(Achievement.id).label('count')
        ).group_by(Achievement.main_category).all()

        # 3. 成果级别分布
        level_rows = db.session.query(
            Achievement.level,
            func.count(Achievement.id).label('count')
        ).group_by(Achievement.level).all()

        # 4. 成果趋势（按月，近12个月补齐空缺月份）
        trend_rows = db.session.query(
            extract('year', Achievement.submitted_at).label('year'),
            extract('month', Achievement.submitted_at).label('month'),
            func.count(Achievement.id).label('count')
        ).filter(Achievement.submitted_at >= (datetime.now() - timedelta(days=365))).group_by(
            extract('year', Achievement.submitted_at),
            extract('month', Achievement.submitted_at)
        ).order_by(
            extract('year', Achievement.submitted_at),
            extract('month', Achievement.submitted_at)
        ).all()

        trend_map = {}
        for row in trend_rows:
            try:
                key = f'{int(row.year)}-{int(row.month):02d}'
                trend_map[key] = int(row.count)
            except Exception:
                continue

        trend_data = []
        now = datetime.now()
        for i in range(11, -1, -1):
            d = datetime(now.year, now.month, 1) - timedelta(days=i * 30)
            key = f'{d.year}-{d.month:02d}'
            trend_data.append({'month': key, 'count': trend_map.get(key, 0)})

        # 5. 各院系成果对比（按学生 department 聚合）
        dept_rows = db.session.query(
            Student.department,
            func.count(Achievement.id).label('count')
        ).join(Achievement, Achievement.student_id == Student.id).group_by(
            Student.department
        ).order_by(func.count(Achievement.id).desc()).all()
        department_data = []
        for row in dept_rows:
            if row.department:
                department_data.append({'department': row.department, 'count': int(row.count)})

        # 6. 审核通过率
        approved = Achievement.query.filter(Achievement.status == 'approved').count()
        total_reviewed = Achievement.query.filter(Achievement.status.in_(['approved', 'rejected'])).count()
        approval_rate = round((approved / total_reviewed * 100), 1) if total_reviewed else 0

        # 7. 实时动态（最新操作日志）
        recent_logs = SystemLog.query.order_by(SystemLog.created_at.desc()).limit(10).all()
        recent_data = [
            {
                'id': log.id,
                'username': log.username or '',
                'role': log.role or '',
                'action_type': log.action_type or '',
                'action_detail': log.action_detail or '',
                'result': log.result or '',
                'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S') if log.created_at else ''
            } for log in recent_logs
        ]

        return jsonify({
            'overview': {
                'total_achievements': total_achievements,
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_courses': total_courses
            },
            'category': [
                {'name': r.main_category, 'count': int(r.count)} for r in category_rows if r.main_category
            ],
            'level': [
                {'level': r.level, 'count': int(r.count)} for r in level_rows if r.level
            ],
            'trend': trend_data,
            'department': department_data,
            'approval_rate': approval_rate,
            'recent': recent_data
        }), 200

    except Exception as e:
        print(f"\n=== GET /api/stats/screen/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈:\n{traceback.format_exc()}")
        return jsonify({'error': f'获取大屏统计失败: {str(e)}'}), 500


@stats_bp.route('/class', methods=['GET'])
@jwt_required()
def get_class_stats():
    """获取班级成果统计"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'student':
            if not current_user.student:
                return jsonify({'error': '学生信息不存在'}), 404

            student = current_user.student

            achievement_stats = db.session.query(
                func.count(Achievement.id).label('total'),
                func.sum(case((Achievement.status == 'approved', 1), else_=0)).label('approved'),
                func.sum(case((Achievement.status == 'pending', 1), else_=0)).label('pending'),
                func.sum(case((Achievement.status == 'rejected', 1), else_=0)).label('rejected')
            ).filter(Achievement.student_id == student.id).first()

            type_stats = db.session.query(
                Achievement.main_category,
                func.count(Achievement.id).label('count')
            ).filter(Achievement.student_id == student.id).group_by(Achievement.main_category).all()

            type_data = {}
            for row in type_stats:
                if row.main_category:
                    type_data[row.main_category] = row.count

            start_date = datetime.now() - timedelta(days=180)
            trend_stats = db.session.query(
                extract('year', Achievement.submitted_at).label('year'),
                extract('month', Achievement.submitted_at).label('month'),
                func.count(Achievement.id).label('submitted_count')
            ).filter(
                Achievement.student_id == student.id,
                Achievement.submitted_at >= start_date
            ).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).all()

            total = int(achievement_stats.total) if achievement_stats and achievement_stats.total else 0
            approved = int(achievement_stats.approved) if achievement_stats and achievement_stats.approved else 0
            pending = int(achievement_stats.pending) if achievement_stats and achievement_stats.pending else 0
            rejected = int(achievement_stats.rejected) if achievement_stats and achievement_stats.rejected else 0

            result_data = {
                'total_achievements': total,
                'approved_achievements': approved,
                'pending_achievements': pending,
                'rejected_achievements': rejected,
                'by_type': type_data,
                'trend': trend_data,
                'type_distribution': type_data,
                'class_ranking': []
            }
            print("\n=== 学生角色 - 准备返回的数据 ===")
            for key, value in result_data.items():
                print(f"  {key}: {type(value).__name__} = {value}")

            return jsonify(result_data), 200

        if current_user.role == 'teacher':
            if not current_user.teacher:
                return jsonify({
                    'total_achievements': 0,
                    'approved_achievements': 0,
                    'pending_achievements': 0,
                    'rejected_achievements': 0,
                    'total_students': 0,
                    'by_type': {},
                    'trend': [],
                    'type_distribution': {},
                    'class_ranking': [],
                    'student_ranking': []
                }), 200

            teacher = current_user.teacher
            student_ids = get_accessible_student_ids(current_user)

            if not student_ids:
                return jsonify({
                    'total_achievements': 0,
                    'approved_achievements': 0,
                    'pending_achievements': 0,
                    'rejected_achievements': 0,
                    'total_students': 0,
                    'by_type': {},
                    'trend': [],
                    'type_distribution': {},
                    'class_ranking': [],
                    'student_ranking': []
                }), 200

            achievement_stats = db.session.query(
                func.count(Achievement.id).label('total'),
                func.sum(case((Achievement.status == 'approved', 1), else_=0)).label('approved'),
                func.sum(case((Achievement.status == 'pending', 1), else_=0)).label('pending'),
                func.sum(case((Achievement.status == 'rejected', 1), else_=0)).label('rejected')
            ).join(Student, Student.id == Achievement.student_id).filter(Student.id.in_(student_ids)).first()

            student_ranking = db.session.query(
                Student.id,
                User.name,
                func.count(Achievement.id).label('total')
            ).join(User, User.id == Student.user_id).outerjoin(Achievement, Achievement.student_id == Student.id).filter(
                Student.id.in_(student_ids)
            ).group_by(Student.id, User.name).order_by(func.count(Achievement.id).desc()).limit(5).all()

            type_stats = db.session.query(
                Achievement.main_category,
                func.count(Achievement.id).label('count')
            ).join(Student, Student.id == Achievement.student_id).filter(Student.id.in_(student_ids)).group_by(
                Achievement.main_category
            ).all()

            type_data = {}
            for row in type_stats:
                if row.main_category:
                    type_data[row.main_category] = row.count

            start_date = datetime.now() - timedelta(days=180)
            trend_stats = db.session.query(
                extract('year', Achievement.submitted_at).label('year'),
                extract('month', Achievement.submitted_at).label('month'),
                func.count(Achievement.id).label('submitted_count')
            ).join(Student, Student.id == Achievement.student_id).filter(
                Student.id.in_(student_ids),
                Achievement.submitted_at >= start_date
            ).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at)
            ).all()

            total_students = len(student_ids)

            total = int(achievement_stats.total) if achievement_stats and achievement_stats.total else 0
            approved = int(achievement_stats.approved) if achievement_stats and achievement_stats.approved else 0
            pending = int(achievement_stats.pending) if achievement_stats and achievement_stats.pending else 0
            rejected = int(achievement_stats.rejected) if achievement_stats and achievement_stats.rejected else 0

            ranking_data = []
            for row in student_ranking:
                ranking_data.append({
                    'student_id': row.id,
                    'name': row.name,
                    'total': int(row.total) if row.total else 0
                })

            trend_data = []
            for row in trend_stats:
                try:
                    year = int(row.year)
                    month = int(row.month)
                    count_val = int(row.submitted_count) if row.submitted_count else 0
                    trend_data.append({
                        'month': f'{year}-{month:02d}',
                        'count': count_val
                    })
                except Exception as e:
                    print(f"\n=== trend_stats 行处理错误 ===")
                    print(f"错误类型: {type(e).__name__}")
                    print(f"错误信息: {str(e)}")
                    print(f"行数据: {row}")

            result_data = {
                'total_achievements': total,
                'approved_achievements': approved,
                'pending_achievements': pending,
                'rejected_achievements': rejected,
                'total_students': total_students,
                'by_type': type_data,
                'trend': trend_data,
                'type_distribution': type_data,
                'class_ranking': [],
                'student_ranking': ranking_data
            }
            print("\n=== 教师角色 - 准备返回的数据 ===")
            for key, value in result_data.items():
                print(f"  {key}: {type(value).__name__} = {value}")

            return jsonify(result_data), 200

        return jsonify({'error': '无权查看统计'}), 403

    except Exception as e:
        print(f"\n=== GET /api/stats/class/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈:\n{traceback.format_exc()}")
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500


@stats_bp.route('/school', methods=['GET'])
@jwt_required()
def get_school_stats():
    """获取全院统计"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ['head', 'teaching_admin']:
                return jsonify({'error': '无权查看全院统计'}), 403
        else:
            return jsonify({'error': '无权查看全院统计'}), 403

        total_students = Student.query.count()
        total_classes = Course.query.count()
        total_teachers = Teacher.query.count()

        achievement_stats = db.session.query(
            func.count(Achievement.id).label('total'),
            func.sum(case((Achievement.status == 'approved', 1), else_=0)).label('approved'),
            func.sum(case((Achievement.status == 'pending', 1), else_=0)).label('pending'),
            func.sum(case((Achievement.status == 'rejected', 1), else_=0)).label('rejected')
        ).first()

        type_stats = db.session.query(
            Achievement.main_category,
            func.count(Achievement.id).label('count')
        ).group_by(Achievement.main_category).all()

        level_stats = db.session.query(
            Achievement.level,
            func.count(Achievement.id).label('count')
        ).group_by(Achievement.level).all()

        status_stats = db.session.query(
            Achievement.status,
            func.count(Achievement.id).label('count')
        ).group_by(Achievement.status).all()

        class_ranking = db.session.query(
            Course.id,
            Course.name.label('class_name'),
            func.count(Achievement.id).label('achievement_count')
        ).outerjoin(CourseStudent, CourseStudent.course_id == Course.id).outerjoin(
            Achievement, Achievement.student_id == CourseStudent.student_id
        ).group_by(Course.id, Course.name).order_by(
            func.count(Achievement.id).desc()
        ).limit(10).all()

        type_data = {}
        for row in type_stats:
            if row.main_category:
                type_data[row.main_category] = row.count

        level_data = {}
        for row in level_stats:
            if row.level:
                level_data[row.level] = row.count

        status_data = {}
        for row in status_stats:
            if row.status:
                status_data[row.status] = row.count

        start_date = datetime.now() - timedelta(days=180)
        trend_stats = db.session.query(
            extract('year', Achievement.submitted_at).label('year'),
            extract('month', Achievement.submitted_at).label('month'),
            func.count(Achievement.id).label('submitted_count'),
            func.sum(case((Achievement.status == 'approved', 1), else_=0)).label('approved_count')
        ).filter(Achievement.submitted_at >= start_date).group_by(
            extract('year', Achievement.submitted_at),
            extract('month', Achievement.submitted_at)
        ).order_by(
            extract('year', Achievement.submitted_at),
            extract('month', Achievement.submitted_at)
        ).all()

        total = int(achievement_stats.total) if achievement_stats and achievement_stats.total else 0
        approved = int(achievement_stats.approved) if achievement_stats and achievement_stats.approved else 0
        pending = int(achievement_stats.pending) if achievement_stats and achievement_stats.pending else 0
        rejected = int(achievement_stats.rejected) if achievement_stats and achievement_stats.rejected else 0

        ranking_data = []
        for row in class_ranking:
            ranking_data.append({
                'class_id': row.id,
                'class_name': row.class_name,
                'achievement_count': int(row.achievement_count) if row.achievement_count else 0
            })

        trend_data = []
        for row in trend_stats:
            try:
                year = int(row.year)
                month = int(row.month)
                submitted_count = int(row.submitted_count) if row.submitted_count else 0
                approved_count = int(row.approved_count) if row.approved_count else 0
                trend_data.append({
                    'date': f'{year}-{month:02d}',
                    'submitted_count': submitted_count,
                    'approved_count': approved_count
                })
            except Exception as e:
                print(f"\n=== school trend_stats 行处理错误 ===")
                print(f"错误类型: {type(e).__name__}")
                print(f"错误信息: {str(e)}")
                print(f"行数据: {row}")

        return jsonify({
            'total_students': total_students,
            'total_classes': total_classes,
            'total_teachers': total_teachers,
            'total_achievements': total,
            'approved_achievements': approved,
            'pending_achievements': pending,
            'rejected_achievements': rejected,
            'by_type': type_data,
            'trend': trend_data,
            'type_distribution': type_data,
            'level_distribution': level_data,
            'status_distribution': status_data,
            'class_ranking': ranking_data
        }), 200

    except Exception as e:
        print(f"\n=== GET /api/stats/school/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈:\n{traceback.format_exc()}")
        return jsonify({'error': f'获取全院统计失败: {str(e)}'}), 500


@stats_bp.route('/trend', methods=['GET'])
@jwt_required()
def get_trend_stats():
    """获取趋势分析"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        period = request.args.get('period', '7d')

        days_map = {'7d': 7, '30d': 30, '90d': 90}
        days = days_map.get(period, 30)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        query = db.session.query(
            extract('year', Achievement.submitted_at).label('year'),
            extract('month', Achievement.submitted_at).label('month'),
            extract('day', Achievement.submitted_at).label('day'),
            func.count(Achievement.id).label('submitted_count')
        )

        if current_user.role == 'teacher':
            if not current_user.teacher:
                return jsonify({'error': '教师信息不存在'}), 404
            student_ids = get_accessible_student_ids(current_user)
            if student_ids:
                query = query.join(Student, Student.id == Achievement.student_id).filter(Student.id.in_(student_ids))
            else:
                return jsonify({
                    'trend_data': [],
                    'class_ranking': []
                }), 200
        elif current_user.role != 'admin':
            return jsonify({'error': '无权查看趋势分析'}), 403

        if days <= 30:
            query = query.filter(Achievement.submitted_at >= start_date).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at),
                extract('day', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at),
                extract('day', Achievement.submitted_at)
            )

            trend_stats = query.all()

            trend_data = []
            for row in trend_stats:
                try:
                    year = int(row.year)
                    month = int(row.month)
                    day = int(row.day)
                    trend_data.append({
                        'date': f'{year}-{month:02d}-{day:02d}',
                        'submitted_count': row.submitted_count
                    })
                except Exception as e:
                    print(f"\n=== trend_stats 行处理错误 ===")
                    print(f"错误类型: {type(e).__name__}")
                    print(f"错误信息: {str(e)}")
                    print(f"行数据: {row}")
        else:
            query = query.filter(Achievement.submitted_at >= start_date).group_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at),
                extract('day', Achievement.submitted_at)
            ).order_by(
                extract('year', Achievement.submitted_at),
                extract('month', Achievement.submitted_at),
                extract('day', Achievement.submitted_at)
            )

            trend_stats = query.all()

            trend_data = []
            for row in trend_stats:
                try:
                    year = int(row.year)
                    month = int(row.month)
                    day = int(row.day)
                    trend_data.append({
                        'date': f'{year}-{month:02d}-{day:02d}',
                        'submitted_count': row.submitted_count
                    })
                except Exception as e:
                    print(f"\n=== trend_stats 行处理错误 ===")
                    print(f"错误类型: {type(e).__name__}")
                    print(f"错误信息: {str(e)}")
                    print(f"行数据: {row}")

        return jsonify({
            'trend_data': trend_data
        }), 200

    except Exception as e:
        print(f"\n=== GET /api/stats/trend/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈:\n{traceback.format_exc()}")
        return jsonify({'error': f'获取趋势分析失败: {str(e)}'}), 500
