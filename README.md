# 多 MCP 协同智能体金融助理项目

本项目是“从 0-1 打造多 MCP 协同智能体系统实战”的课程代码整理版，包含两个演示项目：

- `project1_stock_counselor`：手写 MCP Client 同时连接多个 SSE MCP Server。
- `project2_Agent_SDK+MCP_materials`：使用 OpenAI Agents SDK 编排多智能体，并通过 MCP Server 调用金融工具。

推荐优先运行 `project2_Agent_SDK+MCP_materials`，它包含 FastAPI 接口和 Gradio 前端。

## 功能

- 股票近期收盘价查询
- 股票未来走势预测
- 股票投资建议报告生成
- 金融政策本地知识库咨询
- 金融问题联网检索
- 金融文章专业性/规范性审查
- 多智能体业务转接
- 转人工服务模拟

## 环境要求

- Windows 10/11
- Python 3.13 或更高版本
- PowerShell

本仓库已经提供 `requirements.txt`，并推荐使用项目内虚拟环境 `.venv`。

## 本地运行

### 1. 创建虚拟环境

```powershell
python -m venv .venv
```

### 2. 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. 配置 API Key

项目运行目录中已经提供 `.env.example`，本地实际运行使用 `.env`。

项目 2 的 `.env` 路径：

```text
mcp_lecture_project/project2_Agent_SDK+MCP_materials/.env
```

内容如下：

```env
server_url=127.0.0.1
API_KEY=
DEEPSEEK_API_KEY=
APP_API_KEY=
APP_ID=
```

变量说明：

- `server_url`：本地运行保持 `127.0.0.1`。
- `API_KEY`：阿里云百炼 DashScope 兼容 OpenAI 接口 Key，用于 `qwen-plus` 和 embedding。
- `DEEPSEEK_API_KEY`：DeepSeek 官方 API Key，用于 Agents SDK 的 function calling。
- `APP_API_KEY` / `APP_ID`：DashScope Application 联网检索应用配置。

`.env` 已被 `.gitignore` 忽略，不会提交到 GitHub。

### 4. 启动项目 2

```powershell
.\scripts\start_project2.ps1
```

启动后访问：

- Gradio 前端：http://127.0.0.1:9996
- FastAPI 接口：http://127.0.0.1:9998/finance_MultiAgent_MultiMCP

接口请求示例：

```powershell
$body = @{
  current_message = "查询一下中国石油近期收盘价数据"
  session_id = ""
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:9998/finance_MultiAgent_MultiMCP" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### 5. 启动项目 1

```powershell
.\scripts\start_project1.ps1
```

然后在新终端中运行交互式客户端：

```powershell
cd mcp_lecture_project\project1_stock_counselor
..\..\.venv\Scripts\python.exe multi_sse_mcp_client.py
```

## 主要端口

项目 2：

- `8335`：转人工 MCP Server
- `8336`：股票预测 MCP Server
- `9330`：文章审查 MCP Server
- `9339`：金融咨询 MCP Server
- `9998`：FastAPI 服务
- `9996`：Gradio 前端

项目 1：

- `7335`：转人工 MCP Server
- `7336`：股票 MCP Server
- `7337`：政策回复 MCP Server

## GitHub 部署

本项目中的 `.env`、`.venv`、缓存和 IDE 配置不会被提交。首次推送到 GitHub：

```powershell
git init
git add .
git commit -m "Initial local runnable MCP multi-agent project"
git branch -M main
git remote add origin <你的GitHub仓库地址>
git push -u origin main
```

如果 GitHub 仓库已经存在，请只执行：

```powershell
git remote add origin <你的GitHub仓库地址>
git push -u origin main
```

## 注意事项

- 请不要把真实 API Key 写进代码或 README。
- 本地运行前确认 `.env` 中的 Key 已填写。
- 如果模型调用失败，先检查 `API_KEY`、`DEEPSEEK_API_KEY`、`APP_API_KEY` 和 `APP_ID`。
- 如果端口被占用，请先关闭旧进程或修改对应服务文件中的端口。
- `finance_consult_mcp_server.py` 使用 ChromaDB，本地知识库数据会写入 `db_data/`，该目录不会提交。

