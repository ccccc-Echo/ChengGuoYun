from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Achievement, User, Student, Teacher, Course, CourseStudent, AchievementKnowledge
from extensions import db
from constants import (
    get_main_category_label, get_sub_category_label, get_level_label, MAIN_CATEGORY_MAP
)
from routes.achievements import build_auditor_display
import os
import io
from datetime import datetime

export_bp = Blueprint('student_export', __name__, url_prefix='/api/student/export')


def _resolve_attachment_disk_path(file_path):
    """将附件存储的 URL 路径(/uploads/xxx)解析为磁盘绝对路径"""
    if not file_path:
        return None
    filename = os.path.basename(file_path)
    return os.path.join(current_app.config['UPLOAD_FOLDER'], filename)


def generate_certificates_pdf(user, student, achievements):
    """生成获奖证书汇总 PDF（reportlab + 中文 CID 字体）"""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, PageBreak, KeepTogether
    )
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from PIL import Image as PILImage

    # 注册中文 CID 字体（reportlab 自带，无需外部字体文件）
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    font_name = 'STSong-Light'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title='获奖证书汇总'
    )
    avail_width = doc.width

    primary = colors.HexColor('#4095e5')
    label_color = colors.HexColor('#666666')
    bg_color = colors.HexColor('#f5f7fa')
    border_color = colors.HexColor('#dcdfe6')
    grid_color = colors.HexColor('#e4e7ed')

    title_style = ParagraphStyle('CNTitle', fontName=font_name, fontSize=20,
                                 alignment=1, spaceAfter=10, textColor=colors.HexColor('#1a1a2e'))
    subtitle_style = ParagraphStyle('CNSub', fontName=font_name, fontSize=10.5,
                                    textColor=colors.grey, spaceAfter=3)
    section_style = ParagraphStyle('CNSection', fontName=font_name, fontSize=13,
                                   textColor=primary, spaceBefore=8, spaceAfter=6)
    body_style = ParagraphStyle('CNBody', fontName=font_name, fontSize=10.5, leading=15)
    label_style = ParagraphStyle('CNLabel', fontName=font_name, fontSize=10.5,
                                 textColor=label_color, leading=15)
    small_grey = ParagraphStyle('CNSmallGrey', fontName=font_name, fontSize=9.5,
                                textColor=colors.grey, spaceBefore=2)

    story = []

    # 封面标题区
    story.append(Paragraph('获奖证书汇总', title_style))
    student_name = user.name or ''
    student_no = student.student_no or ''
    class_name = student.class_name() or ''
    major = student.major or ''
    story.append(Paragraph(
        f"姓名：{student_name}　　学号：{student_no}　　课程：{class_name}　　专业：{major}",
        subtitle_style))
    story.append(Paragraph(
        f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}　　共 {len(achievements)} 项已通过成果",
        subtitle_style))
    story.append(Spacer(1, 10))

    for idx, ach in enumerate(achievements, 1):
        block = []
        block.append(Paragraph(f"{idx}. {ach.title or ''}", section_style))

        rows = [
            ('一级分类', get_main_category_label(ach.main_category) or '-'),
            ('二级细分', get_sub_category_label(ach.sub_category) if ach.sub_category else '-'),
            ('级别', get_level_label(ach.level) or '-'),
            ('获奖日期', ach.achieved_date.strftime('%Y-%m-%d') if ach.achieved_date else '-'),
            ('状态', '已通过'),
            ('审核人', build_auditor_display(ach) or '-'),
            ('审核时间', ach.reviewed_at.strftime('%Y-%m-%d %H:%M') if ach.reviewed_at else '-'),
            ('提交时间', ach.submitted_at.strftime('%Y-%m-%d %H:%M') if ach.submitted_at else '-'),
            ('审核意见', ach.review_comment or '-'),
            ('成果描述', ach.description or '-'),
        ]
        data = [[Paragraph(label, label_style), Paragraph(str(val), body_style)] for label, val in rows]
        tbl = Table(data, colWidths=[avail_width * 0.22, avail_width * 0.78])
        tbl.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (0, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, grid_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        block.append(tbl)

        # 证明材料（嵌入证书图片）
        image_flowables = []
        for att in ach.attachments:
            ext = os.path.splitext(att.file_path or '')[1].lower()
            if ext not in ('.png', '.jpg', '.jpeg', '.gif'):
                continue
            disk_path = _resolve_attachment_disk_path(att.file_path)
            if not disk_path or not os.path.exists(disk_path):
                continue
            try:
                with PILImage.open(disk_path) as im:
                    iw, ih = im.size
                max_w = avail_width * 0.62
                max_h = 150 * mm
                ratio = min(max_w / iw, max_h / ih, 1.0)
                image_flowables.append(Image(disk_path, width=iw * ratio, height=ih * ratio))
            except Exception as e:
                print(f"嵌入证明材料图片失败 (attachment={att.id}): {e}")
                continue

        block.append(Spacer(1, 6))
        if image_flowables:
            block.append(Paragraph('证明材料：', label_style))
            for img in image_flowables:
                block.append(img)
                block.append(Spacer(1, 4))
        else:
            block.append(Paragraph('证明材料：无', small_grey))

        # 标题+表格保持在一页，图片自然流动
        story.append(KeepTogether(block[:2]))
        for f in block[2:]:
            story.append(f)
        story.append(Spacer(1, 14))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


@export_bp.route('/certificates', methods=['POST'])
@jwt_required()
def export_certificates():
    """导出获奖证书汇总 PDF（接收选中的成果ID列表）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'student':
            return jsonify({'error': '仅学生可导出获奖证书汇总'}), 403

        student = current_user.student
        if not student:
            return jsonify({'error': '学生信息不存在'}), 404

        data = request.get_json() or {}
        achievement_ids = data.get('achievement_ids', [])
        if not achievement_ids:
            return jsonify({'error': '请至少选择一项成果'}), 400

        # 仅导出该学生本人且已通过的成果
        achievements = Achievement.query.filter(
            Achievement.id.in_(achievement_ids),
            Achievement.student_id == student.id,
            Achievement.status == 'approved'
        ).order_by(Achievement.achieved_date.desc()).all()

        if not achievements:
            return jsonify({'error': '没有可导出的已通过成果'}), 400

        pdf_bytes = generate_certificates_pdf(current_user, student, achievements)

        filename = f"获奖证书汇总_{student.student_no or student.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/student/export/certificates 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导出失败: {str(e)}'}), 500


# ==================== 教师端：导出所授课程学生的获奖证书 ====================

teacher_export_bp = Blueprint('teacher_export', __name__, url_prefix='/api/teacher/export')


def _teacher_managed_students(teacher):
    """教师所授课程中的学生"""
    course_ids = [c.id for c in Course.query.filter(Course.teacher_id == teacher.id).all()]
    if not course_ids:
        return []
    student_ids = [cs.student_id for cs in CourseStudent.query.filter(CourseStudent.course_id.in_(course_ids)).all()]
    if not student_ids:
        return []
    return Student.query.filter(Student.id.in_(student_ids)).all()


def _teacher_student_ids(teacher):
    return [s.id for s in _teacher_managed_students(teacher)]


@teacher_export_bp.route('/award-types', methods=['GET'])
@jwt_required()
def teacher_export_award_types():
    """奖项类型一级分类（中文名 + 存储码），供教师端导出筛选下拉使用"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        # 奖项类型配置中的一级分类（中文名）
        rows = AchievementKnowledge.query.with_entities(
            AchievementKnowledge.category
        ).filter(AchievementKnowledge.category.isnot(None)).distinct().all()

        reverse = {v: k for k, v in MAIN_CATEGORY_MAP.items()}
        seen = set()
        options = []
        for (name,) in rows:
            name = (name or '').strip()
            if not name or name in seen:
                continue
            seen.add(name)
            # code 为数据库存储的一级分类英文码；配置中未收录的分类回退用中文名
            code = reverse.get(name, name)
            options.append({'code': code, 'name': name})

        options.sort(key=lambda x: x['name'])
        return jsonify({'categories': options}), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teacher/export/award-types 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'加载奖项类型失败: {str(e)}'}), 500


@teacher_export_bp.route('/students', methods=['GET'])
@jwt_required()
def teacher_export_students():
    """列出该教师所授课程的全部学生（含成果数），支持按审核时间/分类/级别/学号筛选"""
    try:
        from sqlalchemy import func
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'teacher' or not current_user.teacher:
            return jsonify({'error': '仅教师可查看学生列表'}), 403

        teacher = current_user.teacher
        all_students = _teacher_managed_students(teacher)
        if not all_students:
            return jsonify({'students': []}), 200

        # 读取查询参数
        student_no = (request.args.get('student_no') or '').strip()
        category = (request.args.get('category') or '').strip()
        level = (request.args.get('level') or '').strip()
        start_date = (request.args.get('start_date') or '').strip()
        end_date = (request.args.get('end_date') or '').strip()

        has_achievement_filter = bool(category or level or start_date or end_date)

        # 按学号模糊筛选学生
        students = all_students
        if student_no:
            students = [s for s in all_students if student_no in (s.student_no or '')]

        if not students:
            return jsonify({'students': []}), 200

        # 构建成果查询（所授课程学生 + 已通过 + 过滤条件）
        student_ids = [s.id for s in students]
        ach_query = Achievement.query.filter(
            Achievement.student_id.in_(student_ids),
            Achievement.status == 'approved'
        )
        if category:
            ach_query = ach_query.filter(Achievement.main_category == category)
        if level:
            ach_query = ach_query.filter(Achievement.level == level)
        if start_date:
            ach_query = ach_query.filter(func.date(Achievement.reviewed_at) >= start_date)
        if end_date:
            ach_query = ach_query.filter(func.date(Achievement.reviewed_at) <= end_date)

        from collections import defaultdict
        counts = defaultdict(int)
        for (sid,) in ach_query.with_entities(Achievement.student_id).all():
            counts[sid] += 1

        items = []
        for stu in students:
            count = counts.get(stu.id, 0)
            # 存在成果类过滤条件时，仅保留有符合条件的成果的学生
            if has_achievement_filter and count == 0:
                continue
            items.append({
                'student_id': stu.id,
                'student_no': stu.student_no or '',
                'name': (stu.user.name if stu.user else ''),
                'class_name': (stu.class_name() or ''),
                'achievement_count': count
            })

        items.sort(key=lambda s: (s['class_name'] or '', s['student_no'] or ''))
        return jsonify({'students': items}), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teacher/export/students 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'加载学生列表失败: {str(e)}'}), 500


@teacher_export_bp.route('/student/certificates', methods=['POST'])
@jwt_required()
def teacher_export_student_certificates():
    """导出指定学生的获奖证书汇总 PDF（复用学生端单学生导出逻辑）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'teacher' or not current_user.teacher:
            return jsonify({'error': '仅教师可导出学生成果'}), 403

        teacher = current_user.teacher
        data = request.get_json() or {}
        student_id = data.get('student_id')
        if not student_id:
            return jsonify({'error': '缺少学生信息'}), 400

        # 校验该学生属于教师所授课程
        student_ids = _teacher_student_ids(teacher)
        if not student_ids or student_id not in student_ids:
            return jsonify({'error': '该学生不属于您所授课程'}), 403

        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404

        achievements = Achievement.query.filter(
            Achievement.student_id == student_id,
            Achievement.status == 'approved'
        ).order_by(Achievement.achieved_date.desc()).all()

        if not achievements:
            return jsonify({'error': '该学生暂无已通过成果'}), 400

        pdf_bytes = generate_certificates_pdf(student.user, student, achievements)

        filename = f"获奖证书汇总_{student.student_no or student.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/teacher/export/student/certificates 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导出失败: {str(e)}'}), 500


@teacher_export_bp.route('/student/<int:student_id>/achievements', methods=['GET'])
@jwt_required()
def teacher_export_student_achievements(student_id):
    """列出指定学生的全部已通过成果（供单项导出弹窗展示）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'teacher' or not current_user.teacher:
            return jsonify({'error': '仅教师可查看学生成果'}), 403

        teacher = current_user.teacher
        student_ids = _teacher_student_ids(teacher)
        if not student_ids or student_id not in student_ids:
            return jsonify({'error': '该学生不属于您所授课程'}), 403

        achievements = Achievement.query.filter(
            Achievement.student_id == student_id,
            Achievement.status == 'approved'
        ).order_by(Achievement.achieved_date.desc()).all()

        student = achievements[0].student if achievements else Student.query.get(student_id)
        items = [{
            'achievement_id': a.id,
            'title': a.title or '',
            'main_category': get_main_category_label(a.main_category),
            'sub_category': get_sub_category_label(a.sub_category),
            'level': get_level_label(a.level),
            'achieved_date': a.achieved_date.strftime('%Y-%m-%d') if a.achieved_date else '',
            'reviewed_at': a.reviewed_at.strftime('%Y-%m-%d %H:%M') if a.reviewed_at else ''
        } for a in achievements]

        return jsonify({
            'student_id': student_id,
            'student_no': (student.student_no if student else ''),
            'name': (student.user.name if student and student.user else ''),
            'class_name': (student.class_name() if student else ''),
            'achievements': items
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/teacher/export/student/<id>/achievements 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'加载学生成果失败: {str(e)}'}), 500


@teacher_export_bp.route('/student/achievement', methods=['POST'])
@jwt_required()
def teacher_export_single_achievement():
    """导出该学生单条已通过成果的 PDF"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': '用户不存在'}), 404
        if current_user.role != 'teacher' or not current_user.teacher:
            return jsonify({'error': '仅教师可导出学生成果'}), 403

        teacher = current_user.teacher
        data = request.get_json() or {}
        achievement_id = data.get('achievement_id')
        if not achievement_id:
            return jsonify({'error': '缺少成果信息'}), 400

        achievement = Achievement.query.filter(
            Achievement.id == achievement_id,
            Achievement.status == 'approved'
        ).first()
        if not achievement:
            return jsonify({'error': '成果不存在或未通过审核'}), 400

        student = achievement.student
        student_ids = _teacher_student_ids(teacher)
        if not student or not student_ids or student.id not in student_ids:
            return jsonify({'error': '该成果不属于您所授课程的学生'}), 403

        pdf_bytes = generate_certificates_pdf(student.user, student, [achievement])

        filename = f"获奖证书_{achievement.title or achievement.id}_{student.student_no or student.id}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/teacher/export/student/achievement 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导出失败: {str(e)}'}), 500
