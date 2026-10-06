-- ============================================
-- 成果云系统 - 账号体系重构迁移脚本（修复版）
-- 执行顺序：1.字符集 -> 2.新增字段 -> 3.清理重复 -> 4.更新 -> 5.新增 -> 6.验证
-- ============================================

-- ============================================
-- 第一步：设置字符集（解决中文乱码）
-- ============================================
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

USE achievement_db;

-- ============================================
-- 第二步：新增缺失字段
-- ============================================

-- 检查并添加 advisor_id 字段
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS advisor_id INT NULL;

-- ============================================
-- 第三步：查看当前数据状态（用于清理重复）
-- ============================================

SELECT '=== 当前用户表状态 ===' AS info;
SELECT id, username, name, role FROM users ORDER BY username;

SELECT '=== 当前教师表状态 ===' AS info;
SELECT id, user_id, teacher_no, role, advisor_id FROM teachers ORDER BY teacher_no;

SELECT '=== 当前学生表状态 ===' AS info;
SELECT id, user_id, student_no, class_id FROM students ORDER BY student_no;

SELECT '=== 当前班级表状态 ===' AS info;
SELECT id, name, department, advisor_id FROM classes ORDER BY id;

-- ============================================
-- 第四步：清理重复数据
-- ============================================

-- 检查是否存在重复的用户名
SELECT username, COUNT(*) AS cnt FROM users GROUP BY username HAVING cnt > 1;

-- 检查是否存在重复的教师编号
SELECT teacher_no, COUNT(*) AS cnt FROM teachers GROUP BY teacher_no HAVING cnt > 1;

-- 如果存在重复，删除旧的冲突记录
-- 注意：请根据上面的查询结果手动确认需要删除的记录

-- ============================================
-- 第五步：更新教师用户名（如果之前执行失败）
-- ============================================

-- 先检查是否已经更新过
SELECT username FROM users WHERE username IN ('head_li', 'advisor_wang', 'teacher_zhou');

-- 更新用户名（仅当旧用户名存在时）
UPDATE users SET username = 'h001' WHERE username = 'head_li';
UPDATE users SET username = 'a001' WHERE username = 'advisor_wang';
UPDATE users SET username = 't001' WHERE username = 'teacher_zhou';

-- ============================================
-- 第六步：更新学生学号
-- ============================================

-- 通过原用户名更新学生学号
UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's001001'
WHERE u.username = 's001';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's001002'
WHERE u.username = 's002';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's001003'
WHERE u.username = 's003';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's002001'
WHERE u.username = 's004';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's002002'
WHERE u.username = 's005';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's002003'
WHERE u.username = 'zhangsan';

UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.student_no = 's002004'
WHERE u.username = 'test001';

-- ============================================
-- 第七步：更新教师编号和角色
-- ============================================

UPDATE teachers t
JOIN users u ON t.user_id = u.id
SET t.teacher_no = 'h001', t.role = 'head'
WHERE u.username = 'h001';

UPDATE teachers t
JOIN users u ON t.user_id = u.id
SET t.teacher_no = 'a001', t.role = 'advisor'
WHERE u.username = 'a001';

UPDATE teachers t
JOIN users u ON t.user_id = u.id
SET t.teacher_no = 't001', t.role = 'faculty'
WHERE u.username = 't001';

UPDATE teachers t
JOIN users u ON t.user_id = u.id
SET t.teacher_no = 'admin_zhang', t.role = 'teaching_admin'
WHERE u.username = 'admin_zhang';

-- ============================================
-- 第八步：创建班级（解决外键约束问题）
-- ============================================

-- 创建班级2024CS01（王辅导员管理）
INSERT IGNORE INTO classes (id, name, department, grade) VALUES 
('2024CS01', '计算机科学与技术2024级1班', '计算机学院', 2024);

-- 创建班级2024CS02（陈辅导员管理）
INSERT IGNORE INTO classes (id, name, department, grade) VALUES 
('2024CS02', '计算机科学与技术2024级2班', '计算机学院', 2024);

-- ============================================
-- 第九步：新增教师账号（a002 - 陈辅导员, t002 - 孙教师）
-- ============================================

SET @default_password = 'pbkdf2:sha256:600000$aXwswVWb3wg4d9O0$abc42e5cced5d03482a09f0f7cd381302acb8981ef1328512718f7f7e366347e';

-- 新增陈辅导员用户
INSERT INTO users (username, password_hash, role, name, email, created_at) VALUES
('a002', @default_password, 'teacher', '陈辅导员', 'a002@school.edu.cn', NOW())
ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email);

-- 新增孙教师用户
INSERT INTO users (username, password_hash, role, name, email, created_at) VALUES
('t002', @default_password, 'teacher', '孙教师', 't002@school.edu.cn', NOW())
ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email);

-- 新增陈辅导员教师记录
INSERT INTO teachers (user_id, teacher_no, department, title, phone, role, department_id)
SELECT id, 'a002', '计算机学院', '辅导员', '13900002001', 'advisor', 1
FROM users WHERE username = 'a002'
ON DUPLICATE KEY UPDATE teacher_no = VALUES(teacher_no), role = VALUES(role);

-- 新增孙教师教师记录
INSERT INTO teachers (user_id, teacher_no, department, title, phone, role, department_id)
SELECT id, 't002', '计算机学院', '讲师', '13900002002', 'faculty', 1
FROM users WHERE username = 't002'
ON DUPLICATE KEY UPDATE teacher_no = VALUES(teacher_no), role = VALUES(role);

-- ============================================
-- 第十步：更新班级的辅导员关联
-- ============================================

-- 更新班级2024CS01的辅导员为a001
UPDATE classes c
JOIN teachers t ON t.teacher_no = 'a001'
SET c.advisor_id = t.id
WHERE c.id = '2024CS01';

-- 更新班级2024CS02的辅导员为a002
UPDATE classes c
JOIN teachers t ON t.teacher_no = 'a002'
SET c.advisor_id = t.id
WHERE c.id = '2024CS02';

-- ============================================
-- 第十一步：更新学生班级分配
-- ============================================

-- 分配学生到班级1（a001管理）
UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.class_id = '2024CS01'
WHERE u.username IN ('s001', 's002', 's003');

-- 分配学生到班级2（a002管理）
UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.class_id = '2024CS02'
WHERE u.username IN ('s004', 's005', 'zhangsan', 'test001');

-- ============================================
-- 第十二步：建立教师-辅导员关联
-- ============================================

-- t001 (周教师) 归属 a001 (王辅导员)
UPDATE teachers t1
JOIN users u1 ON t1.user_id = u1.id
JOIN teachers t2 ON t2.teacher_no = 'a001'
SET t1.advisor_id = t2.id
WHERE u1.username = 't001';

-- t002 (孙教师) 归属 a002 (陈辅导员)
UPDATE teachers t1
JOIN users u1 ON t1.user_id = u1.id
JOIN teachers t2 ON t2.teacher_no = 'a002'
SET t1.advisor_id = t2.id
WHERE u1.username = 't002';

-- ============================================
-- 验证查询
-- ============================================

SELECT '=== 1. 教师账号 ===' AS info;
SELECT 
    u.username, 
    u.name, 
    u.role, 
    t.teacher_no, 
    t.role AS teacher_role,
    t.advisor_id
FROM users u
LEFT JOIN teachers t ON u.id = t.user_id
WHERE u.role = 'teacher'
ORDER BY u.username;

SELECT '=== 2. 学生账号 ===' AS info;
SELECT 
    u.username, 
    u.name, 
    s.student_no, 
    s.class_id, 
    c.name AS class_name,
    c.advisor_id
FROM users u
LEFT JOIN students s ON u.id = s.user_id
LEFT JOIN classes c ON s.class_id = c.id
WHERE u.role = 'student'
ORDER BY s.class_id, s.student_no;

SELECT '=== 3. 辅导员-教师-学生对应关系 ===' AS info;
SELECT 
    advisor.username AS advisor_username,
    advisor.name AS advisor_name,
    faculty.username AS faculty_username,
    faculty.name AS faculty_name,
    student.username AS student_username,
    student.name AS student_name,
    s.student_no,
    c.name AS class_name
FROM teachers t_faculty
JOIN users faculty ON t_faculty.user_id = faculty.id
LEFT JOIN teachers t_advisor ON t_faculty.advisor_id = t_advisor.id
LEFT JOIN users advisor ON t_advisor.user_id = advisor.id
LEFT JOIN classes c ON c.advisor_id = t_advisor.id
LEFT JOIN students s ON s.class_id = c.id
LEFT JOIN users student ON s.user_id = student.id
WHERE t_faculty.role = 'faculty'
ORDER BY advisor.username, faculty.username, s.student_no;

SELECT '=== 4. 各角色人数统计 ===' AS info;
SELECT 
    '教师' AS category,
    u.role,
    COUNT(*) AS count
FROM users u
WHERE u.role = 'teacher'
GROUP BY u.role

UNION ALL

SELECT 
    '学生' AS category,
    u.role,
    COUNT(*) AS count
FROM users u
WHERE u.role = 'student'
GROUP BY u.role;

SELECT '=== 迁移完成 ===' AS info;