from langchain.messages import HumanMessage,ToolMessage
import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from rich import print as rprint
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from langchain.tools import tool
from pydantic import BaseModel,Field
from langchain_core.utils.function_calling import convert_to_openai_tool

# 从 .env 文件中加载环境变量；override=True 表示覆盖已有的同名环境变量
load_dotenv(override=True)

# 从环境变量中读取配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# 初始化聊天模型，使用环境变量中的密钥和接口地址连接服务
model = init_chat_model(model='deepseek:deepseek-v4-flash',
                        # 设置温度值，控制输出随机性，范围0.0-2.0，越高越随机
                        temperature = 0.0,
                        api_key=DEEPSEEK_API_KEY,
                        base_url=DEEPSEEK_BASE_URL)

# 用 Pydantic 定义工具的输入结构：参数类型、默认值和供模型理解的说明
# 注意：Schema 中的默认值不等于下面 Python 函数签名中的参数默认值
class weatherSchema(BaseModel):
    city: str = Field(default = "上海", description="城市名称")
    if_forecast :bool = Field(default = False,description="是否包含天气预报")

# 将函数包装为 LangChain 工具；args_schema 指定输入参数的校验规则
@tool("get_weather_and_forecast", description="查询当日天气，可以包含明日天气预报",args_schema=weatherSchema)
def get_weather_and_forecast(city:str,if_forecast:bool):
    # 此处使用模拟天气数据，没有调用真实的天气查询接口
    res = f"{city} 今天天气不错"
    # 当模型传入 if_forecast=True 时，额外返回明日预报
    if if_forecast:
        res +="\n明天也不错"
    return res

# 打印 OpenAI 工具格式的定义，查看工具名称、描述和参数结构；不会执行工具
print(convert_to_openai_tool(get_weather_and_forecast))

# 将工具定义提供给模型；bind_tools 本身不会自动执行 Python 函数
model_with_tools = model.bind_tools([get_weather_and_forecast])

# 消息列表保存完整对话，后续依次加入模型的调用请求、工具结果和模型回答
messages = [HumanMessage("今天杭州天气如何？明天呢？")]
# 第一次调用：模型根据用户问题决定是否调用工具，并生成工具参数
response = model_with_tools.invoke(messages)
# 必须保留包含工具调用请求的 AIMessage，供后续工具结果与其对应
messages.append(response)
# response 是 AIMessage 对象，通过属性访问 tool_calls，而不是字典下标
# 每个调用包含 name（工具名）、args（参数）、id（调用标识）等字段
# 如果模型没有请求调用工具，这里得到空列表
tool_calls = response.tool_calls

# 模型可能一次请求多个工具调用，因此逐个处理
for tool_call in tool_calls:
    # 使用 name 字段判断应该执行哪个工具
    if tool_call["name"] == "get_weather_and_forecast":
        # 传入完整的 ToolCall：工具校验参数并执行，返回 ToolMessage
        # ToolMessage 中的 tool_call_id 用于关联模型发起的那一次调用
        tool_msg = get_weather_and_forecast.invoke(tool_call)
        # 将工具结果加入对话，下一次模型调用才能读取到这些结果
        messages.append(tool_msg)

# 第二次调用：把工具结果交给模型，让模型组织自然语言回答
# 此示例只处理一轮工具调用；若模型再次请求工具，需继续执行工具并回传结果
final_response = model_with_tools.invoke(messages)
messages.append(final_response)
# 按消息类型格式化打印整个过程，便于观察 Human → AI → Tool → AI 的顺序
for msg in messages:
    msg.pretty_print()
