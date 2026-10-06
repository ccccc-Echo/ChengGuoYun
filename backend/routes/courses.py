from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Course, CourseStudent, Student, Teacher, User
from extensions import db
import random
import string
import datetime
from utils.logger import log_action

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')


def generate_invite_code():
    """生成6位邀请码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def generate_course_code():
    """生成课程代码"""
    timestamp = datetime.datetime.now().strftime('%y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'COURSE{timestamp}{random_str}'


@course_bp.route('/available', methods=['GET'])
@jwt_required()
def get_available_courses():
    """获取可选课程列表（含微课程）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'student':
            return jsonify({'error': '仅学生可查看课程列表'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        joined_course_ids = [cs.course_id for cs in student.course_students]

        type_filter = request.args.get('type')

        query = Course.query

        if type_filter:
            query = query.filter_by(type=type_filter)

        query = query.filter(Course.id.notin_(joined_course_ids))

        courses = query.order_by(Course.type, Course.created_at.desc()).all()

        return jsonify({
            'courses': [course.to_dict() for course in courses]
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/available 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取课程列表失败: {str(e)}'}), 500


@course_bp.route('/join', methods=['POST'])
@jwt_required()
def join_course():
    """加入课程"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'student':
            return jsonify({'error': '仅学生可加入课程'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        course_id = data.get('course_id')
        invite_code = data.get('invite_code')

        if not course_id and not invite_code:
            return jsonify({'error': '请提供课程ID或邀请码'}), 400

        if invite_code:
            course = Course.query.filter_by(invite_code=invite_code).first()
            if not course:
                return jsonify({'error': '邀请码无效'}), 404
        else:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': '课程不存在'}), 404

        existing = CourseStudent.query.filter_by(course_id=course.id, student_id=student.id).first()
        if existing:
            return jsonify({'error': '已加入该课程'}), 400

        if course.student_count >= course.max_students:
            return jsonify({'error': '课程人数已满'}), 400

        course_student = CourseStudent(
            course_id=course.id,
            student_id=student.id
        )

        course.student_count += 1

        db.session.add(course_student)
        db.session.commit()

        return jsonify({
            'message': '加入课程成功',
            'course': course.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/courses/join 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'加入课程失败: {str(e)}'}), 500


@course_bp.route('/leave', methods=['DELETE'])
@jwt_required()
def leave_course():
    """退课"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'student':
            return jsonify({'error': '仅学生可退课'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        data = request.get_json()
        if not data or 'course_id' not in data:
            return jsonify({'error': '请提供课程ID'}), 400

        course_id = data['course_id']

        course_student = CourseStudent.query.filter_by(
            course_id=course_id,
            student_id=student.id
        ).first()

        if not course_student:
            return jsonify({'error': '未加入该课程'}), 404

        course = Course.query.get(course_id)
        if course and course.student_count > 0:
            course.student_count -= 1

        db.session.delete(course_student)
        db.session.commit()

        return jsonify({'message': '退课成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/courses/leave 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'退课失败: {str(e)}'}), 500


@course_bp.route('/star', methods=['POST'])
@jwt_required()
def star_course():
    """置顶课程"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'student':
            return jsonify({'error': '仅学生可置顶课程'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        data = request.get_json()
        if not data or 'course_id' not in data:
            return jsonify({'error': '请提供课程ID'}), 400

        course_id = data['course_id']

        course_student = CourseStudent.query.filter_by(
            course_id=course_id,
            student_id=student.id
        ).first()

        if not course_student:
            return jsonify({'error': '未加入该课程'}), 404

        course_student.is_starred = not course_student.is_starred

        db.session.commit()

        return jsonify({
            'message': '置顶成功' if course_student.is_starred else '取消置顶成功',
            'is_starred': course_student.is_starred
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/courses/star 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'置顶课程失败: {str(e)}'}), 500


@course_bp.route('/', methods=['GET'])
@jwt_required()
def admin_list_courses():
    """课程列表（管理员查看全部，教师查看自己创建；分页/名称筛选）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role not in ['admin', 'teacher']:
            return jsonify({'error': '无权限查看课程列表'}), 403

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        name = request.args.get('name')
        course_id = request.args.get('course_id', type=int)

        query = Course.query

        if current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({'error': '教师信息不存在'}), 404
            query = query.filter(Course.teacher_id == teacher.id)

        if name:
            query = query.filter(Course.name.like(f'%{name}%'))

        courses = query.order_by(Course.created_at.desc()).all()

        # 按 course_id 过滤（供筛选用）
        if course_id:
            courses = [c for c in courses if c.id == course_id]

        total = len(courses)
        start = (page - 1) * page_size
        page_courses = courses[start:start + page_size]

        result = []
        for course in page_courses:
            dict_course = course.to_dict()
            result.append(dict_course)

        return jsonify({
            'courses': result,
            'pagination': {
                'total': total,
                'pages': (total + page_size - 1) // page_size,
                'current_page': page,
                'per_page': page_size
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取课程列表失败: {str(e)}'}), 500


@course_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    """创建课程（教师端）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'teacher':
            return jsonify({'error': '仅教师可创建课程'}), 403

        teacher = current_user.teacher
        if not teacher:
            return jsonify({'error': '教师信息不存在'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        name = data.get('name')
        semester = data.get('semester')
        description = data.get('description', '')
        max_students = data.get('max_students', 50)

        if not name:
            return jsonify({'error': '请输入课程名称'}), 400

        if not semester:
            return jsonify({'error': '请输入学期'}), 400

        course_code = generate_course_code()
        while Course.query.filter_by(code=course_code).first():
            course_code = generate_course_code()

        course = Course(
            name=name,
            code=course_code,
            teacher_id=teacher.id,
            type='regular',
            description=description,
            max_students=max_students,
            semester=semester
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({
            'message': '课程创建成功',
            'course': course.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/courses/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'创建课程失败: {str(e)}'}), 500


@course_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_courses():
    """获取已加入课程列表（学生端）或我创建的课程列表（教师端），管理员可查看所有课程"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'student':
            student = current_user.student
            if not student:
                return jsonify({'error': '学生信息不存在'}), 404

            course_students = CourseStudent.query.filter_by(student_id=student.id).order_by(
                CourseStudent.is_starred.desc(),
                CourseStudent.joined_at.desc()
            ).all()

            my_courses = []
            for cs in course_students:
                course = cs.course
                if course:
                    course_dict = course.to_dict()
                    course_dict['is_starred'] = cs.is_starred
                    course_dict['joined_at'] = cs.joined_at.strftime('%Y-%m-%d %H:%M:%S') if cs.joined_at else None
                    my_courses.append(course_dict)

            return jsonify({
                'courses': my_courses
            }), 200

        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher:
                return jsonify({'error': '教师信息不存在'}), 404

            courses = Course.query.filter_by(teacher_id=teacher.id).order_by(
                Course.created_at.desc()
            ).all()

            return jsonify({
                'courses': [course.to_dict() for course in courses]
            }), 200

        elif current_user.role == 'admin':
            courses = Course.query.order_by(Course.created_at.desc()).all()

            courses_with_teacher = []
            for course in courses:
                course_dict = course.to_dict()
                course_dict['teacher_name'] = course.teacher.user.name if course.teacher and course.teacher.user else ''
                courses_with_teacher.append(course_dict)

            return jsonify({
                'courses': courses_with_teacher
            }), 200

        else:
            return jsonify({'error': '无权限查看课程'}), 403

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/my 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取课程列表失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_detail(course_id):
    """获取课程详情（管理员可查看所有课程）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限查看该课程'}), 403
        elif current_user.role == 'student':
            student = current_user.student
            if not student:
                return jsonify({'error': '学生信息不存在'}), 404
            exists = CourseStudent.query.filter_by(course_id=course_id, student_id=student.id).first()
            if not exists:
                return jsonify({'error': '未加入该课程'}), 403
        else:
            return jsonify({'error': '无权限查看该课程'}), 403

        return jsonify({
            'course': course.to_dict()
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/{course_id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取课程详情失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/students', methods=['GET'])
@jwt_required()
def get_course_students(course_id):
    """获取课程学生列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限查看该课程学生'}), 403
        else:
            return jsonify({'error': '仅教师可查看课程学生列表'}), 403

        course_students = CourseStudent.query.filter_by(course_id=course_id).order_by(
            CourseStudent.joined_at.desc()
        ).all()

        students_data = []
        for cs in course_students:
            student = cs.student
            if student:
                students_data.append({
                    'student_id': student.id,
                    'student_no': student.student_no,
                    'name': student.user.name if student.user else '',
                    'major': student.major,
                    'class_name': student.class_name(),
                    'joined_at': cs.joined_at.strftime('%Y-%m-%d %H:%M:%S') if cs.joined_at else None
                })

        return jsonify({
            'students': students_data
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/{course_id}/students 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取学生列表失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/students', methods=['POST'])
@jwt_required()
def add_course_student(course_id):
    """录入学生到课程"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if course.is_locked:
            return jsonify({'error': '课程已锁定，无法录入学生'}), 400

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限录入学生'}), 403
        else:
            return jsonify({'error': '无权限录入学生'}), 403

        data = request.get_json()
        if not data or 'student_no' not in data:
            return jsonify({'error': '请提供学生学号'}), 400

        student_no = data['student_no'].strip()
        student = Student.query.filter_by(student_no=student_no).first()

        if not student:
            return jsonify({'error': '学生不存在'}), 404

        existing = CourseStudent.query.filter_by(course_id=course_id, student_id=student.id).first()
        if existing:
            return jsonify({'error': '学生已在课程中'}), 400

        if course.student_count >= course.max_students:
            return jsonify({'error': '课程人数已满'}), 400

        course_student = CourseStudent(
            course_id=course_id,
            student_id=student.id
        )

        course.student_count += 1

        db.session.add(course_student)
        db.session.commit()

        return jsonify({
            'message': '学生录入成功',
            'student': {
                'student_id': student.id,
                'student_no': student.student_no,
                'name': student.user.name if student.user else ''
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/courses/{course_id}/students 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'录入学生失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
def remove_course_student(course_id, student_id):
    """从课程移除学生"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if course.is_locked:
            return jsonify({'error': '课程已锁定，无法移除学生'}), 400

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限移除学生'}), 403
        else:
            return jsonify({'error': '无权限移除学生'}), 403

        course_student = CourseStudent.query.filter_by(
            course_id=course_id,
            student_id=student_id
        ).first()

        if not course_student:
            return jsonify({'error': '学生不在该课程中'}), 404

        if course.student_count > 0:
            course.student_count -= 1

        db.session.delete(course_student)
        db.session.commit()

        return jsonify({'message': '学生移除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/courses/{course_id}/students/{student_id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'移除学生失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/invite', methods=['POST'])
@jwt_required()
def generate_course_invite(course_id):
    """生成课程邀请码"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限生成邀请码'}), 403
        else:
            return jsonify({'error': '无权限生成邀请码'}), 403

        if course.invite_code:
            return jsonify({'error': '邀请码已生成'}), 400

        invite_code = generate_invite_code()
        while Course.query.filter_by(invite_code=invite_code).first():
            invite_code = generate_invite_code()

        course.invite_code = invite_code
        db.session.commit()

        return jsonify({
            'message': '邀请码生成成功',
            'invite_code': invite_code
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/courses/{course_id}/invite 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'生成邀请码失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/qrcode', methods=['GET'])
@jwt_required()
def get_course_qrcode(course_id):
    """生成课程二维码（自动生成邀请码）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限获取二维码'}), 403
        else:
            return jsonify({'error': '无权限获取二维码'}), 403

        # 如果没有邀请码，自动生成
        if not course.invite_code:
            invite_code = generate_invite_code()
            while Course.query.filter_by(invite_code=invite_code).first():
                invite_code = generate_invite_code()
            course.invite_code = invite_code
            db.session.commit()

        # 构造加入链接（使用前端 Origin，兼容代理环境）
        origin = request.headers.get('Origin', '').rstrip('/')
        if not origin:
            origin = request.host_url.rstrip('/')
        join_url = f'{origin}/join?code={course.invite_code}'

        return jsonify({
            'qrcode_data': join_url,
            'join_url': join_url,
            'invite_code': course.invite_code,
            'code': course.invite_code
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/courses/{course_id}/qrcode 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取二维码失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>/lock', methods=['PUT'])
@jwt_required()
def lock_course(course_id):
    """锁定/解锁课程（锁定后禁止修改、删除及学生变动）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限锁定该课程'}), 403
        else:
            return jsonify({'error': '无权限锁定该课程'}), 403

        data = request.get_json()
        if not data or 'is_locked' not in data:
            return jsonify({'error': '参数错误：缺少 is_locked'}), 400

        course.is_locked = 1 if data.get('is_locked') else 0
        db.session.commit()

        return jsonify({
            'message': '课程已锁定' if course.is_locked else '课程已解锁',
            'is_locked': bool(course.is_locked)
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/courses/{course_id}/lock 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'锁定课程失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """修改课程信息"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if course.is_locked:
            return jsonify({'error': '课程已锁定，无法修改'}), 400

        if current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限修改课程信息'}), 403
        else:
            return jsonify({'error': '仅教师可修改课程信息'}), 403

        data = request.get_json()
        if not data:
            return jsonify({'error': '请求体为空'}), 400

        name = data.get('name')
        semester = data.get('semester')
        description = data.get('description')
        max_students = data.get('max_students')

        if name:
            course.name = name
        if semester:
            course.semester = semester
        if description is not None:
            course.description = description
        if max_students is not None:
            if max_students <= 0:
                return jsonify({'error': '最大人数必须大于0'}), 400
            course.max_students = max_students

        db.session.commit()

        return jsonify({
            'message': '课程信息修改成功',
            'course': course.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/courses/{course_id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'修改课程信息失败: {str(e)}'}), 500


@course_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    """删除课程"""
    try:
        from models import Achievement

        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': '课程不存在'}), 404

        if course.is_locked:
            return jsonify({'error': '课程已锁定，无法删除'}), 400

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or course.teacher_id != teacher.id:
                return jsonify({'error': '无权限删除课程'}), 403
        else:
            return jsonify({'error': '无权限删除课程'}), 403

        course_students = CourseStudent.query.filter_by(course_id=course_id).all()
        student_ids = [cs.student_id for cs in course_students]

        for cs in course_students:
            db.session.delete(cs)

        pending_achievements = Achievement.query.filter(
            Achievement.student_id.in_(student_ids),
            Achievement.status == 'pending'
        ).all()

        for achievement in pending_achievements:
            achievement.status = 'rejected'
            achievement.review_comment = '课程已删除'

        db.session.delete(course)
        db.session.commit()

        # 班级已并入课程，删除课程即原「删除班级」操作
        log_action('delete_course', f'删除课程“{course.name}”', user=current_user)

        return jsonify({'message': '课程删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/courses/{course_id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除课程失败: {str(e)}'}), 500
