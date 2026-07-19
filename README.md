# 多 MCP 协同智能体金融助理项目

这是一个围绕金融服务场景搭建的多智能体应用。我把股票查询预测、金融政策咨询、文章风控审查和转人工服务拆成多个 MCP 工具服务，再用智能体负责理解用户意图、选择工具和完成业务转接。

项目里保留了两套实现：

- 基础版：手写 MCP Client，同时连接多个 SSE MCP Server，便于理解 MCP 工具聚合流程。
- 完整应用版：基于 OpenAI Agents SDK 编排多个业务智能体，并提供 FastAPI 接口和 Gradio 页面。

本地体验建议直接运行完整应用版，对应目录是 `mcp_lecture_project/project2_Agent_SDK+MCP_materials`。

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

依赖统一放在 `requirements.txt` 里，推荐使用项目内虚拟环境 `.venv`，避免影响电脑上的其他 Python 项目。

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

完整应用版的 `.env` 路径：

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

### 4. 启动完整应用版

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

### 5. 启动基础版

```powershell
.\scripts\start_project1.ps1
```

然后在新终端中运行交互式客户端：

```powershell
cd mcp_lecture_project\project1_stock_counselor
..\..\.venv\Scripts\python.exe multi_sse_mcp_client.py
```

## 主要端口

完整应用版：

- `8335`：转人工 MCP Server
- `8336`：股票预测 MCP Server
- `9330`：文章审查 MCP Server
- `9339`：金融咨询 MCP Server
- `9998`：FastAPI 服务
- `9996`：Gradio 前端

基础版：

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
