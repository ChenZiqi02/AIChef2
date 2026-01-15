# AIChef 技术架构文档

## 1. 项目概述
**AIChef** 是一个智能菜谱推荐系统，利用 RAG（检索增强生成）技术，将简单的食材清单转化为具有大厨水准的菜谱建议。系统主打“精致餐饮（Fine Dining）”美学，并内置了一位**幽默风趣、具备上下文感知能力的 AI 厨师顾问**。

## 2. 技术栈 (Tech Stack)

### 前端 (Frontend)
- **框架**: React 18 + Vite (TypeScript)
- **样式**: Tailwind CSS v3 (定制 "Stone & Orange" 配色方案) + PostCSS
- **图标库**: Lucide React (专业烹饪图标)
- **状态管理**: React Hooks (`useState`, `useEffect`) + SessionStorage (本地缓存)
- **路由**: React Router DOM v6
- **路由**: React Router DOM v6
- **网络请求**: Axios (封装了自动注入 `X-Username` Header 的拦截器)
- **多用户管理**: React Context API (`UserContext`) 实现全局用户切换

### 后端 (Backend)
- **框架**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy
- **关系型数据库**: SQLite (`data/users.db`) - 用于存储用户信息和偏好
- **服务器**: Uvicorn (ASGI)
- **API 风格**: RESTful JSON API

### AI 与数据 (AI & Data)
- **核心 LLM**: **SiliconFlow / DeepSeek** (通过 OpenAI 兼容接口调用)
  - **模型**: `deepseek-ai/DeepSeek-V3` (或其他兼容模型)
  - **人设**: 幽默、专业、擅长吐槽“黑暗料理”的私家大厨。
- **向量数据库**: ChromaDB (本地持久化存储于 `data/chroma_db_v3`)
- **Embeddings**: HuggingFace Embeddings (`BAAI/bge-small-zh-v1.5`)
- **编排框架**: LangChain (用于 Prompt 管理和流式调用)

## 3. 核心功能特性 (Key Features)

### 3.1 智能检索与去重 (Smart Retrieval & Deduplication)
- **混合检索**: 基于向量相似度（Vector Similarity）检索 Top-K 候选菜谱。
- **智能去重**: 后端集成 `difflib` 算法，在召回阶段自动过滤名称高度相似的重复菜谱（相似度阈值 > 0.8），确保展示结果的多样性。
- **动态扩充**: 自动检索 3 倍于请求数量的候选集，以保证去重后仍能返回足够数量的结果。

### 3.2 上下文感知搜索 (Context-Aware Search)
- **对话驱动刷新**: 用户在聊天框输入的反馈（如“不要辣”、“换个做法”）会被作为 `refinement` 参数传递给后端。
- **Query 优化**: 后端利用 LLM 将“原始查询 + 改进意见”重写为更精准的搜索关键词（例如：把 “土豆” + “不要辣” 优化为 “清淡土豆做法”）。
- **实时更新**: 前端无需刷新页面，聊天互动即可触发列表更新。

### 3.3 交互式 AI 顾问 (Interactive Consultant)
- **个性化点评**: AI 根据当前检索到的菜谱列表生成开场白。
- **黑暗料理过滤**: 对离谱的食材搭配（如“巧克力+蒜”）进行幽默吐槽并拒绝推荐。

### 3.4 个性化用户系统 (User System)
- **多用户支持**: 前端支持用户身份切换 (Dad/Mom/Kid)，通过 `X-Username` 请求头实现上下文隔离。
- **自动注册**: 后端采用“自动推断”机制，如果请求头中的用户不存在，会自动在 SQLite 数据库中创建新用户，无需繁琐注册流程。
- **偏好过滤**: 用户的忌口（如“不吃香菜”）会存储在 `users.db`。检索系统在返回结果前，会读取当前用户的偏好配置，强制过滤掉包含忌口食材的菜谱 (Hard Filter)。
- **收藏夹隔离**: 每个用户的收藏列表 (Favorites) 相互独立，存储时通过 Namespaced Key (e.g. `aichef_favorites_Mom`) 进行物理隔离。

### 3.5 性能优化
- **前端缓存**: 使用 `sessionStorage` 缓存搜索结果，实现详情页返回时的**秒级加载 (Instant Load)**。
- **异步处理**: 后端 API 采用 `async/await`，支持高并发访问。

## 4. 项目结构 (Project Structure)

```
AIChef/
├── app/
│   ├── main.py            # FastAPI 入口与路由定义
│   ├── services.py        # 核心业务逻辑 (去重、AI 交互、搜索优化)
│   ├── models.py          # Pydantic 数据模型定义 (API 接口)
│   └── sql_models.py      # SQLAlchemy 数据库模型 (User 表结构)
├── core/
│   ├── config.py          # 环境变量配置
│   ├── database.py        # SQLite 数据库连接管理
│   ├── generator.py       # LLM 生成逻辑封装
│   ├── retriever.py       # 向量检索核心代码
│   └── ingest.py          # 数据入库脚本
├── data/
│   └── chroma_db_v3/      # 向量数据库文件
├── frontend/
│   ├── src/
│   │   ├── components/    # 可复用 UI 组件
│   │   ├── Home.tsx       # 首页 (着陆页)
│   │   ├── Results.tsx    # 搜索结果页 (含搜索 + AI 聊天逻辑)
│   │   ├── Detail.tsx     # 菜谱详情页
│   │   └── App.tsx        # 路由配置
│   └── ...配置文件...
└── run.py                 # 项目统一启动脚本
```

## 5. 开发工作流与部署 (Workflow & Deployment)
### 快速启动 (Quick Start)
- **Windows 一键启动**: 直接运行根目录下的 `start.bat`。该脚本会自动：
    1. 检查并创建 Python 虚拟环境。
    2. 安装后端依赖 (`requirements.txt`)。
    3. 安装前端依赖 (`npm install`)。
    4. 同时启动后端 (8000) 和前端 (5173)。

### 手动开发
1.  **启动后端**: `python AIChef/run.py`
2.  **启动前端**: 进入 frontend 目录运行 `npm run dev`
3.  **环境配置**: 依赖 `.env` 文件中的 `SILICONFLOW_API_KEY` 等配置。

## 6. 技术路线总结 (Roadmap Summary)
- **阶段一**: 搭建基础 RAG 流程，实现基本的“搜食材 -> 出菜谱”。
- **阶段二**: 优化视觉体验，引入 Fine Dining 设计语言；引入 AI 人设，增加交互趣味性。
- **阶段三 (当前)**: 
    - 强化后端逻辑，增加**去重**与**多轮对话意图理解**。
    - 实现前端与后端的深层联动，让 Chat 不仅仅是聊天，更能直接控制数据展示。
    - **新增**: 引入轻量级用户系统，支持多用户切换与偏好记忆。
