---
title: CHATSAM - ChatGPT2API with Data Persistence
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

<h1 align="center">CHATSAM - ChatGPT2API</h1>

<p align="center">一键部署到 HuggingFace Spaces，支持数据持久化 + 防止休眠</p>

<p align="center">
  <a href="#一键部署">🚀 一键部署</a> •
  <a href="#数据持久化">📦 数据持久化</a> •
  <a href="#防止休眠">⚡ 防止休眠</a> •
  <a href="#功能特性">✨ 功能特性</a>
</p>

---

## 🚀 一键部署到 HuggingFace

### 步骤 1：创建 HuggingFace Space

1. 登录 [HuggingFace](https://huggingface.co)
2. 点击右上角 **"Create Space"**
3. 填写信息：
   - **Space name**: 你的项目名称（如 `my-chatsam`）
   - **SDK**: 选择 **Docker**
   - **Hardware**: 选择 **CPU basic**（免费）
4. 点击 **"Create Space"**

### 步骤 2：克隆此项目并推送

```bash
# 克隆此项目
git clone https://github.com/chanzsam/CHATSAM.git
cd CHATSAM

# 添加 HuggingFace 远程仓库
git remote add hf https://huggingface.co/spaces/<你的用户名>/<你的space名称>

# 推送到 HuggingFace
git push hf main
```

### 步骤 3：配置管理员密码

在 Space 的 **Settings → Variables and secrets** 中添加：

| Secret 名称 | Secret 值 |
|------------|-----------|
| `CHATGPT2API_AUTH_KEY` | `你的管理员密码` |

---

## 📦 数据持久化（防止数据丢失）

HuggingFace Spaces 默认使用临时存储，重启后数据会丢失。配置 Git 存储后端可以永久保存数据。

### 配置步骤

#### 1. 创建 GitHub 数据存储仓库

1. 在 GitHub 创建一个新的**私有仓库**（如 `my-chatsam-data`）
2. 初始化仓库，添加空的 JSON 文件：

```json
{
  "items": []
}
```

文件名：
- `accounts.json`
- `auth_keys.json`

#### 2. 配置 HuggingFace Secrets

在 Space 的 **Settings → Variables and secrets** 中添加：

| Secret 名称 | Secret 值 |
|------------|-----------|
| `STORAGE_BACKEND` | `git` |
| `GIT_REPO_URL` | `https://github.com/<你的用户名>/<数据仓库名>.git` |
| `GIT_TOKEN` | `你的 GitHub Personal Access Token` |

#### 3. 创建 GitHub Token

1. 访问 [GitHub Token 设置](https://github.com/settings/tokens)
2. 点击 **"Generate new token (classic)"**
3. 选择权限：`repo`（完整仓库访问）
4. 复制生成的 Token

#### 4. 重启 Space

添加 Secrets 后，点击 **"Factory reboot"** 重启 Space。

---

## ⚡ 防止休眠（24小时在线）

HuggingFace Spaces 免费 48 小时无访问会自动休眠。使用 GitHub Actions 可以保持在线。

### 配置步骤

#### 1. Fork 此项目到你的 GitHub

#### 2. 启用 GitHub Actions

访问你的仓库 **Settings → Actions → General**，选择：
- **Allow all actions and reusable workflows**

#### 3. 配置保活 Workflow

项目已内置 `.github/workflows/keep-alive.yml`：

```yaml
name: Keep HuggingFace Space Alive

on:
  schedule:
    - cron: '0 */12 * * *'  # 每12小时ping一次
  workflow_dispatch:         # 支持手动触发

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping HuggingFace Space
        run: |
          curl -s https://huggingface.co/spaces/<你的用户名>/<你的space名称>
```

#### 4. 修改 Space 地址

编辑 `.github/workflows/keep-alive.yml`，将 URL 改为你的 Space 地址。

---

## ✨ 功能特性

### API 兼容能力

- 兼容 `POST /v1/images/generations` 图片生成接口
- 兼容 `POST /v1/images/edits` 图片编辑接口
- 兼容面向图片场景的 `POST /v1/chat/completions`
- 兼容面向图片场景的 `POST /v1/responses`
- `GET /v1/models` 返回可用模型列表

### 在线画图功能

- 内置在线画图工作台
- 支持 `gpt-image-2`、`codex-gpt-image-2`、`auto` 等模型
- 编辑模式支持参考图上传
- 本地保存图片会话历史

### 号池管理功能

- 自动刷新账号邮箱、类型、额度
- 轮询可用账号执行图片生成
- 自动剔除无效 Token
- 支持多种导入方式

### 数据持久化

- 支持 Git 仓库存储
- 支持 PostgreSQL 存储
- 支持 SQLite 存储
- 配置、账号、用户数据永久保存

---

## 📋 部署清单

| 配置项 | 说明 | 必需 |
|--------|------|------|
| `CHATGPT2API_AUTH_KEY` | 管理员密码 | ✅ 必需 |
| `STORAGE_BACKEND` | 存储后端类型 | 推荐 |
| `GIT_REPO_URL` | Git 数据仓库地址 | 推荐 |
| `GIT_TOKEN` | GitHub Token | 推荐 |

---

## 🔧 本地开发

### Docker 运行

```bash
docker compose up -d
```

### 本地开发

```bash
# 后端
uv sync
uv run main.py

# 前端
cd web
bun install
bun run dev
```

---

## ⚠️ 免责声明

> 本项目涉及对 ChatGPT 官网相关能力的逆向研究，仅供个人学习、技术研究与非商业性技术交流使用。
>
> - 严禁用于任何商业用途
> - 严禁用于违反 OpenAI 服务条款的行为
> - 使用者应自行承担全部风险

---

## 📄 License

MIT License

---

## 🙏 致谢

基于 [basketikun/chatgpt2api](https://github.com/basketikun/chatgpt2api) 项目