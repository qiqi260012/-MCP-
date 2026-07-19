# 多 MCP 协同金融智能咨询 Agent 系统

这个项目是一个多智能体金融咨询系统。我把金融场景里的几类任务拆开：股票趋势研判、金融政策问答、文章风险审查和人工转接，每一类都封装成独立 MCP 服务，再由主 Agent 判断用户意图并转交给对应的专项 Agent。

相比单个聊天机器人，这个项目更关注工具调度、任务分流、多轮上下文和后端接口落地。

## 我做了什么

- 设计主 Agent + 专项子 Agent 的协作结构，让系统可以根据用户意图自动分流。
- 基于 MCP 封装四类服务工具：股票预测、金融咨询、文章审查、人工转接。
- 使用 FastAPI 提供后端接口，支持前端或第三方系统接入。
- 使用 Gradio 搭建本地可交互页面，方便演示完整对话流程。
- 设计全局会话管理逻辑，保存多轮消息和当前处理 Agent。
- 使用结构化 Prompt 和 Function Calling 提升工具调用稳定性。
- 接入本地投资政策知识库，并通过 ChromaDB 做相似度检索。

## 技术栈

- Python
- OpenAI Agents SDK
- MCP / FastMCP
- FastAPI
- SSE
- DeepSeek API
- DashScope / Qwen
- ChromaDB
- Gradio
- Pandas / NumPy
- python-docx

## 智能体设计

- `Switch Agent`：业务分流入口，判断用户需求并转交任务。
- `Investment Agent`：处理股票查询、趋势预测和投资分析报告。
- `Consult Agent`：处理金融政策、本地知识库和联网检索问答。
- `Article Check Agent`：处理金融文章专业性和规范性审查。
- `turn_human Agent`：处理人工转接请求。

## MCP 服务

- `stock_predict_mcp_server.py`：股票近期走势查询、未来趋势预测、投资建议报告生成。
- `finance_consult_mcp_server.py`：投资政策知识库问答和金融问题检索。
- `article_check_mcp_server.py`：金融文章专业性审查、规范性审查、审查报告生成和文章优化。
- `turn_human_server.py`：人工客服转接。

## 运行方式

在仓库根目录创建虚拟环境并安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

复制环境变量模板：

```powershell
Copy-Item mcp_lecture_project\project2_Agent_SDK+MCP_materials\.env.example mcp_lecture_project\project2_Agent_SDK+MCP_materials\.env
```

填写 `.env`：

```env
server_url=127.0.0.1
API_KEY=
DEEPSEEK_API_KEY=
APP_API_KEY=
APP_ID=
```

变量说明：

- `API_KEY`：阿里云百炼 DashScope 兼容 OpenAI 接口 Key，用于 Qwen 和 embedding。
- `DEEPSEEK_API_KEY`：DeepSeek 官方 API Key，用于驱动 Agents SDK。
- `APP_API_KEY` / `APP_ID`：DashScope Application 配置，用于联网检索。

启动完整服务：

```powershell
.\scripts\start_project2.ps1
```

访问地址：

- Gradio 页面：http://127.0.0.1:9996
- FastAPI 接口：http://127.0.0.1:9998/finance_MultiAgent_MultiMCP

## 接口示例

```powershell
$body = @{
  current_message = "查询一下中国石油近期收盘价数据，然后生成一份简短分析"
  session_id = ""
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:9998/finance_MultiAgent_MultiMCP" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## 可以测试的问题

```text
查询一下中国石油近期收盘价数据
帮我预测一下上证指数未来趋势
生成一份中国银行的投资分析报告
非法或受到国际制裁的行业有哪些
帮我审查《全球增长基金的表现与风险分析.docx》
我想转人工
```

## 面试时可以重点讲

- 多 Agent 的任务转交逻辑是怎么设计的。
- MCP 工具服务为什么按业务边界拆分。
- 如何维护多轮会话里的当前 Agent 和消息上下文。
- 本地知识库问答和联网检索如何做兜底。
- 金融文章审查如何拆成专业性、规范性和报告生成三个步骤。
- FastAPI、SSE、Gradio 分别在这个项目里承担什么角色。
