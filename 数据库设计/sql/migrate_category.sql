-- ============================================
-- 数据库迁移脚本：将 achievements 表的 type 字段改为 category
-- ============================================
-- 执行说明：
-- 1. 此脚本用于修复 "Unknown column 'achievements.category'" 错误
-- 2. 将数据库表中的 type 字段重命名为 category
-- 3. 将字段类型从 ENUM 改为 VARCHAR(20)，以支持更多成果类型
-- ============================================

-- 检查当前表结构
-- SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'achievements';

-- 执行字段重命名和类型修改
ALTER TABLE achievements CHANGE COLUMN type category VARCHAR(20) NOT NULL;

-- 验证修改结果
-- SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'achievements' AND COLUMN_NAME = 'category';

-- ============================================
-- 成果类型说明：
-- academic_paper - 学术论文
-- patent - 专利
-- competition - 竞赛获奖
-- research - 科研项目
-- innovation - 创新创业
-- practice - 社会实践
-- ============================================