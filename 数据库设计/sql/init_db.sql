-- ============================================
-- 成果云系统 数据库初始化脚本
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS achievement_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE achievement_db;

-- ============================================
-- 1. 用户表 (users)
-- ============================================
DROP TABLE IF EXISTS achievement_attachments;
DROP TABLE IF EXISTS achievements;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher', 'admin') NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 2. 教师/辅导员表 (teachers)
-- ============================================
CREATE TABLE teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    teacher_no VARCHAR(20) NOT NULL UNIQUE,
    department VARCHAR(100),
    title VARCHAR(50),
    phone VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3. 班级表 (classes)
-- ============================================
CREATE TABLE classes (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    advisor_id INT,
    grade INT,
    student_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (advisor_id) REFERENCES teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4. 学生表 (students)
-- ============================================
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    student_no VARCHAR(20) NOT NULL UNIQUE,
    class_id VARCHAR(20),
    major VARCHAR(100),
    phone VARCHAR(20),
    avatar VARCHAR(255),
    enrolled_at DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5. 成果表 (achievements)
-- ============================================
CREATE TABLE achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    teacher_id INT,
    category VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    level ENUM('校级', '省级', '国家级', '国际级') NOT NULL,
    achieved_date DATE,
    description TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    review_comment TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 6. 附件表 (achievement_attachments)
-- ============================================
CREATE TABLE achievement_attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    achievement_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 插入初始数据
-- ============================================

-- 创建默认管理员账号 (admin / 123456)
-- 密码使用 BCrypt 加密
INSERT INTO users (username, password_hash, role, name, email) VALUES
('admin', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'admin', '系统管理员', 'admin@school.edu.cn');

-- ============================================
-- 插入示例数据
-- ============================================

-- 1. 创建辅导员用户
INSERT INTO users (username, password_hash, role, name, email) VALUES
('t001', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'teacher', '张老师', 'zhang@school.edu.cn');

-- 2. 创建辅导员记录
INSERT INTO teachers (user_id, teacher_no, department, title, phone) VALUES
(2, 'T2020001', '计算机学院', '讲师', '13800001001');

-- 3. 创建班级
INSERT INTO classes (id, name, department, advisor_id, grade, student_count) VALUES
('2024CS01', '计算机科学与技术2024级1班', '计算机学院', 1, 2024, 5);

-- 4. 创建学生用户
INSERT INTO users (username, password_hash, role, name, email) VALUES
('s001', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'student', '王小明', 's001@school.edu.cn'),
('s002', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'student', '李华', 's002@school.edu.cn'),
('s003', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'student', '赵小红', 's003@school.edu.cn'),
('s004', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'student', '钱伟', 's004@school.edu.cn'),
('s005', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZRGdjGj/n3.Q7VYcWYjtVBfRUk1Oa', 'student', '孙丽', 's005@school.edu.cn');

-- 5. 创建学生记录
INSERT INTO students (user_id, student_no, class_id, major, phone, enrolled_at) VALUES
(3, '2024010101', '2024CS01', '计算机科学与技术', '13900001001', '2024-09-01'),
(4, '2024010102', '2024CS01', '计算机科学与技术', '13900001002', '2024-09-01'),
(5, '2024010103', '2024CS01', '计算机科学与技术', '13900001003', '2024-09-01'),
(6, '2024010104', '2024CS01', '计算机科学与技术', '13900001004', '2024-09-01'),
(7, '2024010105', '2024CS01', '计算机科学与技术', '13900001005', '2024-09-01');

-- 6. 创建成果记录
INSERT INTO achievements (student_id, teacher_id, category, title, level, achieved_date, description, status, review_comment) VALUES
-- 学生1的成果
(1, 1, 'award', 'ACM国际大学生程序设计竞赛金奖', '国际级', '2024-11-15', '在ACM-ICPC国际大学生程序设计竞赛中获得金奖', 'approved', '表现优异，予以通过'),
(1, 1, 'cert', '华为HCIA云计算认证', '国家级', '2024-08-20', '通过华为HCIA云计算认证考试', 'approved', '技能证书有效'),
-- 学生2的成果
(2, 1, 'paper', '基于深度学习的图像识别研究', '省级', '2024-10-01', '在省级期刊发表学术论文', 'approved', '论文质量良好'),
(2, 1, 'patent', '一种图像处理方法及装置', '国家级', '2024-09-15', '已获国家发明专利授权', 'approved', '专利有效'),
-- 学生3的成果
(3, 1, 'cert', '英语六级证书', '校级', '2024-06-15', '大学英语六级考试550分', 'approved', '成绩达标'),
-- 学生4的成果
(4, 1, 'award', '校程序设计大赛一等奖', '校级', '2024-05-20', '在校程序设计大赛中获得一等奖', 'approved', '恭喜获奖'),
-- 学生5的成果 (待审核)
(5, NULL, 'paper', '机器学习在数据分析中的应用', '省级', '2024-12-01', '投稿省级期刊论文', 'pending', NULL),
(5, NULL, 'award', '数学建模竞赛省级一等奖', '省级', '2024-11-10', 'mathorcup数学建模省一等奖', 'pending', NULL);

-- 7. 创建附件记录
INSERT INTO achievement_attachments (achievement_id, file_name, file_path, file_size, file_type) VALUES
(1, 'ACM金奖证书.pdf', '/uploads/achievements/2024/01/cert.pdf', 1024000, 'application/pdf'),
(2, 'HCIA证书.jpg', '/uploads/achievements/2024/02/cert.jpg', 512000, 'image/jpeg'),
(3, '论文录用通知.pdf', '/uploads/achievements/2024/03/paper.pdf', 2048000, 'application/pdf'),
(4, '专利证书.pdf', '/uploads/achievements/2024/04/patent.pdf', 1536000, 'application/pdf');

-- ============================================
-- 验证数据
-- ============================================
SELECT '数据初始化完成!' AS message;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS student_count FROM students;
SELECT COUNT(*) AS achievement_count FROM achievements;