-- ============================================
-- 成果云系统 - 成果分类体系迁移脚本
-- 将单级分类(category)改为两级分类(main_category + sub_category)
-- ============================================

SET NAMES utf8mb4;
USE achievement_db;

-- ============================================
-- 第一步：查看当前数据状态
-- ============================================

SELECT '=== 当前成果分类统计 ===' AS info;
SELECT category, COUNT(*) AS count FROM achievements GROUP BY category;

-- ============================================
-- 第二步：添加新字段
-- ============================================

-- 添加一级分类和二级细分字段
ALTER TABLE achievements ADD COLUMN main_category VARCHAR(50) NOT NULL DEFAULT '' COMMENT '一级分类';
ALTER TABLE achievements ADD COLUMN sub_category VARCHAR(50) NULL COMMENT '二级细分';

-- ============================================
-- 第三步：数据迁移（将旧分类映射到新的两级分类）
-- ============================================

-- 学术论文类
UPDATE achievements 
SET main_category = '学科竞赛类', sub_category = '其他'
WHERE category = 'competition';

-- 学术论文类
UPDATE achievements 
SET main_category = '学术论文类', sub_category = '普通期刊'
WHERE category = 'academic_paper';

-- 知识产权类
UPDATE achievements 
SET main_category = '知识产权类', sub_category = '其他'
WHERE category = 'patent';

-- 科研项目类
UPDATE achievements 
SET main_category = '科研项目类', sub_category = '校级大创'
WHERE category = 'research';

-- 荣誉表彰类（创新创业）
UPDATE achievements 
SET main_category = '荣誉表彰类', sub_category = '其他'
WHERE category = 'innovation';

-- 社会实践类
UPDATE achievements 
SET main_category = '社会实践类', sub_category = '社会实践'
WHERE category = 'practice';

-- ============================================
-- 第四步：删除旧字段
-- ============================================

ALTER TABLE achievements DROP COLUMN category;

-- ============================================
-- 验证查询
-- ============================================

SELECT '=== 迁移后成果分类统计 ===' AS info;
SELECT main_category, sub_category, COUNT(*) AS count 
FROM achievements 
GROUP BY main_category, sub_category 
ORDER BY main_category, sub_category;

SELECT '=== 迁移完成 ===' AS info;