# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import User, Class, Teacher, Student, ClassApplication, Course
# from extensions import db
# from datetime import datetime

# class_bp = Blueprint('class', __name__, url_prefix='/api/classes')


# @class_bp.route('/', methods=['GET'])
# @jwt_required()
# def get_classes():
#     """获取班级列表"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         page = request.args.get('page', 1, type=int)
#         page_size = request.args.get('page_size', 20, type=int)
#         name = request.args.get('name')
#         department = request.args.get('department')
#         grade = request.args.get('grade')

#         query = Class.query

#         if current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if teacher:
#                 if teacher.role == 'advisor':
#                     query = query.filter(Class.advisor_id == teacher.id)
#                 elif teacher.role == 'head':
#                     if teacher.department:
#                         query = query.filter(Class.department.like(f'%{teacher.department}%'))
#                 elif teacher.role == 'faculty':
#                     query = query.filter(Class.id == -1)
#                 elif teacher.role == 'teaching_admin':
#                     pass
#                 else:
#                     query = query.filter(Class.id == -1)
#         elif current_user.role == 'student':
#             return jsonify({
#                 'classes': [],
#                 'pagination': {
#                     'total': 0,
#                     'pages': 0,
#                     'current_page': page,
#                     'per_page': page_size
#                 }
#             }), 200

#         if name:
#             query = query.filter(Class.name.like(f'%{name}%'))
#         if department:
#             query = query.filter(Class.department.like(f'%{department}%'))
#         if grade:
#             query = query.filter(Class.grade == grade)

#         paginated = query.order_by(Class.id).paginate(
#             page=page, per_page=page_size, error_out=False
#         )

#         classes = []
#         for cls in paginated.items:
#             cls_dict = cls.to_dict()
#             cls_dict['student_count'] = len(cls.students)
#             cls_dict['advisor_name'] = cls.advisor.user.name if cls.advisor and cls.advisor.user else ''
#             cls_dict['type'] = 'class'
#             classes.append(cls_dict)

#         course_query = Course.query
#         if current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if teacher:
#                 course_query = course_query.filter(Course.teacher_id == teacher.id)
#         elif current_user.role == 'admin':
#             pass
#         else:
#             course_query = course_query.filter(Course.id == -1)

#         if name:
#             course_query = course_query.filter(Course.name.like(f'%{name}%'))

#         courses = course_query.order_by(Course.created_at.desc()).all()
#         for course in courses:
#             course_dict = course.to_dict()
#             course_dict['student_count'] = course.student_count
#             course_dict['advisor_name'] = course.teacher.user.name if course.teacher and course.teacher.user else ''
#             course_dict['department'] = course.teacher.department if course.teacher else ''
#             course_dict['grade'] = ''
#             course_dict['type'] = 'course'
#             classes.append(course_dict)

#         return jsonify({
#             'classes': classes,
#             'pagination': {
#                 'total': len(classes),
#                 'pages': 1,
#                 'current_page': 1,
#                 'per_page': len(classes) if len(classes) < page_size else page_size
#             }
#         }), 200

#     except Exception as e:
#         import traceback
#         print(f"\n=== GET /api/classes/ 错误 ===")
#         print(f"错误类型: {type(e).__name__}")
#         print(f"错误信息: {str(e)}")
#         print(f"错误堆栈: {traceback.format_exc()}")
#         return jsonify({'error': f'获取班级列表失败: {str(e)}'}), 500


# @class_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_class():
#     """添加班级"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role == 'admin':
#             pass
#         elif current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if not teacher or teacher.role not in ['head', 'admin']:
#                 return jsonify({'error': '无权添加班级'}), 403
#         else:
#             return jsonify({'error': '无权添加班级'}), 403

#         data = request.get_json()
#         required_fields = ['id', 'name', 'department', 'grade']
#         missing_fields = [field for field in required_fields if field not in data or not data[field]]
#         if missing_fields:
#             return jsonify({'error': f'缺少必填字段: {", ".join(missing_fields)}'}), 400

#         if Class.query.get(data['id']):
#             return jsonify({'error': '班级编号已存在'}), 400

#         cls = Class(
#             id=data['id'],
#             name=data['name'],
#             department=data['department'],
#             grade=data['grade'],
#             advisor_id=data.get('advisor_id')
#         )

#         db.session.add(cls)
#         db.session.commit()

#         return jsonify({
#             'message': '班级添加成功',
#             'class': cls.to_dict()
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'添加班级失败: {str(e)}'}), 500


# @class_bp.route('/<string:id>', methods=['PUT'])
# @jwt_required()
# def update_class(id):
#     """修改班级信息"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role == 'admin':
#             pass
#         elif current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if not teacher or teacher.role not in ['head', 'admin']:
#                 return jsonify({'error': '无权修改班级'}), 403
#         else:
#             return jsonify({'error': '无权修改班级'}), 403

#         cls = Class.query.get(id)
#         if not cls:
#             return jsonify({'error': '班级不存在'}), 404

#         data = request.get_json()

#         # 如果班级已锁定，禁止修改班级名称
#         if cls.is_locked and 'name' in data and data['name'] != cls.name:
#             return jsonify({'error': '班级已锁定，无法修改班级名称'}), 400

#         if 'name' in data:
#             cls.name = data['name']
#         if 'department' in data:
#             cls.department = data['department']
#         if 'grade' in data:
#             cls.grade = data['grade']
#         if 'advisor_id' in data:
#             cls.advisor_id = data['advisor_id']

#         db.session.commit()

#         return jsonify({
#             'message': '班级信息更新成功',
#             'class': cls.to_dict()
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'更新班级失败: {str(e)}'}), 500


# @class_bp.route('/<string:id>', methods=['DELETE'])
# @jwt_required()
# def delete_class(id):
#     """删除班级"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role == 'admin':
#             pass
#         elif current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if not teacher or teacher.role not in ['head', 'admin']:
#                 return jsonify({'error': '无权删除班级'}), 403
#         else:
#             return jsonify({'error': '无权删除班级'}), 403

#         cls = Class.query.get(id)
#         if not cls:
#             return jsonify({'error': '班级不存在'}), 404

#         # 校验班级是否已锁定
#         if cls.is_locked:
#             return jsonify({'error': '班级已锁定，无法删除'}), 400

#         db.session.delete(cls)
#         db.session.commit()

#         return jsonify({'message': '班级删除成功'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'删除班级失败: {str(e)}'}), 500


# @class_bp.route('/apply', methods=['POST'])
# @jwt_required()
# def apply_class():
#     """学生申请加入班级"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role != 'student':
#             return jsonify({'error': '只有学生可以申请加入班级'}), 403

#         student = current_user.student
#         if not student:
#             return jsonify({'error': '学生信息不存在'}), 404

#         if student.class_id:
#             return jsonify({'error': '已加入班级，请勿重复申请'}), 400

#         data = request.get_json()
#         class_id = data.get('class_id')

#         if not class_id:
#             return jsonify({'error': '请指定班级'}), 400

#         cls = Class.query.get(class_id)
#         if not cls:
#             return jsonify({'error': '班级不存在'}), 400

#         existing_application = ClassApplication.query.filter(
#             ClassApplication.student_id == student.id,
#             ClassApplication.status == 'pending'
#         ).first()
#         if existing_application:
#             return jsonify({'error': '已有待处理的申请'}), 400

#         application = ClassApplication(
#             student_id=student.id,
#             class_id=class_id
#         )

#         db.session.add(application)
#         db.session.commit()

#         return jsonify({
#             'message': '申请提交成功',
#             'application': application.to_dict()
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         import traceback
#         print(f"\n=== POST /api/classes/apply 错误 ===")
#         print(f"错误类型: {type(e).__name__}")
#         print(f"错误信息: {str(e)}")
#         print(f"错误堆栈: {traceback.format_exc()}")
#         return jsonify({'error': f'申请失败: {str(e)}'}), 500


# @class_bp.route('/applications', methods=['GET'])
# @jwt_required()
# def get_class_applications():
#     """辅导员查看申请列表"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role == 'admin':
#             pass
#         elif current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if not teacher or teacher.role not in ['advisor', 'head']:
#                 return jsonify({'error': '无权查看申请'}), 403
#         else:
#             return jsonify({'error': '无权查看申请'}), 403

#         page = request.args.get('page', 1, type=int)
#         page_size = request.args.get('page_size', 20, type=int)
#         class_id = request.args.get('class_id')
#         status = request.args.get('status')

#         query = ClassApplication.query

#         if current_user.role == 'teacher' and current_user.teacher:
#             teacher = current_user.teacher
#             if teacher.role == 'advisor':
#                 query = query.join(Class, Class.id == ClassApplication.class_id).filter(Class.advisor_id == teacher.id)

#         if class_id:
#             query = query.filter(ClassApplication.class_id == class_id)

#         if status:
#             query = query.filter(ClassApplication.status == status)

#         query = query.order_by(ClassApplication.applied_at.desc())
#         paginated = query.paginate(page=page, per_page=page_size, error_out=False)

#         applications = []
#         for app in paginated.items:
#             app_dict = app.to_dict()
#             app_dict['student_name'] = app.student.user.name if app.student and app.student.user else ''
#             app_dict['student_no'] = app.student.student_no if app.student else ''
#             app_dict['class_name'] = app.cls.name if app.cls else ''
#             app_dict['processed_by_name'] = app.processed_by_user.user.name if app.processed_by_user and app.processed_by_user.user else ''
#             applications.append(app_dict)

#         return jsonify({
#             'applications': applications,
#             'pagination': {
#                 'total': paginated.total,
#                 'pages': paginated.pages,
#                 'current_page': paginated.page,
#                 'per_page': paginated.per_page
#             }
#         }), 200

#     except Exception as e:
#         import traceback
#         print(f"\n=== GET /api/classes/applications 错误 ===")
#         print(f"错误类型: {type(e).__name__}")
#         print(f"错误信息: {str(e)}")
#         print(f"错误堆栈: {traceback.format_exc()}")
#         return jsonify({'error': f'获取申请列表失败: {str(e)}'}), 500


# @class_bp.route('/applications/<int:id>', methods=['PUT'])
# @jwt_required()
# def process_application(id):
#     """审核通过/驳回"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         if current_user.role != 'teacher':
#             return jsonify({'error': '只有教师可以审核申请'}), 403

#         teacher = current_user.teacher
#         if not teacher:
#             return jsonify({'error': '教师信息不存在'}), 404

#         application = ClassApplication.query.get(id)
#         if not application:
#             return jsonify({'error': '申请不存在'}), 404

#         if teacher.role == 'advisor':
#             cls = Class.query.get(application.class_id)
#             if not cls or cls.advisor_id != teacher.id:
#                 return jsonify({'error': '无权审核此申请'}), 403

#         data = request.get_json()
#         status = data.get('status')

#         if status not in ['approved', 'rejected']:
#             return jsonify({'error': '无效的审核状态'}), 400

#         application.status = status
#         application.processed_at = datetime.now()
#         application.processed_by = teacher.id

#         if status == 'approved':
#             student = Student.query.get(application.student_id)
#             if student:
#                 student.class_id = application.class_id

#         db.session.commit()

#         return jsonify({
#             'message': '审核完成',
#             'application': application.to_dict()
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         import traceback
#         print(f"\n=== PUT /api/classes/applications/{id} 错误 ===")
#         print(f"错误类型: {type(e).__name__}")
#         print(f"错误信息: {str(e)}")
#         print(f"错误堆栈: {traceback.format_exc()}")
#         return jsonify({'error': f'审核失败: {str(e)}'}), 500


# @class_bp.route('/<string:id>/lock', methods=['PUT'])
# @jwt_required()
# def toggle_class_lock(id):
#     """锁定/解锁班级"""
#     try:
#         current_user_id = int(get_jwt_identity())
#         current_user = User.query.get(current_user_id)

#         if not current_user:
#             return jsonify({'error': '用户不存在'}), 404

#         # 权限校验：管理员或有class:lock权限的教师
#         if current_user.role == 'admin':
#             pass
#         elif current_user.role == 'teacher':
#             teacher = current_user.teacher
#             if not teacher or teacher.role not in ['head', 'admin', 'advisor']:
#                 return jsonify({'error': '无权锁定/解锁班级'}), 403
#         else:
#             return jsonify({'error': '无权锁定/解锁班级'}), 403

#         cls = Class.query.get(id)
#         if not cls:
#             return jsonify({'error': '班级不存在'}), 404

#         data = request.get_json() or {}
#         if 'is_locked' in data:
#             # 前端显式指定
#             cls.is_locked = 1 if data['is_locked'] else 0
#         else:
#             # 切换状态
#             cls.is_locked = 0 if cls.is_locked else 1

#         db.session.commit()

#         status_text = '已锁定' if cls.is_locked else '已解锁'
#         return jsonify({
#             'message': f'班级{status_text}成功',
#             'class': cls.to_dict()
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         import traceback
#         print(f"\n=== PUT /api/classes/{id}/lock 错误 ===")
#         print(f"错误类型: {type(e).__name__}")
#         print(f"错误信息: {str(e)}")
#         print(f"错误堆栈: {traceback.format_exc()}")
#         return jsonify({'error': f'锁定/解锁失败: {str(e)}'}), 500
