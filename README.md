---
title: CHATSAM - ChatGPT2API 数据持久化版本
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
  <a href="#-项目说明">📖 项目说明</a> •
  <a href="#-一键部署">🚀 一键部署</a> •
  <a href="#-数据持久化">📦 数据持久化</a> •
  <a href="#-防止休眠">⚡ 防止休眠</a> •
  <a href="#-需要修改的地方">🔧 配置修改</a>
</p>

---

## 📖 项目说明

### 项目来源

本项目基于 **[basketikun/chatgpt2api](https://github.com/basketikun/chatgpt2api)** 进行二次开发和优化。

**原项目功能**：
- ChatGPT 官网图片生成、图片编辑能力的逆向封装
- OpenAI 兼容图片 API / 代理
- 在线画图、号池管理、多种账号导入方式
- Docker 自托管部署能力

**本项目新增功能**：
- ✅ **数据持久化** - 支持 Git 仓库存储，防止数据丢失
- ✅ **防止休眠** - GitHub Actions 自动保活，24小时在线
- ✅ **一键部署** - 完整部署文档，快速部署到 HuggingFace
- ✅ **普通用户额度显示** - 修复普通用户不显示剩余额度的问题

### 致谢

感谢以下项目和开发者：

| 项目/开发者 | 贡献 |
|-------------|------|
| **[basketikun](https://github.com/basketikun)** | 原项目作者，核心功能开发 |
| **[chatgpt2api Contributors](https://github.com/basketikun/chatgpt2api/graphs/contributors)** | 所有贡献者 |
| **[LinuxDO](https://linux.do)** | 社区支持 |

> 如果这个项目对你有帮助，请给原项目 [basketikun/chatgpt2api](https://github.com/basketikun/chatgpt2api) 一个 ⭐ Star！

---

## 🚀 一键部署到 HuggingFace

### 步骤 1：创建 HuggingFace Space

**HuggingFace Spaces** 是 HuggingFace 提供的免费托管平台，可以运行 Docker 容器。

1. 登录 [HuggingFace](https://huggingface.co)
2. 点击右上角 **"Create Space"**（创建空间）
3. 填写信息：
   - **Space name**: 你的项目名称（如 `my-chatsam`）
   - **SDK**: 选择 **Docker**（容器运行环境）
   - **Hardware**: 选择 **CPU basic**（免费，2核CPU，16GB内存）
4. 点击 **"Create Space"**（创建空间）

### 步骤 2：克隆此项目并推送

**克隆** 是从 GitHub 下载项目代码到本地。

```bash
# 克隆此项目（从 GitHub 下载代码）
git clone https://github.com/chanzsam/CHATSAM-Public.git
cd CHATSAM-Public

# 添加 HuggingFace 远程仓库（连接到你的 HF Space）
git remote add hf https://huggingface.co/spaces/<你的HF用户名>/<你的Space名称>

# 推送到 HuggingFace（上传代码到 HF）
git push hf main
```

### 步骤 3：配置管理员密码

**Secrets** 是 HuggingFace 提供的加密存储，用于保存敏感信息（如密码、Token）。

在 Space 的 **Settings → Variables and secrets** 中添加：

| Secret 名称 | Secret 值 | 中文说明 |
|------------|-----------|---------|
| `CHATGPT2API_AUTH_KEY` | `你的管理员密码` | 管理员登录密码，建议使用强密码 |

---

## 📦 数据持久化（防止数据丢失）

### 为什么需要数据持久化？

**HuggingFace Spaces** 使用 **临时存储 (Ephemeral Storage)**：

| 问题 | 原因 | 结果 |
|------|------|------|
| 48小时无访问 | 容器休眠 | 数据丢失 |
| 推送新代码 | 容器重建 | 数据丢失 |
| 资源限制重启 | 内存超限 | 数据丢失 |

**解决方案**：使用 Git 仓库存储后端，数据永久保存！

### 配置步骤

#### 0️⃣ 创建 GitHub Personal Access Token（必需）

**Personal Access Token (PAT)** 是 GitHub 的访问令牌，用于授权第三方应用访问你的仓库。

1. 访问 [GitHub Token 设置](https://github.com/settings/tokens)
2. 点击 **"Generate new token (classic)"**（生成新令牌）
3. 填写信息：
   - **Note**: `CHATSAM Data Storage`（令牌名称）
   - **Expiration**: `No expiration`（永不过期，或选择较长时间）
   - **Select scopes**: 选择 **`repo`**（完整仓库访问权限）
4. 点击 **"Generate token"**（生成令牌）
5. ⚠️ **复制 Token**（只显示一次，请妥善保存）

---

#### 1️⃣ 创建 GitHub 数据存储仓库

**数据仓库** 是专门用于存储项目数据的 GitHub 仓库，建议设置为**私有**。

**方式 A：使用一键脚本（推荐）**

```bash
# 克隆项目
git clone https://github.com/chanzsam/CHATSAM-Public.git
cd CHATSAM-Public

# 安装依赖
pip install requests

# 运行一键脚本
python scripts/create_data_repo.py --token ghp_xxxxxxxxxxxx --repo-name my-chatsam-data
```

**脚本功能**：
- ✅ 自动创建私有仓库
- ✅ 自动创建 `accounts.json` 和 `auth_keys.json` 文件
- ✅ 自动推送到 GitHub
- ✅ 输出配置信息，方便复制到 HuggingFace

**参数说明**：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--token` | GitHub Personal Access Token | 从环境变量 `GITHUB_TOKEN` 读取 |
| `--repo-name` | 仓库名称 | `chatsam-data` |
| `--public` | 创建公开仓库 | 默认私有 |

---

**方式 B：手动创建**

1. 在 GitHub 创建一个新的**私有仓库**（如 `my-chatsam-data`）
2. 在仓库中创建以下文件：

**accounts.json** - 存储账号信息
```json
{
  "items": []
}
```

**auth_keys.json** - 存储用户认证密钥
```json
{
  "items": []
}
```

3. 推送到 GitHub

#### 2️⃣ 配置 HuggingFace Secrets

在 Space 的 **Settings → Variables and secrets** 中添加：

| Secret 名称 | Secret 值 | 中文说明 |
|------------|-----------|---------|
| `STORAGE_BACKEND` | `git` | 存储后端类型，使用 Git 存储 |
| `GIT_REPO_URL` | `https://github.com/<你的用户名>/<数据仓库名>.git` | 数据仓库地址 |
| `GIT_TOKEN` | `ghp_xxxxxxxxxxxx` | GitHub 访问令牌 |

#### 3️⃣ 重启 Space

添加 Secrets 后：
1. 回到 Space 主页
2. 点击右上角 **"⋯"** → **"Factory reboot"**（工厂重启）
3. 等待约 5-10 分钟重新构建

#### 4️⃣ 验证数据持久化

1. 登录你的 Space
2. 添加一个测试用户
3. 检查 GitHub 数据仓库是否有新提交
4. 重启 Space，验证数据是否保留

---

## ⚡ 防止休眠（24小时在线）

### 为什么需要防止休眠？

**HuggingFace Spaces** 免费 48 小时无访问会自动休眠：

| 问题 | 影响 |
|------|------|
| 休眠后冷启动 | 需要 1-3 分钟 |
| 用户体验不佳 | 等待时间长 |

**解决方案**：使用 GitHub Actions 每 12 小时自动访问！

### 配置步骤

#### 1️⃣ Fork 此项目到你的 GitHub

**Fork** 是复制别人的 GitHub 项目到你的账号下。

访问 https://github.com/chanzsam/CHATSAM-Public 并点击 **"Fork"**

#### 2️⃣ 启用 GitHub Actions

**GitHub Actions** 是 GitHub 提供的自动化工作流服务。

1. 进入你的 Fork 仓库
2. 点击 **Settings → Actions → General**
3. 选择 **"Allow all actions and reusable workflows"**（允许所有工作流）
4. 点击 **"Save"**（保存）

#### 3️⃣ 修改保活 Workflow

**Workflow** 是 GitHub Actions 的自动化任务配置文件。

编辑 `.github/workflows/keep-alive.yml`：

```yaml
name: Keep HuggingFace Space Alive  # 工作流名称

on:
  schedule:
    - cron: '0 */12 * * *'  # 每12小时执行一次
  workflow_dispatch:         # 支持手动触发

jobs:
  keep-alive:
    runs-on: ubuntu-latest  # 运行环境
    steps:
      - name: Ping HuggingFace Space  # 步骤名称
        run: |
          # ⚠️ 请修改为你的 Space 地址
          curl -s https://huggingface.co/spaces/<你的HF用户名>/<你的Space名称>
          curl -s https://<你的HF用户名>-<你的Space名称>.hf.space
      - name: Log status  # 记录日志
        run: echo "Keep-alive ping sent at $(date)"
```

**需要修改的地方**：
- `<你的HF用户名>` → 你的 HuggingFace 用户名
- `<你的Space名称>` → 你的 Space 名称

#### 4️⃣ 推送修改

```bash
git add .github/workflows/keep-alive.yml
git commit -m "update: keep-alive workflow URL"
git push
```

#### 5️⃣ 手动测试

1. 进入仓库 **Actions** 页面
2. 点击 **"Keep HuggingFace Space Alive"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 查看运行结果

---

## 🔧 需要修改的地方

### 📋 修改清单

部署前需要修改以下文件：

| 文件路径 | 修改内容 | 是否必需 | 中文说明 |
|---------|---------|---------|---------|
| `.github/workflows/keep-alive.yml` | 修改 HF Space 地址 | ✅ 必需 | 保活工作流配置 |
| `config.json` | 修改管理员密码 | ✅ 必需 | 项目配置文件 |
| HF Secrets | 配置存储后端 | 推荐 | HuggingFace 加密存储 |

---

### 1️⃣ `.github/workflows/keep-alive.yml`

**文件位置**: `.github/workflows/keep-alive.yml`

**文件说明**: GitHub Actions 保活工作流配置文件，用于定时访问 HuggingFace Space 防止休眠。

**需要修改**:

```yaml
# 第 15-16 行，修改为你的 Space 地址
curl -s https://huggingface.co/spaces/<YOUR_HF_USERNAME>/<YOUR_SPACE_NAME>
curl -s https://<YOUR_HF_USERNAME>-<YOUR_SPACE_NAME>.hf.space
```

**示例**:

如果你的 HF 用户名是 `myuser`，Space 名称是 `my-chatsam`：

```yaml
curl -s https://huggingface.co/spaces/myuser/my-chatsam
curl -s https://myuser-my-chatsam.hf.space
```

---

### 2️⃣ `config.json`

**文件位置**: `config.json`

**文件说明**: 项目主配置文件，包含管理员密码、代理设置、备份配置等。

**需要修改**:

```json
{
  "auth-key": "YOUR_SECRET_KEY_HERE"  // ← 修改为你的管理员密码
}
```

**或者使用 Secrets（推荐）**:

在 HF Space Settings 中添加 `CHATGPT2API_AUTH_KEY`，会覆盖 `config.json` 中的设置。

**完整配置说明**:

| 配置项 | 默认值 | 中文说明 |
|--------|-------|---------|
| `auth-key` | `YOUR_SECRET_KEY_HERE` | 管理员登录密码 |
| `refresh_account_interval_minute` | `60` | 账号刷新间隔（分钟） |
| `image_retention_days` | `15` | 图片保留天数 |
| `image_poll_timeout_secs` | `120` | 图片生成超时时间（秒） |
| `auto_remove_rate_limited_accounts` | `false` | 自动移除限速账号 |
| `auto_remove_invalid_accounts` | `true` | 自动移除无效账号 |
| `proxy` | `""` | 代理服务器地址 |
| `base_url` | `""` | API 基础地址 |

---

### 3️⃣ HuggingFace Secrets

**位置**: Space Settings → Variables and secrets

**说明**: HuggingFace 提供的加密存储，用于保存敏感信息。

**需要添加**:

| Secret 名称 | 值示例 | 中文说明 |
|------------|-------|---------|
| `CHATGPT2API_AUTH_KEY` | `MyStrongPassword123!` | 管理员登录密码 |
| `STORAGE_BACKEND` | `git` | 存储后端类型 |
| `GIT_REPO_URL` | `https://github.com/myuser/my-data.git` | 数据仓库地址 |
| `GIT_TOKEN` | `ghp_xxxxxxxxxxxx` | GitHub 访问令牌 |

---

## ✨ 功能特性

### API 兼容能力

| API 接口 | 中文说明 |
|---------|---------|
| `POST /v1/images/generations` | 图片生成接口 |
| `POST /v1/images/edits` | 图片编辑接口 |
| `POST /v1/chat/completions` | 图片场景对话接口 |
| `POST /v1/responses` | 图片场景响应接口 |
| `GET /v1/models` | 获取可用模型列表 |

### 在线画图功能

| 功能 | 中文说明 |
|------|---------|
| 内置在线画图工作台 | 提供可视化界面 |
| 支持 `gpt-image-2` 等模型 | 多种图片生成模型 |
| 编辑模式支持参考图上传 | 可上传图片进行编辑 |
| 本地保存图片会话历史 | 记录生成历史 |

### 号池管理功能

| 功能 | 中文说明 |
|------|---------|
| 自动刷新账号邮箱、类型、额度 | 自动更新账号信息 |
| 轮询可用账号执行图片生成 | 自动选择可用账号 |
| 自动剔除无效 Token | 自动清理无效账号 |
| 支持多种导入方式 | 支持批量导入账号 |

### 数据持久化

| 存储类型 | 中文说明 |
|---------|---------|
| Git 仓库存储 | 数据保存到 GitHub |
| PostgreSQL 存储 | 数据保存到数据库 |
| SQLite 存储 | 数据保存到本地文件 |

---

## 📋 部署清单

| 配置项 | 中文说明 | 是否必需 | 配置方式 |
|--------|---------|---------|---------|
| `CHATGPT2API_AUTH_KEY` | 管理员密码 | ✅ 必需 | HF Secrets |
| `STORAGE_BACKEND` | 存储后端类型 | 推荐 | HF Secrets |
| `GIT_REPO_URL` | Git 数据仓库地址 | 推荐 | HF Secrets |
| `GIT_TOKEN` | GitHub 访问令牌 | 推荐 | HF Secrets |
| `keep-alive.yml` | 保活 URL | ✅ 必需 | 修改文件 |

---

## 🔧 本地开发

### Docker 运行

**Docker** 是容器化运行环境，可以在本地模拟 HuggingFace Spaces。

```bash
docker compose up -d
```

访问：`http://localhost:7860`

### 本地开发

```bash
# 后端（Python 服务）
uv sync  # 安装依赖
uv run main.py  # 启动服务

# 前端（Web 界面）
cd web
bun install  # 安装依赖
bun run dev  # 启动开发服务器
```

---

## 📸 项目截图

> ⚠️ 截图待补充，你可以访问 [原项目](https://github.com/basketikun/chatgpt2api) 查看更多截图。

### 界面预览

| 功能 | 中文说明 |
|------|---------|
| **文生图界面** | 输入提示词生成图片 |
| **编辑图界面** | 上传图片进行编辑 |
| **号池管理** | 管理账号和额度 |
| **用户管理** | 创建普通用户账号 |

---

## ⚠️ 免责声明

> 本项目涉及对 ChatGPT 官网相关能力的逆向研究，仅供个人学习、技术研究与非商业性技术交流使用。
>
> - 严禁用于任何商业用途
> - 严禁用于违反 OpenAI 服务条款的行为
> - 严禁用于生成违法内容
> - 使用者应自行承担全部风险

---

## 📄 License

MIT License（MIT 开源许可证）

---

## 🙏 致谢

### 原项目

本项目基于 [basketikun/chatgpt2api](https://github.com/basketikun/chatgpt2api) 开发。

### 贡献者

<a href="https://github.com/basketikun/chatgpt2api/graphs/contributors">
  <img alt="Contributors" src="https://contrib.rocks/image?repo=basketikun/chatgpt2api" />
</a>

### 社区

学 AI，上 L 站：[LinuxDO](https://linux.do)

---

## 📌 Star History

如果这个项目对你有帮助，请给原项目一个 Star！

[![Star History Chart](https://api.star-history.com/chart?repos=basketikun/chatgpt2api&type=date)](https://star-history.com/)