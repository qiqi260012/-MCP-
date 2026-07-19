# 股票辅助分析与投资者情绪安抚 Agent

这个项目主要解决一个很具体的问题：投资者在咨询股票时，往往不只是想看数据，也会带着明显情绪，比如焦虑、亏损后的沮丧，或者短期上涨后的兴奋。所以我把行情分析、趋势预测、情绪回复和人工转接拆成多个 MCP 工具，让 Agent 根据用户输入自动选择合适的处理链路。

## 我做了什么

- 封装股票行情 MCP 工具，支持查询近三日平均收盘价，并和前一阶段均值做趋势对比。
- 使用 EWMA 方法做短期走势预测，为回复提供量化依据。
- 设计情绪回复策略，根据用户情绪和股票走势生成更稳妥的安抚话术。
- 接入人工转接 MCP 工具，用来处理极端情绪或高风险表达。
- 编写 MCP Client，同时连接多个 SSE MCP Server，统一收集工具并交给大模型调度。

## 技术栈

- Python
- MCP / FastMCP
- SSE
- Pandas / NumPy
- EWMA 时间序列预测
- OpenAI compatible API
- Function Calling
- Prompt Engineering

## 核心模块

- `stock_sever.py`：股票数据查询和趋势预测 MCP Server。
- `policy_reply_server.py`：结合用户情绪和行情走势生成回复策略。
- `turn_human_server.py`：人工转接工具服务。
- `multi_sse_mcp_client.py`：聚合多个 MCP Server 的客户端。
- `function_utils.py`：移动平均预测、股票趋势计算和回复策略函数。

## 业务流程

```text
用户输入
  -> Agent 识别股票名称、情绪和咨询意图
  -> 调用股票行情/预测 MCP 工具
  -> 调用情绪回复策略 MCP 工具
  -> 高风险情况触发人工转接
  -> 返回带数据依据和风险提示的回复
```

## 本地运行

在仓库根目录创建虚拟环境并安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

复制环境变量模板：

```powershell
Copy-Item mcp_lecture_project\project1_stock_counselor\.env.example mcp_lecture_project\project1_stock_counselor\.env
```

填写 `.env`：

```env
server_url=127.0.0.1
API_KEY=
DEEPSEEK_API_KEY=
```

启动 MCP 服务：

```powershell
.\scripts\start_project1.ps1
```

再打开一个终端运行交互式客户端：

```powershell
cd mcp_lecture_project\project1_stock_counselor
..\..\.venv\Scripts\python.exe multi_sse_mcp_client.py
```

## 可以测试的问题

```text
我想了解一下中国银行的股市情况
中国石油又跌了，我有点难受
上证指数最近怎么样
我想转人工
```

## 面试时可以重点讲

- 为什么把行情分析、回复策略和转人工拆成不同 MCP Server。
- 如何通过 Function Calling 抽取股票标的、用户情绪和工具参数。
- 如何避免大模型直接给出不合规的投资建议。
- 极端情绪和接口异常场景下如何做兜底。
