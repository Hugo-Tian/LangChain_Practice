from langchain_deepseek import ChatDeepSeek
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

# 将.env中的变量加载为环境变量
load_dotenv(override=True)

# 从环境变量读取配置
# 可以省略，有默认值
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# 创建Deepseek LLM
deepseek_llm = ChatDeepSeek(
    # api_key=DEEPSEEK_API_KEY,
    # base_url=DEEPSEEK_BASE_URL,
    model_name='deepseek-flash'
)

print(deepseek_llm.invoke('你是谁'))