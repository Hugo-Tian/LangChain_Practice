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
                        temperature = 1.0,
                        api_key=DEEPSEEK_API_KEY,
                        base_url=DEEPSEEK_BASE_URL)



# 使用字典列表构建消息
message1=[
    {"role":"system","content":"你是一个数学老师"},
    {"role":"user","content":"帮我解释一下导数"}
]

#使用消息对象列表构建信息
message2=[
    SystemMessage("你是我的宠物小狗"),
    HumanMessage("要不要出去玩"),


]
# 向模型发送单条数据
response = model.invoke(message2)

# 打印响应
rprint(response)


