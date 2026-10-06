@echo off
REM ============================================================
REM  数据库每日自动备份 - 任务计划程序导入脚本
REM  功能：每天凌晨 2:00 执行 backup/backup.py 生成数据库备份，
REM        备份脚本会自动清理 30 天前的备份文件。
REM  用法：以管理员身份运行本脚本（右键 -> 以管理员身份运行）
REM ============================================================

REM Python 可执行文件（如已加入 PATH，可保持默认 python）
set PYTHON=python

REM 项目后端目录（请按实际路径修改）
set BACKEND_DIR=D:\成果云\backend

REM 备份脚本完整路径
set BACKUP_SCRIPT=%BACKEND_DIR%\backup\backup.py

REM 任务名称
set TASK_NAME=成果云数据库每日备份

REM 创建计划任务：每天 02:00 执行
schtasks /Create /TN "%TASK_NAME%" /TR "\"%PYTHON%\" \"%BACKUP_SCRIPT%\"" /SC DAILY /ST 02:00 /F

if %errorlevel% equ 0 (
    echo.
    echo [成功] 已创建每日 02:00 的备份计划任务，任务名：%TASK_NAME%
    echo [说明] 备份文件将生成于：%BACKEND_DIR%\backup\，30 天前备份自动删除
    echo [手动] 可运行：python "%BACKUP_SCRIPT%"
    echo [移除] 可用：schtasks /Delete /TN "%TASK_NAME%" /F
) else (
    echo.
    echo [失败] 创建计划任务出错，请确认已以管理员身份运行本脚本。
)
pause