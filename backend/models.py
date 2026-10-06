from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Competition(db.Model):
    """竞赛信息表（第二课堂）"""
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month = db.Column(db.String(10), comment='月份')
    name = db.Column(db.String(200), comment='竞赛名称')
    category = db.Column(db.String(50), comment='竞赛分类')
    sign_start = db.Column(db.String(20), comment='报名开始')
    sign_end = db.Column(db.String(20), comment='报名结束')
    heat = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment='热度值')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self, **extra):
        data = {
            'id': self.id,
            'month': self.month,
            'name': self.name,
            'category': self.category,
            'sign_start': self.sign_start,
            'sign_end': self.sign_end,
            'heat': self.heat,
        }
        data.update(extra)
        return data


class CompetitionFavorite(db.Model):
    """比赛收藏表（我的比赛）"""
    __tablename__ = 'competition_favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    competition = db.relationship('Competition', backref='favorites')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'competition_id': self.competition_id,
            'competition': self.competition.to_dict() if self.competition else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    login_fail_count = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment='连续登录失败次数')
    locked_until = db.Column(db.DateTime, nullable=True, comment='账号锁定截止时间，NULL为未锁定')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

    # 关系
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    teacher = db.relationship('Teacher', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Student(db.Model):
    """学生表"""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_no = db.Column(db.String(20), nullable=False, unique=True)
    class_id = db.Column(db.String(20), nullable=True)  # TODO(未来) 接入学校系统重建班级时恢复 db.ForeignKey('classes.id')
    major = db.Column(db.String(100))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    enrolled_at = db.Column(db.Date)
    id_card = db.Column(db.String(18))

    # 关系
    achievements = db.relationship('Achievement', backref='student', cascade='all, delete-orphan')
    # TODO(未来) 接入学校系统后，重建“班级”概念（学生自动加入/教师自动匹配）时恢复此关系：
    # class_info = db.relationship('Class', backref='students', foreign_keys=[class_id])

    def class_name(self):
        """由学生当前加入的首个课程派生展示名（班级已并入课程）"""
        cs = getattr(self, 'course_students', None)
        if cs:
            for m in cs:
                if m.course:
                    return m.course.name
        return None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_no': self.student_no,
            'class_id': self.class_id,
            'class_name': self.class_name(),
            'major': self.major,
            'phone': self.phone,
            'avatar': self.avatar,
            'department': self.department,
            'enrolled_at': self.enrolled_at.strftime('%Y-%m-%d') if self.enrolled_at else None
        }


class Teacher(db.Model):
    """教师/辅导员表"""
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    teacher_no = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(100))
    title = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='faculty')
    department_id = db.Column(db.Integer, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    status = db.Column(db.String(20), default='pending', comment='账号状态：pending(待审核), approved(已通过)')

    # 关系
    # TODO(未来) 班级并入课程，恢复班级概念时启用：
    # classes_advised = db.relationship('Class', backref='advisor', foreign_keys='Class.advisor_id')
    achievements_reviewed = db.relationship('Achievement', backref='teacher', foreign_keys='Achievement.teacher_id')
    # TODO(未来) 恢复班级概念时启用：
    # class_applications_processed = db.relationship('ClassApplication', backref='processed_by_user', foreign_keys='ClassApplication.processed_by')
    role_info = db.relationship('Role', backref='teachers')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'teacher_no': self.teacher_no,
            'department': self.department,
            'title': self.title,
            'phone': self.phone,
            'role': self.role,
            'department_id': self.department_id,
            'role_id': self.role_id,
            'role_name': self.role_info.name if self.role_info else None
        }


# TODO(未来) 班级已并入课程。接入学校系统、重建“班级”（学生自动加入/教师自动匹配）时恢复本模型：
# class Class(db.Model):
#     """班级表"""
#     __tablename__ = 'classes'
#
#     id = db.Column(db.String(20), primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     department = db.Column(db.String(100))
#     advisor_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
#     grade = db.Column(db.Integer)
#     student_count = db.Column(db.Integer, default=0)
#     is_locked = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment='是否锁定：0-未锁定，1-已锁定')
#     created_at = db.Column(db.TIMESTAMP, default=datetime.now)
#
#     def to_dict(self):
#         """转换为字典"""
#         return {
#             'id': self.id,
#             'name': self.name,
#             'department': self.department,
#             'advisor_id': self.advisor_id,
#             'advisor_name': self.advisor.user.name if self.advisor and self.advisor.user else None,
#             'grade': self.grade,
#             'student_count': self.student_count,
#             'is_locked': bool(self.is_locked),
#             'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
#         }


class Achievement(db.Model):
    """成果表"""
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    main_category = db.Column(db.String(50), nullable=False, comment='一级分类')
    sub_category = db.Column(db.String(50), nullable=True, comment='二级细分')
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    achieved_date = db.Column(db.Date)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    submitted_at = db.Column(db.TIMESTAMP, default=datetime.now)
    reviewed_at = db.Column(db.TIMESTAMP)
    review_comment = db.Column(db.Text)
    auditor_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True, comment='审核人教师ID')

    # 关系
    attachments = db.relationship('AchievementAttachment', backref='achievement', cascade='all, delete-orphan')
    auditor = db.relationship('Teacher', foreign_keys=[auditor_id], backref='audited_achievements')

    def to_dict(self, include_attachments=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.user.name if self.student and self.student.user else None,
            'student_no': self.student.student_no if self.student else None,
            'class_name': self.student.class_name() if self.student else None,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.user.name if self.teacher and self.teacher.user else None,
            'main_category': self.main_category,
            'sub_category': self.sub_category,
            'title': self.title,
            'level': self.level,
            'achieved_date': self.achieved_date.strftime('%Y-%m-%d') if self.achieved_date else None,
            'description': self.description,
            'status': self.status,
            'submitted_at': self.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if self.submitted_at else None,
            'reviewed_at': self.reviewed_at.strftime('%Y-%m-%d %H:%M:%S') if self.reviewed_at else None,
            'review_comment': self.review_comment,
            'auditor_id': self.auditor_id,
            'auditor_name': self.auditor.user.name if self.auditor and self.auditor.user else None
        }

        if include_attachments:
            data['attachments'] = [att.to_dict() for att in self.attachments]

        return data


class AchievementAttachment(db.Model):
    """附件表"""
    __tablename__ = 'achievement_attachments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.BigInteger)
    file_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'achievement_id': self.achievement_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'uploaded_at': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S') if self.uploaded_at else None
        }


class AchievementKnowledge(db.Model):
    """成果知识库表"""
    __tablename__ = 'achievement_knowledge'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(100))
    level = db.Column(db.String(20), nullable=False)
    level_priority = db.Column(db.Integer, default=0)
    keywords = db.Column(db.Text)
    proof_required = db.Column(db.Text)
    school_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'sub_category': self.sub_category,
            'level': self.level,
            'level_priority': self.level_priority,
            'keywords': self.keywords,
            'proof_required': self.proof_required,
            'school_id': self.school_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class ProofRequirement(db.Model):
    """证明材料要求表"""
    __tablename__ = 'proof_requirements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(100))
    proof_type = db.Column(db.String(100), nullable=False)
    is_required = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'category': self.category,
            'sub_category': self.sub_category,
            'proof_type': self.proof_type,
            'is_required': bool(self.is_required),
            'description': self.description
        }


# TODO(未来) 班级并入课程，恢复班级概念时启用本模型：
# class ClassApplication(db.Model):
#     """班级申请表"""
#     __tablename__ = 'class_applications'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
#     class_id = db.Column(db.String(20), db.ForeignKey('classes.id'), nullable=False)
#     status = db.Column(db.String(20), default='pending')
#     applied_at = db.Column(db.TIMESTAMP, default=datetime.now)
#     processed_at = db.Column(db.TIMESTAMP)
#     processed_by = db.Column(db.Integer, db.ForeignKey('teachers.id'))
#
#     # 关系
#     student = db.relationship('Student', backref='class_applications')
#     cls = db.relationship('Class', backref='class_applications')
#
#     def to_dict(self):
#         """转换为字典"""
#         return {
#             'id': self.id,
#             'student_id': self.student_id,
#             'class_id': self.class_id,
#             'status': self.status,
#             'applied_at': self.applied_at.strftime('%Y-%m-%d %H:%M:%S') if self.applied_at else None,
#             'processed_at': self.processed_at.strftime('%Y-%m-%d %H:%M:%S') if self.processed_at else None,
#             'processed_by': self.processed_by
#         }


class Course(db.Model):
    """课程表"""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    invite_code = db.Column(db.String(6), unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    type = db.Column(db.String(20), default='regular', comment='regular-常规课程, micro-微课程')
    description = db.Column(db.Text)
    max_students = db.Column(db.Integer, default=100)
    student_count = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment='是否锁定：0-未锁定，1-已锁定')
    semester = db.Column(db.String(50), comment='学期')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    # 关系
    teacher = db.relationship('Teacher', backref='courses')
    students = db.relationship('CourseStudent', backref='course', cascade='all, delete-orphan')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'invite_code': self.invite_code,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.user.name if self.teacher and self.teacher.user else None,
            'type': self.type,
            'description': self.description,
            'max_students': self.max_students,
            'student_count': self.student_count,
            'is_locked': bool(self.is_locked),
            'semester': self.semester,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class CourseStudent(db.Model):
    """课程学生关联表"""
    __tablename__ = 'course_students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    is_starred = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.TIMESTAMP, default=datetime.now)

    # 关系
    student = db.relationship('Student', backref='course_students')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'is_starred': bool(self.is_starred),
            'joined_at': self.joined_at.strftime('%Y-%m-%d %H:%M:%S') if self.joined_at else None
        }


class Role(db.Model):
    """角色表"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    permissions = db.Column(db.Text, comment='权限列表JSON')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """转换为字典"""
        import json
        return {
            'id': self.id,
            'name': self.name,
            'permissions': json.loads(self.permissions) if self.permissions else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class Team(db.Model):
    """团队表"""
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    invite_code = db.Column(db.String(20), unique=True)
    join_method = db.Column(db.String(20), default='code', comment='加入方式：code(邀请码), qr(扫码), both(两者皆可)')
    type = db.Column(db.String(30), default='department', comment='团队类型：department院系, subject_group科组, campus校区, grade年级, other其他')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

    creator = db.relationship('Teacher', backref='teams_created')

    def to_dict(self, include_joined_at=False, teacher_id=None):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'creator_id': self.creator_id,
            'creator_name': self.creator.user.name if self.creator else None,
            'creator_no': self.creator.teacher_no if self.creator else None,
            'invite_code': self.invite_code,
            'join_method': self.join_method,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
        if include_joined_at and teacher_id:
            tm = TeamMember.query.filter_by(team_id=self.id, teacher_id=teacher_id).first()
            if tm and tm.joined_at:
                data['joined_at'] = tm.joined_at.strftime('%Y-%m-%d %H:%M:%S')
        return data


class SystemLog(db.Model):
    """系统操作日志表"""
    __tablename__ = 'system_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    role = db.Column(db.String(20))
    action_type = db.Column(db.String(50))
    action_detail = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    result = db.Column(db.String(20))
    level = db.Column(db.String(10))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'action_type': self.action_type,
            'action_detail': self.action_detail,
            'ip_address': self.ip_address,
            'result': self.result,
            'level': self.level,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Notification(db.Model):
    """站内信消息表"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.String(50), comment='消息类型，用于前端区分场景')
    is_read = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment='是否已读：0-未读，1-已读')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

    user = db.relationship('User', backref='notifications')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'is_read': bool(self.is_read),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


def send_notification(user_id, title, content=None, type=None):
    """消息通知工具：创建一条站内信并提交"""
    if not user_id:
        return None
    notification = Notification(
        user_id=user_id,
        title=title,
        content=content,
        type=type
    )
    db.session.add(notification)
    db.session.commit()
    return notification


class VerificationCode(db.Model):
    """验证码表"""
    __tablename__ = 'verification_codes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.TIMESTAMP, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'code': self.code,
            'expires_at': self.expires_at.strftime('%Y-%m-%d %H:%M:%S') if self.expires_at else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class KnowledgeBase(db.Model):
    """成果知识库表"""
    __tablename__ = 'knowledge_base'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_achievement_id = db.Column(db.Integer, comment='来源成果ID（关联原成果）')
    title = db.Column(db.String(255), nullable=False, comment='成果标题')
    category_level1 = db.Column(db.String(50), comment='一级分类')
    category_level2 = db.Column(db.String(50), comment='二级细分')
    level = db.Column(db.String(50), comment='级别')
    student_name = db.Column(db.String(50), comment='学生姓名')
    class_name = db.Column(db.String(50), comment='班级')
    description = db.Column(db.Text, comment='描述')
    proof_material = db.Column(db.String(500), comment='证明材料备份路径')
    status = db.Column(db.String(20), default='approved', comment='状态（固定为 approved）')
    auditor_name = db.Column(db.String(50), comment='审核人')
    audit_comment = db.Column(db.Text, comment='审核意见')
    submitted_at = db.Column(db.TIMESTAMP, comment='提交时间')
    reviewed_at = db.Column(db.TIMESTAMP, comment='审核时间')
    created_at = db.Column(db.TIMESTAMP, default=datetime.now, comment='录入知识库时间')
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'source_achievement_id': self.source_achievement_id,
            'title': self.title,
            'category_level1': self.category_level1,
            'category_level2': self.category_level2,
            'level': self.level,
            'student_name': self.student_name,
            'class_name': self.class_name,
            'description': self.description,
            'proof_material': self.proof_material,
            'status': self.status,
            'auditor_name': self.auditor_name,
            'audit_comment': self.audit_comment,
            'submitted_at': self.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if self.submitted_at else None,
            'reviewed_at': self.reviewed_at.strftime('%Y-%m-%d %H:%M:%S') if self.reviewed_at else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class TeamMember(db.Model):
    """团队成员关联表"""
    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    role = db.Column(db.String(20), default='member', comment='角色：leader(负责人), member(成员)')
    joined_at = db.Column(db.TIMESTAMP, default=datetime.now)

    team = db.relationship('Team', backref=db.backref('members', cascade='all, delete-orphan'))
    teacher = db.relationship('Teacher', backref='teams')

    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.user.name if self.teacher else None,
            'teacher_no': self.teacher.teacher_no if self.teacher else None,
            'role': self.role,
            'joined_at': self.joined_at.strftime('%Y-%m-%d %H:%M:%S') if self.joined_at else None
        }