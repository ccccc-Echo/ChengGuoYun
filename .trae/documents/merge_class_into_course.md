# 合并方案：班级并入课程（删除班级，全系统统一为课程）

## Context（背景）

管理员「班级管理」页把**班级**和**课程**两类混在同一个列表，班级行有「锁定/解锁」，课程行却没有。用户创建的 `22222` 实际存储在 `courses` 表，因此始终看不到锁定按钮。

已确认方向：**班级并入课程**——删除独立班级体系，全系统统一为「课程」（课程已具备扫码加课、邀请码加课、教师建课），并把锁定能力移到**课程**上。现有班级和其学生迁移为课程+选课关系。

**补充要求（本次已纳入）**
1. 彻底清理：所有不再使用的 class 相关代码一律删除/改写为 courses/注释掉，保证代码库无残留。
2. 未来会接入其他学校教育系统，届时会新建「学生自动加入、教师自动匹配」的班级功能，与现有 class 有差异。**因此凡可能被未来复用的 class 代码，优先“注释掉”而非删除**，相关 DB 表结构保留以备复用。

最终态：功能层面只有课程；代码层面旧 class 代码被迁移改写或注释保留；现有班级及其学生迁移为课程+选课关系；课程有 `is_locked`；管理员页改为课程管理并支持锁定。

---

## 阶段 A：数据库迁移（新增 `backend/migrate_class_to_course.py`，幂等可回滚）

1. 建映射表 `migration_class_to_course(class_id VARCHAR(20) PK, course_id INT UNIQUE, migrated_at)` 作为幂等标记（不随功能下线而删除）。
2. `ALTER TABLE courses ADD COLUMN is_locked TINYINT NOT NULL DEFAULT 0;`（先查列是否存在）。
3. 遍历 `classes` 每行 → 插入一条课程：`name=class.name`、`teacher_id=class.advisor_id`、`type='regular'`、`student_count`、`semester=CONCAT(grade,'级')`、`is_locked=class.is_locked`；`code` 唯一（分类 id 无冲突直接用 `class.id`，否则追加 `#2/#3…`）；`invite_code=NULL`；写入映射表，已存在的跳过。
4. 关联学生：`INSERT IGNORE INTO course_students(course_id, student_id,...) SELECT course_id,s.id ... FROM students s WHERE s.class_id=映射.class_id;`
5. 重算 `courses.student_count`。
6. **保留 DB 结构（供未来复用）**：不删除 `classes` 表、`students.class_id` 列、`class_applications` 表——仅停止使用。迁移的数据已落到课程侧，旧结构留作未来「学生自动加入/教师自动匹配」班级功能的底子。

---

## 阶段 B：后端改造

**原则**：功能上删掉 class；代码上“改成课程”优先，确属未来可复用的 class 代码整体**注释保留**（不删除，避免未来重写）。

1. **models.py**
   - `Course` 加 `is_locked` 列 + `to_dict()` 返回 `is_locked`。
   - `Student` 移除 `class_info` 关系的使用，新增从第一条 `CourseStudent.course.name` 派生 `class_name` 的助手；`to_dict()` 保留 `class_id`/`class_name` 键（值改课程派生，保证前端 JSON 契约稳定），`class_info` 关系改为注释保留。
   - `Class`、`ClassApplication`、`Teacher.classes_advised`：**注释保留**整块（未来复用），并从当前运行链路中移除引用。
2. **routes/permissions.py**：分组「班级管理」→「课程管理」，`class:*`→`course:create/edit/delete/lock`；`DEFAULT_ROLES` 内 `class:*` 换 `course:*`。
3. **routes/classes.py**：文件**整体注释保留**（未来复用），并从 `app.py` 移除 `class_bp` 注册（`app.py` 中导入/注册改成注释）。
4. **routes/courses.py**
   - 移除 `Class` 运行期引用；`get_course_students` 的 `class_name` 改课程派生。
   - 新增 `PUT /<int:course_id>/lock`（切换/指定 `is_locked`）。
   - 编辑守卫：`is_locked` 时禁改名称；删除守卫：`is_locked` 返回 400，文案 班级→课程。
   - 新增管理员列表 `GET /`（分页/名称筛选，返回 `{courses:[], pagination:{}}`，含 `is_locked`）。教师列表仍走 `/my`。
5. **其余 `Class`/`class_id`/`class_info` 运行引用全部改写为基于 `CourseStudent`**：
   - `routes/students.py`（教师收scope按 `Course.teacher_id`；列表/详情/创建/编辑的班级字段改课程；`class_name` 派生）
   - `routes/achievements.py`（可访问学生范围、`class_id` 筛选、`class_name` 显示、评审人集合改课程教师）
   - `routes/stats.py`（`get_accessible_class_ids`→课程版；`Class`/`Student.class_id`→`CourseStudent`/`Course`；仪表盘班级总数→课程总数）
   - `routes/export.py`（`_teacher_managed_students` 改在其授课程的学生的范围；`class_name` 派生；去掉 `Class` 运行导入）
   - `routes/auth.py`（学生 `class_id`/`class_name` 返回课程派生值）
   - `routes/knowledge_base.py`（`class_name` 改课程派生）
   - 顺带清理开发遗留 `_tmp2.py`/`_tmp3.py`。

---

## 阶段 C：前端改造

1. **api/index.js**：`coursesApi` 增 `adminList(params)`→`GET /courses/`、`lock(id,{is_locked})`→`PUT /courses/{id}/lock`；删除 `classesApi`。
2. **config/permissions.js**：新增 `course:*` 权限常量，移除 `CLASS_*`。
3. **views/classes/index.vue 就地改造为「课程管理」**：权限 `class:*`→`course:*`；`loadClasses` 改调 `coursesApi.adminList`（`res.courses`）；删除 `row.type==='class'` 分支，课程行统一「编辑(`course:edit`)/删除(`course:delete`)/锁定(`course:lock`)」，锁定图标/置灰逻辑沿用，`handleToggleLock` 指向 `/api/courses/{id}/lock`；文案 班级→课程；管理员页改为仅「编辑/删除/锁定」，移除重复「添加课程」（教师经「我的课程」建课）。
4. **views/students/index.vue**：班级筛选项→课程（`coursesApi.adminList`，参数 `course_id`）；展示列改课程名。
5. **layout/index.vue + router/index.js**：菜单/路由标题「班级管理」→「课程管理」、「我的班级」→「我的课程」；`showClassMenu`/路由守卫 `class:*`→`course:*`。
6. **courses/MyClasses.vue / CourseDetail.vue**：`class:create`→`course:create`，文案 班级→课程；扫码/邀请码加课流程不变。
7. 其它页面历史 `class_name` 显示字段（settings/knowledge/export/profile 等）保留为历史文本，不强制改写。

---

## 阶段 D：执行顺序与验证

执行顺序：A（1-5）→ B1→B2→B3→B4→B5→B6（注释清理）→ `python -c "import app"` → C1..C7 → 前端构建。

验证：
1. `cd backend && python -c "import app"` 无报错；`rg "Class|class_id|class_info" backend/routes` 仅存注释或课程派生，无运行期依赖。
2. 迁移脚本重跑幂等（无重复课程/code）。
3. SQL 抽查：迁移课程均有唯一非空 code；`course_students` 关联数 ≥ 原 `students.class_id` 非空数；`courses.is_locked` 存在默认 0；`classes`/`class_applications` 表仍在（备用未删）。
4. 后端重启后 `init_default_roles()` 应用 `course:*` 权限。
5. 前端构建（`C:\Users\陈乙慈\Downloads` 下 `npm.cmd`）成功，无 `classesApi`/`CLASS_*` 未解析引用。
6. 手工验收：
   - 管理员「课程管理」列表显示课程（含迁移旧班级与 `22222`）且有锁定按钮；锁定后不可改名/删除（前后端均拦截）。
   - 教师「我的课程」QR/邀请码加课正常；迁移旧班级以其原负责教师显示为课程。
   - 学生扫码/邀请码加课正常；迁移学生的选课关系在 `GET /api/courses/{id}/students` 可见。

## 风险提示
- `Class`/`ClassApplication`/`classes.py`/`Student.class_info` 采用“注释保留”以兼顾未来复用，需确保被注释引用不造成导入错误（同步注释 `app.py`、model 引用等）。
- `Student.to_dict()` 保留 `class_id`/`class_name` 键并返回课程派生值，避免 auth/多前端字段约定整体变更。
- 「班级申请」流程（`/apply`、`/applications`）随 `ClassApplication` 注释下线，学生加入统一走课程扫码/邀请码。