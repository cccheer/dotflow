# DotFlow 项目架构设计

## 1. 项目目标

DotFlow 是一个面向 Dot. 墨水屏设备的本地优先内容调度与推送平台。

第一版核心目标：

- 管理 Dot 设备信息
- 管理多个服务实例
- 支持 cron 定时执行和手动执行
- 通过插件生成文本内容
- 将内容推送到指定 Dot 设备
- 记录执行日志，便于排障和回溯

第一版优先实现文本推送链路，图片推送仅预留接口。

## 2. 总体分层

### 前端层

职责：

- 提供管理后台界面
- 管理设备、服务实例、执行记录
- 提供手动触发入口

建议技术：

- React
- Vite
- TypeScript

### API 层

职责：

- 暴露 REST API
- 做基础鉴权
- 参数校验
- 返回统一响应结构

第一版使用：

- FastAPI

### 业务服务层

职责：

- 设备同步与设备配置
- 服务实例 CRUD
- 手动执行服务
- 执行日志记录
- 调度注册和更新

说明：

API 路由不直接写复杂业务逻辑，统一下沉到 service 层。

### 调度层

职责：

- 管理 cron 任务
- 在指定时间触发服务执行

第一版使用：

- APScheduler

说明：

调度器只负责触发，不承担具体生成和推送逻辑。

### 插件层

职责：

- 按统一接口生成文本内容
- 隔离不同业务服务类型

统一接口：

- `validate_config(config)`
- `generate(config) -> { title, message, signature }`

第一版插件：

- `coffee_random`
- `dinner_random`
- `custom_text`
- `webhook_text`

### Dot API Client 层

职责：

- 隔离 Dot 平台接口调用
- 管理鉴权、超时和请求封装
- 提供设备列表、设备状态、文本推送、图片推送接口

说明：

第一版已支持 mock 模式，便于在未接入真实 Dot API 时先跑通主流程。

### 存储层

职责：

- 保存设备信息
- 保存服务实例配置
- 保存作业执行日志

第一版使用：

- SQLite

## 3. 核心执行链路

### 设备同步链路

1. 管理员调用设备同步接口
2. 后端通过 Dot client 拉取设备列表
3. 将设备同步到本地 SQLite
4. 前端展示并允许补充配置，如 `text_task_key`

### 手动执行链路

1. 管理员手动执行某个服务实例
2. 后端读取服务配置和目标设备
3. 插件生成文本内容
4. 执行服务组装请求 payload
5. Dot client 调用文本推送接口
6. 结果写入 jobs 日志

### 定时执行链路

1. 服务实例配置 cron
2. APScheduler 注册定时任务
3. 到点后触发统一执行入口
4. 后续流程与手动执行一致

## 4. 数据模型

### devices

- `id`
- `name`
- `api_base_url`
- `text_task_key`
- `image_task_key`
- `default_content_type`
- `created_at`
- `updated_at`

### services

- `id`
- `name`
- `type`
- `enabled`
- `schedule`
- `device_id`
- `config`
- `created_at`
- `updated_at`

### jobs

- `id`
- `service_id`
- `device_id`
- `trigger_type`
- `run_at`
- `status`
- `request_payload`
- `response_payload`
- `output`
- `error`

## 5. 第一版实现原则

- 先打通文本推送主链路，不提前扩展复杂图片能力
- Dot API 调用必须独立封装
- 调度逻辑与 API 路由分离
- 插件生成逻辑与推送逻辑分离
- 配置和密钥通过环境变量管理
- 所有关键执行结果写入 jobs，便于排障
