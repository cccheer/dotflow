我要开发一个用于 Dot. 墨水屏设备的内容推送平台，请你作为资深全栈工程师，完成系统设计和第一版代码脚手架。

【项目背景】
目标设备使用 Dot. Developer Platform。
设备开放 API 支持：
- GET /api/authV2/open/devices 获取设备列表
- GET /api/authV2/open/device/:id/status 获取设备状态
- POST /api/authV2/open/device/:deviceId/text 推送文本内容
- POST /api/authV2/open/device/:deviceId/image 推送图片内容
鉴权方式为 Authorization: Bearer <API_KEY>。

注意：
- 必须使用新的 authV2 接口，不要使用 legacy endpoint
- 设备在 Dot. App 的 Content Studio 中必须已添加对应的 Text API content 或 Image API content
- 如果设备有多个 API content，需要支持 taskKey
- 第一版优先实现文本推送链路，图片推送能力预留但不优先开发

【项目目标】
构建一个可配置的内容推送平台，包含前端和后端：
1. 前端可管理多个“服务实例”
2. 每个服务实例可配置定时规则（cron）
3. 每个服务实例运行后生成文本内容
4. 后端将内容推送到指定 Dot. 设备
5. 支持手动执行
6. 支持查看执行日志
7. 支持设备同步和设备配置
8. 管理后台需要基础鉴权，不需要多用户系统

【第一版范围】
优先实现：
- 设备同步
- 设备配置（保存 device_id / text_task_key / image_task_key）
- 服务实例 CRUD
- 文本类服务插件机制
- 定时执行
- Dot. Text API 推送
- 执行日志
- Docker 部署

暂不优先实现：
- 图片编辑器
- 多用户权限
- 复杂 AI 图像生成
- 拖拽式页面设计

【推荐技术栈】
- 后端：Python + FastAPI
- 调度：APScheduler
- 存储：SQLite
- 前端：React + Vite
- 部署：Docker + docker-compose

【服务插件机制要求】
每个服务类型实现统一接口：
- validate_config(config)
- generate(config) -> { title, message, signature }

第一版至少实现以下服务类型：
- coffee_random
- dinner_random
- custom_text
- webhook_text

【Dot. 文本推送要求】
统一由 Dot client / Push gateway 调用：
POST /api/authV2/open/device/:deviceId/text

支持字段：
- refreshNow
- title
- message
- signature
- icon
- link
- taskKey

要求：
- 默认 refreshNow=true
- 如果设备配置了 text_task_key，则自动带上
- 对失败请求记录 response payload
- 做基础错误处理和超时处理

【数据模型建议】
devices:
- id
- name
- api_base_url
- text_task_key
- image_task_key
- default_content_type
- created_at
- updated_at

services:
- id
- name
- type
- enabled
- schedule
- device_id
- config (JSON)
- created_at
- updated_at

jobs:
- id
- service_id
- device_id
- trigger_type
- run_at
- status
- request_payload
- response_payload
- output
- error

【前端页面】
第一版包含：
1. Dashboard
2. Devices 页面
3. Services 页面
4. Create/Edit Service 页面
5. Jobs 日志页面

【请输出】
1. 系统架构设计
2. 目录结构
3. 数据模型
4. API 设计
5. 前端页面设计
6. 开发步骤拆解
7. 第一版完整 scaffold 代码
8. Dockerfile 和 docker-compose
9. README

【代码要求】
- 代码必须可运行
- 模块划分清晰
- 方便未来新增服务插件
- Dot API 调用封装独立
- 使用环境变量管理 API_KEY 和管理后台鉴权 token
- 日志和错误处理规范