# Apache Doris 交互式学习平台

本项目基于 Docker Compose，包含以下服务：

- **mysql**：MySQL 开发环境实例（端口 3306）
- **backend**：Node.js + Express API 服务，处理 SQL 执行与 Explain
- **frontend**：React + Vite 前端应用，提供学习路径、架构动画、在线 SQL 练习与可视化执行计划

## 快速启动

```bash
cd doris-learning-platform
docker-compose up --build
```

- 前端访问：http://localhost:3500
- 后端接口：http://localhost:5000/api/sql

## 项目结构

```
├── backend
├── frontend
└── docker-compose.yml
```
