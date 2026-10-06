# 成果云系统 - 前端

基于 Vue 3 + Vite + Element Plus + ECharts 开发的成果云系统前端。

## 技术栈

- Vue 3 - 渐进式 JavaScript 框架
- Vite - 新一代前端构建工具
- Element Plus - 基于 Vue 3 的组件库
- Vue Router - Vue.js 官方路由管理器
- Axios - HTTP 客户端
- ECharts - 可视化图表库
- js-cookie - Cookie 操作库

## 功能特性

### 角色权限
- **管理员**：全部权限，查看全院数据
- **辅导员**：管理本班学生成果、查看班级报表
- **学生**：查看个人档案、录入成果

### 页面功能

#### 登录页
- 用户名密码登录
- 登录成功后根据角色跳转不同页面

#### 仪表盘
- 统计卡片（总成果数、待审核数、班级数、学生数）
- ECharts 图表（成果类型分布、成果级别分布）
- 待审核成果列表

#### 成果管理
- 成果列表（支持按班级/类型/状态筛选）
- 成果详情查看
- 成果审核（通过/驳回）
- 成果删除

#### 录入成果
- 成果表单（标题、类型、级别、日期、描述）
- 附件上传（支持拖拽上传）
- 表单验证

#### 班级管理
- 班级列表（支持筛选）
- 班级详情查看
- 关联学生和成果

#### 学生管理
- 学生列表（支持筛选）
- 学生详情查看
- 关联成果

#### 统计报表
- ECharts 图表展示
  - 成果类型分布（饼图）
  - 成果级别分布（饼图）
  - 成果状态分布（饼图）
  - 班级成果排名（条形图）
  - 成果趋势分析（折线图）

## 项目结构

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   └── index.js              # API 接口封装
│   ├── assets/
│   ├── components/
│   ├── layout/
│   │   └── index.vue             # 布局组件
│   ├── router/
│   │   └── index.js              # 路由配置
│   ├── utils/
│   │   ├── auth.js               # 认证工具
│   │   └── request.js            # HTTP 请求封装
│   ├── views/
│   │   ├── achievements/
│   │   │   ├── index.vue         # 成果管理
│   │   │   └── add.vue           # 录入成果
│   │   ├── classes/
│   │   │   └── index.vue         # 班级管理
│   │   ├── dashboard/
│   │   │   └── index.vue         # 仪表盘
│   │   ├── login/
│   │   │   └── index.vue         # 登录页
│   │   ├── stats/
│   │   │   └── index.vue         # 统计报表
│   │   └── students/
│   │       └── index.vue         # 学生管理
│   ├── App.vue                   # 根组件
│   └── main.js                   # 入口文件
├── index.html
├── jsconfig.json
├── package.json
├── vite.config.js
└── README.md
```

## 安装依赖

```bash
npm install
```

## 启动开发服务器

```bash
npm run dev
```

开发服务器将在 `http://localhost:3000` 启动。

## 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 `dist/` 目录。

## 预览生产版本

```bash
npm run preview
```

## 环境变量

项目通过 `vite.config.js` 配置代理转发 API 请求：

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false
    }
  }
}
```

## 默认账号

- 管理员：`admin` / `123456`

## 开发注意事项

1. 确保 API 服务器正常运行在 `http://localhost:5000`
2. 登录后 token 存储在 Cookie 中，用户信息存储在 localStorage 中
3. 所有 API 请求都会自动携带 token
4. 图表组件需要等待 DOM 渲染完成后才能初始化
5. 使用 ECharts 时需要处理窗口大小变化事件

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## License

MIT