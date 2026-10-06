# 成果云系统 - Flask 后端

## 项目介绍

成果云系统后端 API，提供用户认证、成果管理、统计分析等功能。

## 技术栈

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- Flask-CORS 4.0.0
- MySQL 8.0+

## 项目结构

```
backend/
├── app.py                 # Flask 应用主文件
├── config.py              # 配置管理
├── extensions.py          # 扩展初始化
├── models.py              # 数据模型
├── auth.py                # 认证相关路由
├── achievement.py         # 成果管理路由
├── stats.py               # 统计分析路由
├── requirements.txt       # Python 依赖
├── .env.example           # 环境变量示例
└── README.md             # 项目说明
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
cd backend

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，配置数据库信息
DB_HOST=localhost
DB_PORT=3306
DB_NAME=achievement_db
DB_USER=root
DB_PASSWORD=your_password
```

### 3. 初始化数据库

```bash
# 创建数据库并导入初始数据
mysql -u root -p < ../数据库设计/sql/init_db.sql
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## API 接口说明

### 认证接口 (`/api/auth`)

#### 注册用户（需要管理员权限）
```
POST /api/auth/register
```

请求体：
```json
{
  "username": "student001",
  "password": "123456",
  "role": "student",
  "name": "张三",
  "email": "zhangsan@example.com",
  "student_no": "2024010101",
  "class_id": "2024CS01",
  "major": "计算机科学与技术"
}
```

#### 用户登录
```
POST /api/auth/login
```

请求体：
```json
{
  "username": "student001",
  "password": "123456"
}
```

响应：
```json
{
  "message": "登录成功",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 3,
    "username": "student001",
    "role": "student",
    "name": "张三",
    "student_no": "2024010101",
    "class_id": "2024CS01"
  }
}
```

#### 获取当前用户信息
```
GET /api/auth/me
Headers: Authorization: Bearer <token>
```

### 成果接口 (`/api/achievements`)

#### 获取成果列表
```
GET /api/achievements?page=1&per_page=10&status=pending&type=award
Headers: Authorization: Bearer <token>
```

#### 学生录入成果
```
POST /api/achievements
Headers: Authorization: Bearer <token>
Content-Type: application/json
```

请求体：
```json
{
  "type": "award",
  "title": "ACM竞赛金奖",
  "level": "国际级",
  "achieved_date": "2024-11-15",
  "description": "在ACM国际大学生程序设计竞赛中获得金奖",
  "attachments": [
    {
      "file_name": "证书.pdf",
      "file_path": "/uploads/achievements/2024/01/cert.pdf",
      "file_size": 1024000,
      "file_type": "application/pdf"
    }
  ]
}
```

#### 获取成果详情
```
GET /api/achievements/<id>
Headers: Authorization: Bearer <token>
```

#### 辅导员审核成果
```
PUT /api/achievements/<id>/review
Headers: Authorization: Bearer <token>
Content-Type: application/json
```

请求体：
```json
{
  "status": "approved",
  "review_comment": "表现优异，予以通过"
}
```

#### 删除成果
```
DELETE /api/achievements/<id>
Headers: Authorization: Bearer <token>
```

### 统计接口 (`/api/stats`)

#### 获取班级成果统计
```
GET /api/stats/class?class_id=2024CS01
Headers: Authorization: Bearer <token>
```

响应：
```json
{
  "class_stats": [
    {
      "class_id": "2024CS01",
      "class_name": "计算机科学与技术2024级1班",
      "grade": 2024,
      "total_achievements": 8,
      "approved_count": 6,
      "pending_count": 2,
      "rejected_count": 0
    }
  ]
}
```

#### 获取全院统计（仅管理员）
```
GET /api/stats/school
Headers: Authorization: Bearer <token>
```

响应：
```json
{
  "school_stats": {
    "total_students": 5,
    "total_classes": 1,
    "total_teachers": 1,
    "total_achievements": 8,
    "approved_achievements": 6,
    "pending_achievements": 2,
    "rejected_achievements": 0,
    "by_type": {
      "award": 3,
      "cert": 2,
      "paper": 2,
      "patent": 1
    },
    "by_level": {
      "校级": 2,
      "省级": 3,
      "国家级": 2,
      "国际级": 1
    }
  }
}
```

#### 获取趋势分析（仅管理员）
```
GET /api/stats/trend?months=12
Headers: Authorization: Bearer <token>
```

## 权限说明

| 角色 | 权限范围 |
|------|----------|
| 学生 | 查看/操作自己的成果，删除待审核成果 |
| 辅导员 | 查看/审核本班学生成果，查看班级统计 |
| 管理员 | 查看所有数据，注册用户，查看全院统计和趋势分析 |

## 默认账号

- **管理员**: `admin` / `123456`
- **辅导员**: `t001` / `123456`
- **学生**: `s001` ~ `s005` / `123456`

## 错误处理

API 使用标准 HTTP 状态码：
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权（token 无效或过期）
- `403` - 禁止访问（权限不足）
- `404` - 资源不存在
- `500` - 服务器内部错误

错误响应格式：
```json
{
  "error": "错误描述信息"
}
```

## 开发建议

1. 使用 Postman 或类似工具测试 API
2. 在生产环境中修改 `.env` 中的密钥配置
3. 定期备份数据库
4. 为文件上传功能配置合适的存储路径和权限

## 常见问题

### 数据库连接失败
检查 `.env` 文件中的数据库配置是否正确，确保 MySQL 服务正在运行。

### Token 过期
Token 有效期为 1 天，过期后需要重新登录。

### 文件上传失败
检查上传目录权限，确保 Flask 进程有写入权限。

## 许可证

MIT License