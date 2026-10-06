from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, KnowledgeBase, Achievement
from extensions import db
from datetime import datetime
from constants import (
    get_main_category_label, get_sub_category_label, get_level_label
)
from routes.achievements import build_auditor_display
import os
import io

knowledge_base_bp = Blueprint('knowledge_base', __name__, url_prefix='/api/knowledge-base')


@knowledge_base_bp.route('/', methods=['GET'])
@jwt_required()
def get_knowledge_base():
    """获取知识库列表（支持分页、筛选）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问知识库'}), 403

        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        title = request.args.get('title')
        student_name = request.args.get('student_name')
        category_level1 = request.args.get('category_level1')
        category_level2 = request.args.get('category_level2')
        level = request.args.get('level')

        query = KnowledgeBase.query

        if title:
            query = query.filter(KnowledgeBase.title.like(f'%{title}%'))

        if student_name:
            query = query.filter(KnowledgeBase.student_name.like(f'%{student_name}%'))

        if category_level1:
            query = query.filter(KnowledgeBase.category_level1 == category_level1)

        if category_level2:
            query = query.filter(KnowledgeBase.category_level2 == category_level2)

        if level:
            query = query.filter(KnowledgeBase.level == level)

        query = query.order_by(KnowledgeBase.created_at.desc())
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        return jsonify({
            'knowledge_base': [item.to_dict() for item in pagination.items],
            'pagination': {
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page,
                'per_page': pagination.per_page
            }
        }), 200

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/knowledge-base/ 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'获取知识库失败: {str(e)}'}), 500


@knowledge_base_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_knowledge_base_detail(id):
    """获取单条知识库详情"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权访问知识库'}), 403

        knowledge = KnowledgeBase.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识库记录不存在'}), 404

        return jsonify({
            'knowledge': knowledge.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取知识库详情失败: {str(e)}'}), 500


@knowledge_base_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_knowledge_base(id):
    """编辑知识库成果"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权编辑知识库'}), 403

        knowledge = KnowledgeBase.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识库记录不存在'}), 404

        data = request.get_json()

        if 'title' in data:
            knowledge.title = data['title']
        if 'category_level1' in data:
            knowledge.category_level1 = data['category_level1']
        if 'category_level2' in data:
            knowledge.category_level2 = data['category_level2']
        if 'level' in data:
            knowledge.level = data['level']
        if 'description' in data:
            knowledge.description = data['description']
        if 'proof_material' in data:
            knowledge.proof_material = data['proof_material']

        knowledge.updated_at = datetime.now()

        db.session.commit()

        return jsonify({
            'message': '知识库记录更新成功',
            'knowledge': knowledge.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== PUT /api/knowledge-base/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'更新知识库失败: {str(e)}'}), 500


@knowledge_base_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge_base(id):
    """删除知识库成果"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权删除知识库'}), 403

        knowledge = KnowledgeBase.query.get(id)
        if not knowledge:
            return jsonify({'error': '知识库记录不存在'}), 404

        if knowledge.proof_material:
            backup_path = knowledge.proof_material
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except Exception as e:
                    print(f"删除备份文件失败: {e}")

        db.session.delete(knowledge)
        db.session.commit()

        return jsonify({'message': '知识库记录删除成功'}), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"\n=== DELETE /api/knowledge-base/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'删除知识库失败: {str(e)}'}), 500


def generate_knowledge_base_pdf(knowledge_items, doc_title='成果知识库汇总'):
    """生成成果知识库汇总 PDF（reportlab + 中文 CID 字体）

    字段：序号、成果标题、学生姓名、班级、一级分类、二级细分、级别、
          描述、证明材料（嵌入图片）、状态、审核人（含团队信息）、
          审核时间、审核意见、提交时间
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, KeepTogether
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
        title='成果知识库汇总'
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

    # 预加载来源成果，用于构造"审核人（含团队信息）"
    source_ids = [item.source_achievement_id for item in knowledge_items if item.source_achievement_id]
    source_map = {}
    if source_ids:
        source_achievements = Achievement.query.filter(Achievement.id.in_(source_ids)).all()
        source_map = {ach.id: ach for ach in source_achievements}

    story = []

    # 封面标题区
    story.append(Paragraph(doc_title, title_style))
    story.append(Paragraph(
        f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}　　共 {len(knowledge_items)} 项已通过成果",
        subtitle_style))
    story.append(Spacer(1, 10))

    for idx, item in enumerate(knowledge_items, 1):
        block = []
        block.append(Paragraph(f"{idx}. {item.title or ''}", section_style))

        # 构造审核人显示文本：姓名（院系/科组）
        auditor_display = item.auditor_name or ''
        source_ach = source_map.get(item.source_achievement_id) if item.source_achievement_id else None
        if source_ach:
            display = build_auditor_display(source_ach)
            if display:
                auditor_display = display

        def _fmt_dt(dt):
            return dt.strftime('%Y-%m-%d %H:%M') if dt else '-'

        rows = [
            ('学生姓名', item.student_name or '-'),
            ('班级', item.class_name or '-'),
            ('一级分类', get_main_category_label(item.category_level1) or '-'),
            ('二级细分', get_sub_category_label(item.category_level2) if item.category_level2 else '-'),
            ('级别', get_level_label(item.level) or '-'),
            ('状态', '已通过'),
            ('审核人', auditor_display or '-'),
            ('审核时间', _fmt_dt(item.reviewed_at)),
            ('审核意见', item.audit_comment or '-'),
            ('提交时间', _fmt_dt(item.submitted_at)),
            ('成果描述', item.description or '-'),
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
        # proof_material 存储的是逗号分隔的磁盘绝对路径
        image_flowables = []
        if item.proof_material:
            for path in item.proof_material.split(','):
                path = path.strip()
                if not path:
                    continue
                ext = os.path.splitext(path)[1].lower()
                if ext not in ('.png', '.jpg', '.jpeg', '.gif'):
                    continue
                if not os.path.exists(path):
                    continue
                try:
                    with PILImage.open(path) as im:
                        iw, ih = im.size
                    max_w = avail_width * 0.62
                    max_h = 150 * mm
                    ratio = min(max_w / iw, max_h / ih, 1.0)
                    image_flowables.append(Image(path, width=iw * ratio, height=ih * ratio))
                except Exception as e:
                    print(f"嵌入证明材料图片失败 (knowledge={item.id}): {e}")
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


@knowledge_base_bp.route('/export', methods=['POST'])
@jwt_required()
def export_knowledge_base():
    """导出成果知识库汇总 PDF（管理员）"""
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权导出知识库'}), 403

        # 支持按选中 id 列表导出：body 传 {"id": [1,2,3]} 时只导出选中项，否则导出全部已通过
        ids = None
        raw = request.get_json(silent=True) or {}
        if raw.get('id'):
            try:
                ids = [int(x) for x in raw['id']]
            except (TypeError, ValueError):
                ids = None

        query = KnowledgeBase.query.filter(KnowledgeBase.status == 'approved')
        if ids:
            query = query.filter(KnowledgeBase.id.in_(ids))
        knowledge_items = query.order_by(KnowledgeBase.created_at.desc()).all()

        if not knowledge_items:
            return jsonify({'error': '当前知识库为空，无可导出成果'}), 400

        pdf_bytes = generate_knowledge_base_pdf(knowledge_items)

        filename = f"成果知识库汇总_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print(f"\n=== POST /api/knowledge-base/export 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导出失败: {str(e)}'}), 500


@knowledge_base_bp.route('/export/<int:id>', methods=['GET'])
@jwt_required()
def export_knowledge_base_one(id):
    """导出单条知识库成果 PDF（管理员）"""
    import re
    try:
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': '用户不存在'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': '无权导出知识库'}), 403

        item = KnowledgeBase.query.get(id)
        if not item:
            return jsonify({'error': '知识库记录不存在'}), 404

        pdf_bytes = generate_knowledge_base_pdf([item], doc_title='成果详情')

        # 文件名：成果_<成果标题>_<学生姓名>.pdf（去除文件名非法字符）
        def _safe_name(s):
            return re.sub(r'[\\/:*?"<>|]', '_', s or '').strip() or '-'
        filename = f"成果_{_safe_name(item.title)}_{_safe_name(item.student_name)}.pdf"

        return send_file(
            io.BytesIO(pdf_bytes),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        print(f"\n=== GET /api/knowledge-base/export/{id} 错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'导出失败: {str(e)}'}), 500


def add_to_knowledge_base(achievement):
    """将审核通过的成果添加到知识库"""
    try:
        existing = KnowledgeBase.query.filter_by(source_achievement_id=achievement.id).first()
        if existing:
            return

        from app import app

        proof_material = ''
        if achievement.attachments:
            backup_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'knowledge-base')
            os.makedirs(backup_dir, exist_ok=True)

            backup_paths = []
            for attachment in achievement.attachments:
                if attachment.file_path and os.path.exists(attachment.file_path):
                    filename = os.path.basename(attachment.file_path)
                    backup_path = os.path.join(backup_dir, f"{achievement.id}_{filename}")
                    try:
                        import shutil
                        shutil.copy2(attachment.file_path, backup_path)
                        backup_paths.append(backup_path)
                    except Exception as e:
                        print(f"备份文件失败: {e}")

            if backup_paths:
                proof_material = ','.join(backup_paths)

        student_name = achievement.student.user.name if achievement.student and achievement.student.user else ''
        class_name = achievement.student.class_name() if achievement.student else ''
        auditor_name = achievement.auditor.user.name if achievement.auditor and achievement.auditor.user else ''

        knowledge = KnowledgeBase(
            source_achievement_id=achievement.id,
            title=achievement.title,
            category_level1=achievement.main_category,
            category_level2=achievement.sub_category,
            level=achievement.level,
            student_name=student_name,
            class_name=class_name,
            description=achievement.description,
            proof_material=proof_material,
            auditor_name=auditor_name,
            audit_comment=achievement.review_comment,
            submitted_at=achievement.submitted_at,
            reviewed_at=achievement.reviewed_at
        )

        db.session.add(knowledge)
        db.session.commit()

        print(f"成果 {achievement.id} 已成功录入知识库")

    except Exception as e:
        import traceback
        print(f"\n=== 添加成果到知识库错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误堆栈: {traceback.format_exc()}")
