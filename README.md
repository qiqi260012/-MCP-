# 多智能体金融应用项目集

这个仓库放了我围绕金融服务场景做的两个 Agent 项目。两个项目都使用 MCP 做工具封装，但侧重点不一样：一个更聚焦股票咨询和投资者情绪安抚，另一个更偏完整的多智能体金融咨询系统。

## 项目一：股票辅助分析与投资者情绪安抚 Agent

目录：`mcp_lecture_project/project1_stock_counselor`

这个项目主要面向投资者咨询场景。用户输入股票相关问题后，系统会识别股票标的、用户情绪和咨询意图，再调用行情分析、趋势预测、回复策略或人工转接工具，生成更稳妥的回复。

核心能力：

- 股票近期收盘价趋势分析
- 基于 EWMA 的短期走势预测
- 投资者情绪识别与安抚回复
- 极端情绪场景下的人工转接
- 多个 SSE MCP Server 的统一接入

技术栈：

`Python`、`MCP`、`FastMCP`、`Pandas`、`EWMA`、`Function Calling`、`Prompt Engineering`

详细说明：[项目一 README](mcp_lecture_project/project1_stock_counselor/README.md)

## 项目二：多 MCP 协同金融智能咨询 Agent 系统

目录：`mcp_lecture_project/project2_Agent_SDK+MCP_materials`

这个项目是一个更完整的多智能体金融咨询系统。我把金融文章审查、投资问题答疑、股价趋势研判、知识库问答和人工转接拆成不同 MCP 工具服务，再通过主 Agent 做意图识别和任务分发。

核心能力：

- 多 Agent 业务分流与任务转交
- 多个 MCP 工具服务统一调度
- 金融文章专业性/规范性审查
- 投资政策知识库问答
- 股票趋势查询、预测和报告生成
- FastAPI 接口与 Gradio 页面
- 多轮会话上下文管理

技术栈：

`Python`、`OpenAI Agents SDK`、`MCP`、`FastAPI`、`SSE`、`DeepSeek`、`DashScope`、`ChromaDB`、`Gradio`

详细说明：[项目二 README](mcp_lecture_project/project2_Agent_SDK+MCP_materials/README.md)

## 本地环境

建议使用项目内虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

两个项目都需要在各自目录下配置 `.env`。仓库里提供了 `.env.example`，真实 API Key 请只写在 `.env` 中，`.env` 不会提交到 GitHub。

## 快速启动

启动项目一：

```powershell
.\scripts\start_project1.ps1
```

启动项目二：

```powershell
.\scripts\start_project2.ps1
```

项目二启动后可以访问：

- Gradio 页面：http://127.0.0.1:9996
- FastAPI 接口：http://127.0.0.1:9998/finance_MultiAgent_MultiMCP

## 说明

这个仓库更适合作为项目展示和面试讲解材料。代码里保留了从 MCP Server、Agent 编排、工具调用、会话管理到前端页面的完整链路，方便说明我在 Agent 应用开发、金融场景工具封装和后端接口联调上的实践过程。
