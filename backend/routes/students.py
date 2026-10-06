from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Student, Teacher, Course, CourseStudent
from extensions import db

student_bp = Blueprint('student', __name__, url_prefix='/api/students')


@student_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    """获取学生列表"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        student_no = request.args.get('student_no')
        name = request.args.get('name')
        course_id = request.args.get('course_id', type=int)
        major = request.args.get('major')
        tab = request.args.get('tab', 'my_students')

        query = Student.query

        if current_user.role == 'teacher':
            teacher = current_user.teacher
            if teacher:
                if teacher.role == 'advisor':
                    course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                    if course_ids:
                        my_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(course_ids)).all()]
                        query = query.filter(Student.id.in_(my_student_ids))
                    else:
                        query = query.filter(Student.id == -1)
                elif teacher.role == '院系负责人' or teacher.role == 'head':
                    if tab == 'my_students':
                        my_course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                        if my_course_ids:
                            my_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(my_course_ids)).all()]
                            query = query.filter(Student.id.in_(my_student_ids))
                        else:
                            query = query.filter(Student.id == -1)
                    elif tab == 'other_students':
                        my_course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                        my_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(my_course_ids)).all()] if my_course_ids else []
                        
                        other_teachers = Teacher.query.filter(
                            Teacher.department.like(f'%{teacher.department}%'),
                            Teacher.id != teacher.id
                        ).all()
                        other_teacher_ids = [t.id for t in other_teachers]
                        
                        if other_teacher_ids:
                            other_course_ids = [c.id for c in Course.query.filter(Course.teacher_id.in_(other_teacher_ids)).all()]
                            if other_course_ids:
                                other_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(other_course_ids)).all()]
                                other_student_ids = list(set(other_student_ids) - set(my_student_ids))
                                query = query.filter(Student.id.in_(other_student_ids))
                            else:
                                query = query.filter(Student.id == -1)
                        else:
                            query = query.filter(Student.id == -1)
                elif teacher.role == 'faculty':
                    if tab == 'my_students':
                        my_course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                        if my_course_ids:
                            my_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(my_course_ids)).all()]
                            query = query.filter(Student.id.in_(my_student_ids))
                        else:
                            query = query.filter(Student.id == -1)
                    elif tab == 'other_students':
                        my_course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                        my_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(my_course_ids)).all()] if my_course_ids else []
                        
                        other_teachers = Teacher.query.filter(
                            Teacher.department.like(f'%{teacher.department}%'),
                            Teacher.id != teacher.id
                        ).all()
                        other_teacher_ids = [t.id for t in other_teachers]
                        
                        if other_teacher_ids:
                            other_course_ids = [c.id for c in Course.query.filter(Course.teacher_id.in_(other_teacher_ids)).all()]
                            if other_course_ids:
                                other_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(other_course_ids)).all()]
                                other_student_ids = list(set(other_student_ids) - set(my_student_ids))
                                query = query.filter(Student.id.in_(other_student_ids))
                            else:
                                query = query.filter(Student.id == -1)
                        else:
                            query = query.filter(Student.id == -1)
                elif teacher.role == 'teaching_admin':
                    query = query
                else:
                    return jsonify({
                        'students': [],
                        'pagination': {
                            'total': 0,
                            'pages': 0,
                            'current_page': page,
                            'per_page': page_size
                        }
                    }), 200
            else:
                return jsonify({
                    'students': [],
                    'pagination': {
                        'total': 0,
                        'pages': 0,
                        'current_page': page,
                        'per_page': page_size
                    }
                }), 200
        elif current_user.role == 'student':
            return jsonify({
                'students': [],
                'pagination': {
                    'total': 0,
                    'pages': 0,
                    'current_page': page,
                    'per_page': page_size
                }
            }), 200

        if student_no:
            query = query.filter(Student.student_no.like(f'%{student_no}%'))
        if name:
            query = query.join(User, User.id == Student.user_id).filter(User.name.like(f'%{name}%'))
        if course_id:
            course_student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id == course_id).all()]
            if course_student_ids:
                query = query.filter(Student.id.in_(course_student_ids))
            else:
                query = query.filter(Student.id == -1)
        if major:
            query = query.filter(Student.major.like(f'%{major}%'))

        paginated = query.order_by(Student.student_no).paginate(
            page=page, per_page=page_size, error_out=False
        )

        students = []
        for student in paginated.items:
            student_dict = student.to_dict()
            student_dict['name'] = student.user.name if student.user else ''
            student_dict['class_name'] = student.class_name() or ''
            student_dict['achievement_count'] = len(student.achievements)
            students.append(student_dict)

        return jsonify({
            'students': students,
            'pagination': {
                'total': paginated.total,
                'pages': paginated.pages,
                'current_page': paginated.page,
                'per_page': paginated.per_page
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/students/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取学生列表失败: {str(e)}'}), 500


@student_bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    """添加学生"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ['head', 'advisor', 'admin']:
                return jsonify({'error': '无权添加学生'}), 403
        else:
            return jsonify({'error': '无权添加学生'}), 403

        data = request.get_json()
        required_fields = ['student_no', 'name', 'course_id']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

        if User.query.filter_by(username=data['student_no']).first():
            return jsonify({'error': '学号已存在'}), 400

        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({'error': '课程不存在'}), 400

        user = User(
            username=data['student_no'],
            role='student',
            name=data['name']
        )
        user.set_password(data.get('password', '123456'))

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            student_no=data['student_no'],
            class_id=None,
            major=data.get('major'),
            phone=data.get('phone')
        )
        db.session.add(student)
        db.session.flush()

        db.session.add(CourseStudent(course_id=course.id, student_id=student.id))
        course.student_count = (course.student_count or 0) + 1
        db.session.commit()

        return jsonify({
            'message': '学生添加成功',
            'student': student.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== POST /api/students/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加学生失败: {str(e)}'}), 500


@student_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    """获取学生详情"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        student = Student.query.get(id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404

        if current_user.role == 'student':
            if student.id != current_user.student.id:
                return jsonify({'error': '无权查看'}), 403

        student_dict = student.to_dict()
        student_dict['name'] = student.user.name if student.user else ''
        student_dict['class_name'] = student.class_name() or ''

        return jsonify({'student': student_dict}), 200

    except Exception as e:
        return jsonify({'error': f'获取学生详情失败: {str(e)}'}), 500


@student_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    """修改学生信息"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ['head', 'advisor', 'faculty']:
                return jsonify({'error': '无权修改学生信息'}), 403
        else:
            return jsonify({'error': '无权修改学生信息'}), 403

        student = Student.query.get(id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404

        data = request.get_json()

        if 'name' in data:
            student.user.name = data['name']
        if 'course_id' in data:
            course = Course.query.get(data['course_id'])
            if not course:
                return jsonify({'error': '课程不存在'}), 400
            existing = CourseStudent.query.filter_by(course_id=course.id, student_id=student.id).first()
            if not existing:
                db.session.add(CourseStudent(course_id=course.id, student_id=student.id))
                course.student_count = (course.student_count or 0) + 1
        if 'major' in data:
            student.major = data['major']
        if 'phone' in data:
            student.phone = data['phone']
        if 'department' in data:
            student.department = data['department']

        db.session.commit()

        student_dict = student.to_dict()
        student_dict['name'] = student.user.name
        student_dict['department'] = student.department

        return jsonify({
            'message': '学生信息更新成功',
            'student': student_dict
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新学生信息失败: {str(e)}'}), 500


@student_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    """删除学生（从班级中移除）"""
    try:
        from models import Achievement

        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ['head', 'advisor', 'faculty']:
                return jsonify({'error': '无权删除学生'}), 403
        else:
            return jsonify({'error': '无权删除学生'}), 403

        student = Student.query.get(id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404

        if current_user.role == 'teacher':
            teacher = current_user.teacher
            if teacher.role == 'advisor':
                course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
                in_teacher_course = False
                if course_ids:
                    in_teacher_course = CourseStudent.query.filter(
                        CourseStudent.course_id.in_(course_ids),
                        CourseStudent.student_id == student.id
                    ).first() is not None
                if not in_teacher_course:
                    return jsonify({'error': '只能删除本课程学生'}), 403

        pending_achievements = Achievement.query.filter(
            Achievement.student_id == id,
            Achievement.status == 'pending'
        ).all()

        for achievement in pending_achievements:
            achievement.status = 'rejected'
            achievement.review_comment = '已从课程中移除'

        db.session.delete(student)
        db.session.commit()

        return jsonify({'message': '学生已从课程中移除'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除学生失败: {str(e)}'}), 500


@student_bp.route('/<int:id>/reset-password', methods=['PUT'])
@jwt_required()
def reset_password(id):
    """重置学生密码"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role == 'admin':
            pass
        elif current_user.role == 'teacher':
            teacher = current_user.teacher
            if not teacher or teacher.role not in ['head', 'advisor', 'faculty', 'teaching_admin']:
                return jsonify({'error': '无权重置密码'}), 403
        else:
            return jsonify({'error': '无权重置密码'}), 403

        student = Student.query.get(id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404

        data = request.get_json()
        new_password = data.get('password', '123456')

        student.user.set_password(new_password)
        db.session.commit()

        return jsonify({'message': '密码重置成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'重置密码失败: {str(e)}'}), 500
