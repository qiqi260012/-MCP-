"""
项目二的公共函数定义
pip install openai
pip install dotenv
"""
#%%
from dotenv import load_dotenv
import os
import asyncio
from openai import AsyncOpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
# 获取当前脚本所在目录
script_dir = Path(__file__).resolve().parent
# 加载 .env 文件
env_path = script_dir / ".env"
load_dotenv(env_path)

#定义大模型调用函数，用于处理文本类审查、生成工作
async def LLM_replay(prompt_template,messages):
    """
    prompt_template:大模型调用的提示词模板
    message:大模型调用的用户输入
    """
    llm_client =AsyncOpenAI(api_key=os.getenv("API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    result =await llm_client.chat.completions.create(
        model="qwen-plus", #推荐使用:qwen-plus-latest qwen-plus qwen-max-0125 qwen-plus-latest -0125
        messages=[{"role":"system","content":prompt_template},{"role":"user","content":messages}],
        max_tokens=8192,
        temperature=0)
    return result
# result=await LLM_replay(prompt_template="你是一个AI聊天助手",messages="你好")
# async def main():
#     result=await LLM_replay(prompt_template="你是一个AI聊天助手",messages="你好")
#     print("result:",result.choices[0].message.content)
#
# asyncio.run(main())

#%%
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
# from matplotlib import pyplot as plt
#%%
import numpy as np
import pandas as pd


def simple_moving_average(series, window):
    """计算简单移动平均"""
    return series.rolling(window=window).mean()


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
