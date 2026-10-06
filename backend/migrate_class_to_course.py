"""
一次性迁移脚本：班级(classes) 并入 课程(courses)。
- 给 courses 增加 is_locked 列
- 把每个 class 转成一条 course，学生经 course_students 关联
- 保留 classes / class_applications / students.class_id 结构（供未来复用），仅停止使用
幂等：可重复执行，重复执行无副作用。
"""
import pymysql

DB = dict(host='localhost', user='root', password='cyc13729243361',
          database='achievement_db', charset='utf8mb4')


def conn_open():
    return pymysql.connect(**DB)


def column_exists(cur, table, col):
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
        (table, col))
    return cur.fetchone()[0] > 0


def migrate():
    conn = conn_open()
    cur = conn.cursor()

    # 1) 幂等标记表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS migration_class_to_course (
            class_id VARCHAR(20) PRIMARY KEY,
            course_id INT UNIQUE NOT NULL,
            migrated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2) courses.is_locked
    if not column_exists(cur, 'courses', 'is_locked'):
        cur.execute("ALTER TABLE courses ADD COLUMN is_locked TINYINT NOT NULL DEFAULT 0 AFTER student_count")

    # 3) 班级 -> 课程
    cur.execute("SELECT id, name, advisor_id, grade, student_count, is_locked, created_at FROM classes ORDER BY id")
    classes = cur.fetchall()
    migrated = 0
    for cid, name, teacher_id, grade, student_count, is_locked, created_at in classes:
        cur.execute("SELECT course_id FROM migration_class_to_course WHERE class_id=%s", (cid,))
        if cur.fetchone():
            continue  # 已迁移，跳过

        # 生成唯一 code
        base = cid
        code = base
        suffix = 2
        while True:
            cur.execute("SELECT id FROM courses WHERE code=%s", (code,))
            if cur.fetchone() is None:
                break
            code = '%s#%s' % (base, suffix)
            suffix += 1

        semester = ('%s级' % grade) if grade else None
        description = '由原班级[%s]迁移' % cid
        cur.execute("""
            INSERT INTO courses (name, code, invite_code, teacher_id, type, description,
                                 max_students, student_count, semester, created_at, is_locked)
            VALUES (%s, %s, NULL, %s, 'regular', %s, NULL, %s, %s, %s, %s)
        """, (name, code, teacher_id, description, student_count, semester, created_at, 1 if is_locked else 0))
        course_id = cur.lastrowid
        cur.execute("INSERT INTO migration_class_to_course (class_id, course_id) VALUES (%s, %s)", (cid, course_id))
        migrated += 1

    # 4) 学生 -> course_students
    cur.execute("""
        INSERT IGNORE INTO course_students (course_id, student_id, is_starred, joined_at)
        SELECT m.course_id, s.id, 0, NOW()
        FROM students s
        JOIN migration_class_to_course m ON s.class_id = m.class_id
    """)

    # 5) 重算 student_count
    cur.execute("""
        UPDATE courses c
        SET c.student_count = (SELECT COUNT(*) FROM course_students cs WHERE cs.course_id = c.id)
        WHERE c.id IN (SELECT course_id FROM migration_class_to_course)
    """)

    conn.commit()

    # 汇总
    cur.execute("SELECT COUNT(*) FROM courses WHERE id IN (SELECT course_id FROM migration_class_to_course)")
    course_n = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM course_students WHERE course_id IN (SELECT course_id FROM migration_class_to_course)")
    link_n = cur.fetchone()[0]
    print('完成。迁移班级 -> 课程: %d 条；关联选课学生: %d 条' % (course_n, link_n))
    cur.execute("SHOW COLUMNS FROM courses LIKE 'is_locked'")
    print('courses.is_locked 列:', '存在' if cur.fetchone() else '缺失')
    conn.close()


if __name__ == '__main__':
    migrate()