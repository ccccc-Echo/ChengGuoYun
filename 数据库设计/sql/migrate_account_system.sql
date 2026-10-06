-- ============================================
-- 成果云系统 - 账号体系重构迁移脚本
-- 执行顺序：1.ALTER TABLE -> 2.UPDATE -> 3.INSERT -> 4.验证
-- ============================================

USE achievement_db;

-- ============================================
-- 第一步：新增字段
-- ============================================

-- 为 teachers 表添加 advisor_id 字段（教师所属辅导员）
ALTER TABLE teachers ADD COLUMN IF NOT EXISTS advisor_id INT AFTER department_id;

-- ============================================
-- 第二步：更新 users 表 - 教师账号重命名
-- ============================================

-- 院系负责人: head_li -> h001
UPDATE users SET username = 'h001' WHERE username = 'head_li';

-- 辅导员: advisor_wang -> a001
UPDATE users SET username = 'a001' WHERE username = 'advisor_wang';

-- 教师: teacher_zhou -> t001
UPDATE users SET username = 't001' WHERE username = 'teacher_zhou';

-- ============================================
-- 第三步：更新 students 表 - 学生账号重命名
-- ============================================

-- 更新学生学号
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
-- 第四步：更新 teachers 表 - 教师编号和角色
-- ============================================

-- 更新教师编号（与用户名一致）
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
-- 第五步：新增教师账号（a002 - 陈辅导员, t002 - 孙教师）
-- ============================================

-- 密码统一为 123456 的哈希值
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
-- 第六步：建立师生对应关系
-- ============================================

-- 设置教师的所属辅导员
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
-- 第七步：更新学生班级分配
-- ============================================

-- 确保班级表存在对应班级
-- 班级1: 2024CS01 (王辅导员管理)
INSERT INTO classes (id, name, department, advisor_id, grade)
SELECT '2024CS01', '2024级计算机1班', '计算机学院', t.id, 2024
FROM teachers t JOIN users u ON t.user_id = u.id WHERE u.username = 'a001'
ON DUPLICATE KEY UPDATE name = VALUES(name), advisor_id = VALUES(advisor_id);

-- 班级2: 2024CS02 (陈辅导员管理)
INSERT INTO classes (id, name, department, advisor_id, grade)
SELECT '2024CS02', '2024级计算机2班', '计算机学院', t.id, 2024
FROM teachers t JOIN users u ON t.user_id = u.id WHERE u.username = 'a002'
ON DUPLICATE KEY UPDATE name = VALUES(name), advisor_id = VALUES(advisor_id);

-- 分配学生到班级1 (a001管理的学生)
UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.class_id = '2024CS01'
WHERE u.username IN ('s001', 's002', 's003');

-- 分配学生到班级2 (a002管理的学生)
UPDATE students s
JOIN users u ON s.user_id = u.id
SET s.class_id = '2024CS02'
WHERE u.username IN ('s004', 's005', 'zhangsan', 'test001');

-- ============================================
-- 第八步：更新成果表中的教师关联
-- ============================================

-- 更新成果表中的 teacher_id 关联（确保教师ID正确）
-- 此步骤可选，如果之前的成果已经正确关联则不需要

-- ============================================
-- 验证查询
-- ============================================

-- 1. 查询所有教师账号
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

-- 2. 查询所有学生账号及其班级
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

-- 3. 查询辅导员-教师-学生对应关系
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
JOIN teachers t_advisor ON t_faculty.advisor_id = t_advisor.id
JOIN users advisor ON t_advisor.user_id = advisor.id
LEFT JOIN classes c ON c.advisor_id = t_advisor.id
LEFT JOIN students s ON s.class_id = c.id
LEFT JOIN users student ON s.user_id = student.id
WHERE t_faculty.role = 'faculty'
ORDER BY advisor.username, faculty.username, s.student_no;

-- 4. 查询各角色人数统计
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

-- ============================================
-- 完成
-- ============================================
-- 执行完毕后请验证以上查询结果是否符合预期
-- ============================================