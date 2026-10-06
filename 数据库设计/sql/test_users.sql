USE achievement_db;

INSERT INTO users (username, password_hash, role, name, email, created_at) VALUES
('head_li', 'pbkdf2:sha256:600000$aXwswVWb3wg4d9O0$abc42e5cced5d03482a09f0f7cd381302acb8981ef1328512718f7f7e366347e', 'teacher', '李院长', 'head_li@school.edu.cn', NOW()),
('advisor_wang', 'pbkdf2:sha256:600000$aXwswVWb3wg4d9O0$abc42e5cced5d03482a09f0f7cd381302acb8981ef1328512718f7f7e366347e', 'teacher', '王辅导员', 'advisor_wang@school.edu.cn', NOW()),
('teacher_zhou', 'pbkdf2:sha256:600000$aXwswVWb3wg4d9O0$abc42e5cced5d03482a09f0f7cd381302acb8981ef1328512718f7f7e366347e', 'teacher', '周教师', 'teacher_zhou@school.edu.cn', NOW()),
('admin_zhang', 'pbkdf2:sha256:600000$aXwswVWb3wg4d9O0$abc42e5cced5d03482a09f0f7cd381302acb8981ef1328512718f7f7e366347e', 'teacher', '张教务', 'admin_zhang@school.edu.cn', NOW())
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash), 
    role = VALUES(role), 
    name = VALUES(name), 
    email = VALUES(email);

INSERT INTO teachers (user_id, teacher_no, department, title, phone, role, department_id) VALUES
((SELECT id FROM users WHERE username = 'head_li'), 'H001', '计算机学院', '院长', '13800138001', 'head', 1),
((SELECT id FROM users WHERE username = 'advisor_wang'), 'A001', '计算机学院', '辅导员', '13800138002', 'advisor', 1),
((SELECT id FROM users WHERE username = 'teacher_zhou'), 'T001', '计算机学院', '讲师', '13800138003', 'faculty', 1),
((SELECT id FROM users WHERE username = 'admin_zhang'), 'TA001', '教务处', '教务管理员', '13800138004', 'teaching_admin', 0)
ON DUPLICATE KEY UPDATE 
    teacher_no = VALUES(teacher_no), 
    department = VALUES(department), 
    title = VALUES(title), 
    phone = VALUES(phone), 
    role = VALUES(role), 
    department_id = VALUES(department_id);

SELECT '测试账号插入完成' AS result;