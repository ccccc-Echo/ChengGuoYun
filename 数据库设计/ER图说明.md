# 成果云系统 - 表关系说明 (ER图)

## 一、实体与关系概述

### 1. 实体列表

| 实体名 | 说明 | 主键 |
|--------|------|------|
| users | 用户表 | id |
| students | 学生表 | id |
| teachers | 教师/辅导员表 | id |
| classes | 班级表 | id |
| achievements | 成果表 | id |
| achievement_attachments | 附件表 | id |

### 2. ER关系图（文字版）

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │  teachers   │       │   classes   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │──1:1──│ user_id(FK) │       │ id (PK)     │
│ username    │       │ id (PK)     │──N:1──│ advisor_id  │
│ role        │       │ teacher_no  │       │             │
│ name        │       │ department  │       │             │
└─────────────┘       └─────────────┘       └─────────────┘
       │                                           │
       │ 1:N                                       │ N:1
       ▼                                           │
┌─────────────┐       ┌─────────────┐              │
│  students   │       │achievements │              │
├─────────────┤       ├─────────────┤              │
│ id (PK)     │──1:N──│ student_id  │◄─────────────┘
│ user_id(FK) │       │ teacher_id  │
│ class_id    │       │ id (PK)     │
│ student_no  │       │ type        │
│ major       │       │ level       │
└─────────────┘       │ status      │
                      └─────────────┘
                            │
                            │ 1:N
                            ▼
                   ┌──────────────────┐
                   │achievement_      │
                   │attachments       │
                   ├──────────────────┤
                   │ id (PK)          │
                   │ achievement_id   │
                   │ file_name        │
                   │ file_path        │
                   └──────────────────┘
```

## 二、详细外键关系

### 1. users ↔ students (1:1)
```
users.id ──────────► students.user_id
```
- 说明：一个用户对应一个学生账户
- 约束：ON DELETE CASCADE（用户删除时同步删除学生记录）

### 2. users ↔ teachers (1:1)
```
users.id ──────────► teachers.user_id
```
- 说明：一个用户对应一个教师账户
- 约束：ON DELETE CASCADE

### 3. teachers ↔ classes (1:N)
```
teachers.id ───────► classes.advisor_id
```
- 说明：一个辅导员可以管理多个班级
- 约束：ON DELETE SET NULL（辅导员删除时，班级 advisor_id 置空）

### 4. classes ↔ students (1:N)
```
classes.id ────────► students.class_id
```
- 说明：一个班级包含多名学生
- 约束：ON DELETE SET NULL

### 5. students ↔ achievements (1:N)
```
students.id ───────► achievements.student_id
```
- 说明：一个学生可以有多项成果
- 约束：ON DELETE CASCADE

### 6. teachers ↔ achievements (1:N)
```
teachers.id ───────► achievements.teacher_id
```
- 说明：一个辅导员可以审核多项成果
- 约束：ON DELETE SET NULL（允许成果在辅导员删除后仍保留）

### 7. achievements ↔ achievement_attachments (1:N)
```
achievements.id ───► achievement_attachments.achievement_id
```
- 说明：一项成果可以有多个附件
- 约束：ON DELETE CASCADE

## 三、关系路径说明

### 学生提交成果的完整路径
```
users → students → achievements → achievement_attachments
```

### 辅导员审核成果的完整路径
```
users → teachers → classes → students → achievements
       → achievements (作为审核人)
```

### 院长查看报表的查询路径
```
classes → students → achievements (聚合统计)
```

## 四、关键约束说明

| 约束类型 | 说明 |
|----------|------|
| UNIQUE | username、student_no、teacher_no 全局唯一 |
| NOT NULL | users.role、achievements.type、achievements.level 等必填字段 |
| ENUM | role (student/teacher/admin)、type (award/cert/paper/patent)、status (pending/approved/rejected) |
| DEFAULT | status 默认 pending、created_at/sumitted_at 默认当前时间戳 |
| CASCADE | 用户删除时级联删除学生/教师记录 |
| SET NULL | 辅导员/班级删除时，相关外键置空 |

## 五、索引设计建议

```sql
-- 建议添加的索引
CREATE INDEX idx_students_class_id ON students(class_id);
CREATE INDEX idx_achievements_student_id ON achievements(student_id);
CREATE INDEX idx_achievements_teacher_id ON achievements(teacher_id);
CREATE INDEX idx_achievements_status ON achievements(status);
CREATE INDEX idx_classes_advisor_id ON classes(advisor_id);
```
