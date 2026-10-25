import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from rich import print as rprint
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

# 从.env文件中加载环境变量
load_dotenv(override=True)

# 从环境变量中读取配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

model = init_chat_model(model='deepseek:deepseek-v4-flash',
                        # 设置温度值，控制输出随机性，范围0.0-2.0，越高越随机
                        temperature = 0,
                        api_key=DEEPSEEK_API_KEY,
                        base_url=DEEPSEEK_BASE_URL)

#流式调用
# for chunk in model.stream('写一首诗，预测未来的ai发展'):
#     rprint(chunk.text,end="",flush=True)

# 批量调用
messages=[
    "你是谁",
    "ai的定义是什么",
    "ai的就业岗位有哪些"
]

# responses = model.batch(messages)
# for response in responses:
#     rprint(response.text,end="",flush=True)

rprint(model.profile)