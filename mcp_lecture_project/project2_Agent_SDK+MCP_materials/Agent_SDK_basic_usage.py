"""
使用multi-agent框架OpenAI_agent_SDK的基本代码操作讲解
pip install agents
1、DEEPSEEK模型必须是官网www.deepseek.com的模型，不能是其他平台接入的模型，原因是多智能体系统+MCP依赖于能做functioncalling的模型
其他接入deepseek的平台暂时不支持functioncalling
2、事件驱动的多智能体框架，每次运行产生一系列的时间通过.new_items属性查看历史所有事件
3、智能体的转交通过内部执行transfer_xxx_agent的functioncalling的方法实现
"""
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel,Agent,Runner,set_default_openai_client
from agents.model_settings import ModelSettings
from agents import set_tracing_disabled
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[0]
STOCK_DATA_PATH = PROJECT_ROOT / "project1_stock_counselor" / "stock_data.xlsx"
sys.path.append(str(SCRIPT_DIR))
set_tracing_disabled(False) # 是否跟踪智能体运行过程
# 设置DeepSeek模型作为Agent的驱动模型：.env
load_dotenv()
server_url=os.getenv("server_url", "127.0.0.1") #server_url="192.110.223.33"
external_client = AsyncOpenAI(
    base_url = "https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"))

#取代默认的openAI model为自定义的LLM client
set_default_openai_client(external_client)
deepseek_model = OpenAIChatCompletionsModel(
    model="deepseek-chat",
    openai_client=external_client)
print(deepseek_model)
#%%
######################1.智能体Agent的定义与调用#############
# 创建一个咨询Agent：
import asyncio
consult_agent = Agent(name="consult agent",  # 智能体名称：咨询智能体
              instructions="你是一个只能回答医疗领域的智能体", #智能体的功能描述,system_prompt 你是一个善于回答金融问题的助理
              model=deepseek_model)
#异步调用智能体执行用户输入 Run a workflow starting at the given agent
async def main():
    result = await Runner.run(starting_agent=consult_agent, input="美国次贷危机发生在哪一年？")
    print(result)
    print("final_response:", result.final_output)  # 本轮最终输出的结果
    # 通过new_items属性来查看全部的事件list：
    print("event_list:", result.new_items)
    # 具体回复的内容
    print(result.new_items[0].raw_item)
    print(len(result.new_items))  # 返回事件数




asyncio.run(main())
#%%
# print(result)
#%%

#%%

#%%
###############多轮对话通过memory进行历史对话继承#######################
async def main1():
    result = await Runner.run(starting_agent=consult_agent, input="美国次贷危机发生在哪一年？")
    print(result)
    print("final_response:", result.final_output)  # 本轮最终输出的结果
    # 通过new_items属性来查看全部的事件list：
    print("event_list:", result.new_items)
    # 具体回复的内容
    print(result.new_items[0].raw_item)
    print(len(result.new_items))  # 返回事件数
    # 将本轮对话结果追加到消息列表，专门的API，return_result.to_input_list()
    messages = result.to_input_list()
    print("多轮对话messages list:", messages)
    # 而此时，我们只需要将此前对话消息，加上新一轮的对话消息，即可快速进行多轮对话：
    messages.append({"role": "user", "content":"请问刚才我问过美国次贷危机这个问题了吗？"})
    print("messages:",messages)

    result1 = await Runner.run(starting_agent=consult_agent, input=messages)
    # 而此次运行的事件则会保留在result1中：
    print("result1:",result1)
    print("event_len1:", len(result.new_items))

asyncio.run(main1())

#%%
##################2.Agent的工具调用##################
from agents import function_tool
import numpy as np
import pandas as pd
import requests,json
def exponential_moving_average(series, alpha, forecast_periods=1):
    """
    计算指数移动平均并预测未来值
    参数:
    series: pandas.Series，原始时间序列数据
    alpha: float，平滑因子，范围(0,1]
    forecast_periods: int，预测未来的期数，默认为1
    返回:
    forecast: pandas.Series，包含原始数据的EMA和平滑后的预测值
    """
    # 计算EMA
    ema = series.ewm(alpha=alpha, adjust=False).mean()
    # 获取最后一个EMA值作为预测基础
    last_ema = ema.iloc[-1]
    # 创建未来日期索引
    future_dates = pd.date_range(
        start=series.index[-1],
        periods=forecast_periods + 1,
        freq=pd.infer_freq(series.index)
    )[1:]
    # 创建预测值序列
    forecast_values = np.full(forecast_periods, last_ema)
    forecast_series = pd.Series(forecast_values, index=future_dates)
    # 合并原始数据的EMA和预测值
    full_forecast = pd.concat([ema, forecast_series])
    return full_forecast

#函数1：定义预测未来7天股票收盘价及与近三天收盘价进行比较涨跌的函数
def predict_future_7data(stock_name):
    if stock_name=="上证指数":
        stock_data = pd.read_excel(STOCK_DATA_PATH,
            parse_dates=['Date'], sheet_name='上证指数')
    elif stock_name=="中国石油":
        stock_data = pd.read_excel(STOCK_DATA_PATH,
            parse_dates=['Date'], sheet_name='中国石油')
    elif stock_name=="中国银行":
        stock_data = pd.read_excel(STOCK_DATA_PATH,
            parse_dates=['Date'], sheet_name='中国银行')
    else:
        return f"我无法预测未来7日{stock_name}股票的收盘价"
    stock_data.asfreq('D')
    series = pd.Series(np.float16(stock_data['Close']), index=stock_data['Date'])
    # 计算EMA并预测未来10期
    alpha = 0.8  # 平滑因子
    forecast =exponential_moving_average(series, alpha, forecast_periods=3)
    print("forecast:",forecast)

    forecast_in_oneline=",".join([str(round(k,3)) for k in list(forecast)[-7:]])
    print("forecast_in_oneline:",forecast_in_oneline)
    #计算未来七天的均值

    avg_value=round(np.average(np.array(forecast).tolist()[-7:]),3)
    #计算股票近三天的平均收盘价
    avg_last_three_days_stock_price = stock_data['Close'][-3:].mean()

    print("last_three_days_stock_price:", avg_last_three_days_stock_price,"avg_value:",avg_value)
    if avg_last_three_days_stock_price>=avg_value:
        return_message = f"未来7天{stock_name}股票的收盘价预测结果为:{forecast_in_oneline}，未来7天平均收盘价为{avg_value}，预计会比近期价格有所下跌" #近三天股票{stock_name}的平均收盘价为{last_three_days_stock_price}，
    else:
        return_message = f"未来7天{stock_name}股票的收盘价预测结果为:{forecast_in_oneline}，未来7天平均收盘价为{avg_value}，预计会比近期价格有所上涨" #近三天股票{stock_name}的平均收盘价为{last_three_days_stock_price}，
    return return_message
#使用工具装饰器定义工具
@function_tool
async def predict_future_7data_tool(stock_name :str) -> str:
    """
     输入指定的股票名称，返回股票未来的涨跌趋势
    :param stock_name:股票名称，如：上证指数,中国石油,中国银行等
    :return: 股票未来的涨跌趋势描述，如：未来七天将上涨/下跌
    """
    return_message = predict_future_7data(stock_name)
    return return_message
stock_agent = Agent(
    name="收盘价预测Agent",
    instructions="你是一名智能助手，你能预测股票未来的收盘价",
    tools=[predict_future_7data_tool],
    model=deepseek_model
)
async def main3():
    predict_result = await Runner.run(stock_agent, input="请问上证指数未来收盘价是多少？")
    print("predict_result:",predict_result)
    print("xxx:",predict_result.new_items)
    print("event len:",len(predict_result.new_items))
    return predict_result.final_output
asyncio.run(main3())
#%%
#Runner.run是一个事件循环,会不停的执行程序直到max_turns或者完成目标任务
@function_tool
def judge_interest(attitude):
    """
    根据用户是否喜欢该商品进行分别回复
    :param attitude: 必要参数，判断用户是否对该商品感兴趣；eg:感兴趣,不感兴趣
    :return：是否成功写入
    """
    if attitude=="感兴趣":
        return "用户喜欢该商品"
    else:
        return "用户不喜欢该商品"

@function_tool
def changed_attitude(attitude):
    """
    根据用户是否喜欢该商品决定是否向其推荐其它商品
    :param attitude: 用户对某商品是否感兴趣，eg:感兴趣,不感兴趣
    :return：是否推荐其它商品
    """
    if attitude=="感兴趣":
        return "不推荐其它商品,就这个商品"
    else:
        return "好的，推荐商品B给您，您再看看呢"
interest_agent = Agent(
    name="喜好Agent",
    instructions="你是一名智能助手，你能依据用户兴趣进行商品推荐",
    tools=[changed_attitude,judge_interest],
    model=deepseek_model
)
async def main4():
    predict_result = await Runner.run(interest_agent, input="我不喜欢这款哈密瓜") #我喜欢这款哈密瓜
    print("predict_result:",predict_result)
    print(predict_result.new_items)
    # 调用工具1：参数抽取+工具执行返回
    print(predict_result.new_items[0])
    print(predict_result.new_items[1])
    # %%
    # 调用工具2：参数抽取+工具执行返回
    print(predict_result.new_items[2])
    print(predict_result.new_items[3])

    print(predict_result.new_items[4])  # 最终回复
asyncio.run(main4())
#%%
#################Agents SDK的多Agent执行流程(handoffs的妙用)#######################
#多智能体框架中的多智能体，通过的智能体之间handsoff的方式进行协作的
#阳春白雪的智能体
poem_agent = Agent(
    name="poem agent",
    instructions="你是一个诗人,你善于将用户问题转化为诗歌进行回复",
    handoff_description="当用户输入描述美景的话时，调用该智能体回答问题", #告诉LLM什么时候转交给该智能体
    model=deepseek_model
)
#粗俗的智能体
vulgar_agent = Agent(
    name="vulgar agent",
    instructions="你是一个粗俗的人,你只能用粗俗下三滥的语言进行回复", #定义智能体的功能
    handoff_description="当用户骂脏话时，调用该智能体来回答用户问题", #描述智能体交接时候的场景
    model=deepseek_model
)
async def main5():
    response = await Runner.run(poem_agent, input="今天月亮好圆啊")
    print(response.final_output)
    response = await Runner.run(vulgar_agent, input="今天月亮好圆啊")
    print(response.final_output)

asyncio.run(main5())

#%%
#创建一个调度智能体，该智能体能根据用户的话术决策用哪个下游智能体帮助回复
switch_agent=Agent(
    name="switch Agent",
    instructions="请根据用户需求移交给合适的智能体进行回复，若没合适的则自己回答",
    handoffs=[vulgar_agent,poem_agent],#转交list
    mcp_servers=[],
    model=deepseek_model
)

async def main6():
    response = await Runner.run(switch_agent, input="今天月亮好圆啊") #今天月亮好圆啊 你个垃圾
    print(response.final_output)
    print(response.new_items)


asyncio.run(main6())
#%%
#看看中间的执行过程
print(response.new_items)
#%%
###################Agent SDK中集成MCP功能############################
import shutil
from agents import Agent, Runner, trace
from agents.mcp import MCPServer, MCPServerSse
from contextlib import AsyncExitStack
#定义
async def run_mcp_servers(servers_params, message):
    # 使用 AsyncExitStack管理server上下文
    async with AsyncExitStack() as stack:
        servers = [] #记录所有符合agent SDK范式的mcp服务列表
        # 创建并进入所有 server 上下文
        for p in servers_params:
            print("p:",p)
            #根据服务端类型将所有MCP SERVER添加至上下文
            server = MCPServerSse(
                name=p.get("name", "未命名的MCP服务器"),
                cache_tools_list=True,
                params={
                    "url":p['url']
                },
            )
            print(p.get("name"))
            entered_server = await stack.enter_async_context(server)
            servers.append(entered_server)
        print("servers:",servers)
        # 构造 agent，传入多个 server
        agent = Agent(
            name="Assistant",
            instructions="你是一个股票心理按摩师，你能帮助股民回答问题，解决心理困扰",
            mcp_servers=servers, #所有MCP服务器组成的list
            model_settings=ModelSettings(tool_choice="auto"),
            model=deepseek_model
        )
        print(f"Running: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        return result

async def main7():
    result = await run_mcp_servers(
        servers_params=[
            {"name": "policy reply Server", "url":f"http://{server_url}:7337/sse"},
            {"name": "stock Server", "url":f"http://{server_url}:7336/sse"} #,"type":"stdio"
        ],
        message="帮我查询上证指数未来的趋势"
    )
    print("result:",result)
    print(result.new_items)

asyncio.run(main7())
