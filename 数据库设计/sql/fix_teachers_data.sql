-- ============================================
-- 修复 teachers 表数据缺失问题
-- ============================================

SET NAMES utf8mb4;
USE achievement_db;

-- ============================================
-- 第一步：检查当前数据状态
-- ============================================

SELECT '=== 当前 teacher 角色用户 ===' AS info;
SELECT id, username, name, role FROM users WHERE role = 'teacher' ORDER BY username;

SELECT '=== 当前 teachers 表数据 ===' AS info;
SELECT id, user_id, teacher_no, role, department, department_id, advisor_id FROM teachers ORDER BY teacher_no;

SELECT '=== users中有但teachers中缺失的记录 ===' AS info;
SELECT u.id, u.username, u.name
FROM users u
LEFT JOIN teachers t ON u.id = t.user_id
WHERE u.role = 'teacher' AND t.id IS NULL;

-- ============================================
-- 第二步：检查并添加缺失字段
-- ============================================

SELECT '=== teachers 表结构 ===' AS info;
DESC teachers;

-- 如果 advisor_id 字段不存在，添加它
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS advisor_id INT NULL;

-- ============================================
-- 第三步：插入缺失的教师记录
-- ============================================

INSERT INTO teachers (user_id, teacher_no, department, title, phone, role, department_id)
VALUES
((SELECT id FROM users WHERE username = 'h001'), 'h001', '计算机学院', '院长', '13800138001', 'head', 1),
((SELECT id FROM users WHERE username = 'a001'), 'a001', '计算机学院', '辅导员', '13800138002', 'advisor', 1),
((SELECT id FROM users WHERE username = 'a002'), 'a002', '计算机学院', '辅导员', '13800138003', 'advisor', 1),
((SELECT id FROM users WHERE username = 't001'), 't001', '计算机学院', '讲师', '13800138004', 'faculty', 1),
((SELECT id FROM users WHERE username = 't002'), 't002', '计算机学院', '讲师', '13800138005', 'faculty', 1),
((SELECT id FROM users WHERE username = 'admin_zhang'), 'admin_zhang', '教务处', '教务管理员', '13800138006', 'teaching_admin', 0)
ON DUPLICATE KEY UPDATE 
    teacher_no = VALUES(teacher_no), 
    role = VALUES(role),
    department = VALUES(department),
    title = VALUES(title),
    phone = VALUES(phone),
    department_id = VALUES(department_id);

-- ============================================
-- 第四步：建立教师-辅导员关联
-- ============================================

-- t001 归属 a001
UPDATE teachers t1
JOIN teachers t2 ON t2.teacher_no = 'a001'
SET t1.advisor_id = t2.id
WHERE t1.teacher_no = 't001';

-- t002 归属 a002
UPDATE teachers t1
JOIN teachers t2 ON t2.teacher_no = 'a002'
SET t1.advisor_id = t2.id
WHERE t1.teacher_no = 't002';

-- ============================================
-- 第五步：更新班级辅导员关联
-- ============================================

-- 确保班级存在
INSERT IGNORE INTO classes (id, name, department, grade) VALUES 
('2024CS01', '计算机科学与技术2024级1班', '计算机学院', 2024),
('2024CS02', '计算机科学与技术2024级2班', '计算机学院', 2024);

-- 更新班级辅导员
UPDATE classes SET advisor_id = (SELECT id FROM teachers WHERE teacher_no = 'a001') WHERE id = '2024CS01';
UPDATE classes SET advisor_id = (SELECT id FROM teachers WHERE teacher_no = 'a002') WHERE id = '2024CS02';

-- ============================================
-- 验证查询
-- ============================================

SELECT '=== 验证：教师记录完整性 ===' AS info;
SELECT u.username, u.name, t.teacher_no, t.role, t.advisor_id
FROM users u
LEFT JOIN teachers t ON u.id = t.user_id
WHERE u.role = 'teacher'
ORDER BY u.username;

SELECT '=== 验证：班级辅导员关联 ===' AS info;
SELECT c.id, c.name, t.teacher_no, t.name AS advisor_name
FROM classes c
LEFT JOIN teachers t ON c.advisor_id = t.id
ORDER BY c.id;

SELECT '=== 修复完成 ===' AS info;