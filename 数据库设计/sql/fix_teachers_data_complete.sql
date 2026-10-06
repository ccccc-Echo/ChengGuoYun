-- ============================================
-- 成果云系统 - 教师数据完整修复脚本
-- 执行步骤：1.设置字符集 -> 2.查看当前状态 -> 3.清理数据 -> 4.重新插入 -> 5.建立关联 -> 6.验证
-- ============================================

-- ============================================
-- 第一步：设置字符集（解决中文乱码）
-- ============================================
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

USE achievement_db;

-- ============================================
-- 第二步：查看当前数据状态
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
-- 第三步：清理现有 teachers 表数据
-- ============================================

-- 先检查是否有外键约束关联
SELECT '=== 检查 teachers 表的外键关联 ===' AS info;

-- 检查班级表中的 advisor_id 关联
SELECT '班级表中关联的教师:' AS info;
SELECT c.id, c.name, c.advisor_id FROM classes WHERE advisor_id IS NOT NULL;

-- 检查成果表中的 teacher_id 关联
SELECT '成果表中关联的教师数量:' AS info;
SELECT COUNT(*) AS count FROM achievements WHERE teacher_id IS NOT NULL;

-- 检查班级申请表中的 processed_by 关联
SELECT '班级申请表中关联的教师数量:' AS info;
SELECT COUNT(*) AS count FROM class_applications WHERE processed_by IS NOT NULL;

-- 如果需要，可以先解除外键关联
-- UPDATE classes SET advisor_id = NULL;
-- UPDATE achievements SET teacher_id = NULL;
-- UPDATE class_applications SET processed_by = NULL;

-- 清空 teachers 表
DELETE FROM teachers;

-- ============================================
-- 第四步：重新插入所有教师记录
-- ============================================

INSERT INTO teachers (user_id, teacher_no, department, title, phone, role, department_id) VALUES
((SELECT id FROM users WHERE username = 'h001'), 'h001', '计算机学院', '院长', '13800138001', 'head', 1),
((SELECT id FROM users WHERE username = 'a001'), 'a001', '计算机学院', '辅导员', '13800138002', 'advisor', 1),
((SELECT id FROM users WHERE username = 'a002'), 'a002', '计算机学院', '辅导员', '13800138003', 'advisor', 1),
((SELECT id FROM users WHERE username = 't001'), 't001', '计算机学院', '讲师', '13800138004', 'faculty', 1),
((SELECT id FROM users WHERE username = 't002'), 't002', '计算机学院', '讲师', '13800138005', 'faculty', 1),
((SELECT id FROM users WHERE username = 't003'), 't003', '计算机学院', '讲师', '13800138006', 'faculty', 1),
((SELECT id FROM users WHERE username = 'admin_zhang'), 'admin_zhang', '教务处', '教务管理员', '13800138007', 'teaching_admin', 0);

-- ============================================
-- 第五步：建立教师关联关系
-- ============================================

-- 设置教师的所属辅导员
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

-- t003 归属 a002
UPDATE teachers t1
JOIN teachers t2 ON t2.teacher_no = 'a002'
SET t1.advisor_id = t2.id
WHERE t1.teacher_no = 't003';

-- ============================================
-- 第六步：更新班级辅导员关联
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
SELECT u.username, u.name, t.teacher_no, t.role, t.department, t.advisor_id
FROM users u
JOIN teachers t ON u.id = t.user_id
WHERE u.role = 'teacher'
ORDER BY t.teacher_no;

SELECT '=== 验证：辅导员-教师关联 ===' AS info;
SELECT t1.teacher_no AS faculty_no, t1.name AS faculty_name,
       t2.teacher_no AS advisor_no, t2.name AS advisor_name
FROM teachers t1
LEFT JOIN teachers t2 ON t1.advisor_id = t2.id
WHERE t1.role = 'faculty'
ORDER BY t1.teacher_no;

SELECT '=== 验证：班级辅导员关联 ===' AS info;
SELECT c.id, c.name, t.teacher_no, t.name AS advisor_name
FROM classes c
LEFT JOIN teachers t ON c.advisor_id = t.id
ORDER BY c.id;

SELECT '=== 修复完成 ===' AS info;