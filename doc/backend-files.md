# Backend 文件说明

本文档用于说明第一版 backend scaffold 中各文件的职责和关系。

## 1. 应用入口

### `backend/app/main.py`

作用：

- 创建 FastAPI 应用
- 注册总路由
- 在生命周期中初始化数据库
- 启动和关闭 APScheduler

这是后端应用真正的启动入口。

## 2. core 层

### `backend/app/core/config.py`

作用：

- 定义 `Settings`
- 读取环境变量
- 统一管理数据库、鉴权、Dot API 和调度器相关配置

### `backend/app/core/database.py`

作用：

- 定义 SQLAlchemy `Base`
- 创建 engine 和 session
- 提供 `get_db()`
- 提供 `init_db()`

### `backend/app/core/logging.py`

作用：

- 提供基础日志配置
- 统一日志格式

### `backend/app/core/security.py`

作用：

- 提供管理后台 Bearer Token 校验
- 供 API 路由复用

## 3. api 层

### `backend/app/api/router.py`

作用：

- 汇总并注册所有 route 模块

### `backend/app/api/deps.py`

作用：

- 提供 API 依赖注入类型
- 目前主要是数据库 session 依赖

### `backend/app/api/routes/health.py`

作用：

- 提供健康检查接口

### `backend/app/api/routes/devices.py`

作用：

- 设备列表查询
- Dot 设备同步
- 本地设备配置更新

### `backend/app/api/routes/services.py`

作用：

- 服务实例列表
- 创建服务实例
- 更新服务实例
- 手动执行服务实例

### `backend/app/api/routes/jobs.py`

作用：

- 查询任务执行日志列表

## 4. models 层

### `backend/app/models/device.py`

数据表：`devices`

作用：

- 保存设备基础信息
- 保存 `text_task_key` 和 `image_task_key`
- 保存默认内容类型等设备配置

### `backend/app/models/service.py`

数据表：`services`

作用：

- 保存服务实例定义
- 保存服务类型、启用状态、cron、目标设备和插件配置

### `backend/app/models/job.py`

数据表：`jobs`

作用：

- 保存每次执行记录
- 保存请求体、响应体、插件输出和错误信息

## 5. schemas 层

### `backend/app/schemas/common.py`

作用：

- 定义统一 API 响应结构 `ApiResponse`

### `backend/app/schemas/device.py`

作用：

- 定义设备的读写数据结构

### `backend/app/schemas/service.py`

作用：

- 定义服务实例的创建、更新、读取结构

### `backend/app/schemas/job.py`

作用：

- 定义作业日志的读取结构

## 6. clients 层

### `backend/app/clients/dot_client.py`

作用：

- 封装 Dot 平台接口调用
- 提供设备列表、设备状态、文本推送、图片推送接口
- 支持 `DOT_API_MOCK=true` 的 mock 模式

说明：

当前已具备真实请求入口，但默认建议先用 mock 跑通系统。

## 7. plugins 层

### `backend/app/plugins/base.py`

作用：

- 定义插件统一抽象接口

### `backend/app/plugins/registry.py`

作用：

- 注册和获取插件实例
- 管理已支持的服务类型

### `backend/app/plugins/coffee_random.py`

作用：

- 随机生成咖啡推荐文本

### `backend/app/plugins/dinner_random.py`

作用：

- 随机生成晚餐推荐文本

### `backend/app/plugins/custom_text.py`

作用：

- 根据配置直接生成自定义文本内容

### `backend/app/plugins/webhook_text.py`

作用：

- 预留 webhook 文本服务能力
- 当前先返回 mock 内容

## 8. services 层

### `backend/app/services/device_service.py`

作用：

- 管理设备查询、同步和更新逻辑
- 协调本地设备数据与 Dot 设备数据

### `backend/app/services/service_service.py`

作用：

- 管理服务实例 CRUD 逻辑
- 校验设备存在性
- 校验插件配置
- 在服务变更后同步调度器

### `backend/app/services/job_service.py`

作用：

- 提供作业日志查询能力

### `backend/app/services/execution_service.py`

作用：

- 执行单个服务实例
- 调用插件生成内容
- 组装 Dot 文本推送 payload
- 调用 Dot client
- 写入 jobs 日志

### `backend/app/services/scheduler_service.py`

作用：

- 管理 APScheduler 生命周期
- 根据服务配置注册或更新 cron 任务
- 到时触发统一执行入口

## 9. 当前 scaffold 特点

- 已具备基本启动骨架
- 已具备基础数据模型
- 已具备 API 路由入口
- 已具备插件扩展机制
- 已具备调度器接线
- 已具备 mock Dot client

## 10. 当前已知待补项

- 删除服务实例接口
- 单个资源详情接口
- 更完善的异常处理
- cron 表达式显式校验
- 更完整的 Dot API 错误落库
- 数据迁移机制
- 单元测试和接口测试
