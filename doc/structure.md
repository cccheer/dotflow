# DotFlow 目录结构说明

## 1. 当前仓库结构

```text
dotflow/
├── AGENTS.md
├── LICENSE
├── project.md
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── clients/
│   │   ├── core/
│   │   ├── models/
│   │   ├── plugins/
│   │   ├── schemas/
│   │   └── services/
│   └── data/
└── doc/
```

## 2. 根目录文件说明

### `AGENTS.md`

项目协作约束文档，定义工作方式、架构规则、代码质量规则和交付要求。

### `project.md`

项目需求说明文档，定义项目背景、功能范围、接口要求、数据模型建议和输出目标。

### `LICENSE`

项目许可证文件。

### `doc/`

项目文档目录，用于存放设计说明和文件说明。

## 3. backend 目录说明

### `backend/.env.example`

环境变量示例文件，约定运行所需的配置项，包括：

- `ADMIN_TOKEN`
- `DATABASE_URL`
- `DOT_API_BASE_URL`
- `DOT_API_KEY`
- `DOT_API_TIMEOUT_SECONDS`
- `DOT_API_MOCK`
- `SCHEDULER_TIMEZONE`

### `backend/requirements.txt`

后端 Python 依赖列表。

### `backend/data/`

用于存放 SQLite 数据文件，便于后续 Docker volume 挂载和本地持久化。

### `backend/app/`

后端应用主目录。

## 4. backend/app 模块边界

### `app/main.py`

应用启动入口，负责：

- 创建 FastAPI 实例
- 挂载路由
- 启动时初始化数据库
- 启动调度器
- 应用关闭时优雅停止调度器

### `app/core/`

核心基础设施层，放应用配置、数据库初始化、日志配置和安全校验。

### `app/api/`

API 层，只处理接口定义、参数收发和依赖注入。

### `app/models/`

数据库模型层，定义 SQLite 中的实体表结构。

### `app/schemas/`

请求和响应数据结构层，负责 API 数据校验和序列化。

### `app/clients/`

第三方接口调用层，目前主要承载 Dot API client。

### `app/plugins/`

服务插件层，负责生成内容，不直接负责推送。

### `app/services/`

业务服务层，负责把模型、插件、第三方调用和调度器串起来。

## 5. 后续建议目录扩展

后续继续开发时，可以逐步补充：

- `frontend/`：React 管理后台
- `docker-compose.yml`：本地编排
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `scripts/`：启动或初始化辅助脚本
- `tests/`：后端接口和业务测试
