-- 成果知识库表
CREATE TABLE IF NOT EXISTS achievement_knowledge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '成果名称',
    category VARCHAR(50) NOT NULL COMMENT '一级分类：学科竞赛类/学术论文类/知识产权类/科研项目类/荣誉表彰类/技能证书类/社会实践类',
    sub_category VARCHAR(100) COMMENT '二级分类',
    level VARCHAR(20) NOT NULL COMMENT '级别：国家级/省级/校级',
    level_priority INT DEFAULT 0 COMMENT '级别权重，用于排序',
    keywords TEXT COMMENT '关键词，逗号分隔',
    proof_required TEXT COMMENT '所需证明材料说明',
    school_id INT DEFAULT 0 COMMENT '学校ID，预留',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_level (level),
    INDEX idx_school_id (school_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成果知识库';

-- 证明材料要求表
CREATE TABLE IF NOT EXISTS proof_requirements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50) NOT NULL COMMENT '一级分类',
    sub_category VARCHAR(100) COMMENT '二级分类',
    proof_type VARCHAR(100) NOT NULL COMMENT '证明材料类型：证书照片/论文封面/录用通知/授权书/截图等',
    is_required TINYINT(1) DEFAULT 1 COMMENT '是否必传',
    description TEXT COMMENT '说明',
    INDEX idx_category_sub (category, sub_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证明材料要求';

-- 班级申请表
CREATE TABLE IF NOT EXISTS class_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL COMMENT '申请人',
    class_id VARCHAR(20) NOT NULL COMMENT '申请的班级',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态：pending/approved/rejected',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    processed_by INT COMMENT '处理人',
    INDEX idx_student_id (student_id),
    INDEX idx_class_id (class_id),
    INDEX idx_status (status),
    CONSTRAINT fk_class_app_student FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    CONSTRAINT fk_class_app_class FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    CONSTRAINT fk_class_app_processed FOREIGN KEY (processed_by) REFERENCES teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级申请表';

-- 教师表扩展字段
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'faculty' COMMENT '角色：head/advisor/faculty/teaching_admin';
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS department_id INT DEFAULT 0 COMMENT '所属院系ID';

-- 教师表索引
ALTER TABLE teachers ADD INDEX IF NOT EXISTS idx_role (role);
ALTER TABLE teachers ADD INDEX IF NOT EXISTS idx_department_id (department_id);