-- ============================================
-- 成果云系统 - 字符集编码修复脚本
-- ============================================

-- 第二步：设置连接字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

-- 第三步：修改数据库默认字符集
ALTER DATABASE achievement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 第四步：修改所有表的字符集
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE students CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE achievements CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE teachers CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE classes CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE achievement_attachments CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE achievement_knowledge CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE class_applications CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE proof_requirements CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 第五步：验证字符集设置
SELECT '=== 修改后的表字符集 ===' AS info;
SHOW CREATE TABLE users;
SHOW CREATE TABLE students;
SHOW CREATE TABLE achievements;

-- 第六步：检查数据是否正常显示
SELECT '=== 用户数据 ===' AS info;
SELECT id, username, name, email FROM users LIMIT 10;

SELECT '=== 学生数据 ===' AS info;
SELECT s.student_no, u.name, s.class_id FROM students s JOIN users u ON s.user_id = u.id LIMIT 10;

SELECT '=== 成果数据 ===' AS info;
SELECT a.title, a.main_category, a.sub_category, a.level, u.name AS student_name 
FROM achievements a 
JOIN students s ON a.student_id = s.id 
JOIN users u ON s.user_id = u.id 
LIMIT 10;

SELECT '=== 修复完成 ===' AS info;