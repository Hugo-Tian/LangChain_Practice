from langchain.messages import HumanMessage,ToolMessage
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from rich import print as rprint
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from langchain.tools import tool

# 从.env文件中加载环境变量
load_dotenv(override=True)

# 从环境变量中读取配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

model = init_chat_model(model='deepseek:deepseek-v4-flash',
                        # 设置温度值，控制输出随机性，范围0.0-2.0，越高越随机
                        temperature = 0.0,
                        api_key=DEEPSEEK_API_KEY,
                        base_url=DEEPSEEK_BASE_URL)

@tool(parse_docstring = True)
def get_weather(city:str):
    """
    获取天气的工具

    Args:
         city:城市
    """

    return f"{city}的天气晴朗"

# 将模型与工具绑定
model_with_tools = model.bind_tools([get_weather])

messages = [
    HumanMessage("上海今天天气如何")
]

# # 模型生成调用工具请求
# response = model_with_tools.invoke(messages)
#
# # 添加AIMessage
# messages.append(response)
#
# tool_calls = response.tool_calls
#
# for tool_call in tool_calls:
#     if tool_call["name"]=="get_weather":
#         # 返回的是ToolMessage类型消息
#         tool_response= get_weather.invoke(tool_call)
#         print(type(tool_response))
#         messages.append(tool_response)
#
# print("=======================messages=========================")
# for msg in messages:
#     msg.pretty_print()
# print("=======================messages=========================")
# final_response = model_with_tools.invoke(messages)
# print(f"final_response:{final_response}")

while True:
    # 1. 调用模型
    response = model_with_tools.invoke(messages)
    messages.append(response)

    # 2. 没有工具调用，说明可以结束
    if not response.tool_calls:
        break

    # 3. 执行所有工具
    for tool_call in response.tool_calls:
        if tool_call["name"] == "get_weather":
            tool_response = get_weather.invoke(tool_call)
            messages.append(tool_response)

print(response.content)