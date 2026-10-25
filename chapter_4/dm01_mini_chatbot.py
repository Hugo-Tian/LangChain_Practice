from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MAX_PAIRS_HISTORY = 10

def keep_recent_messages(messages,max_pairs = MAX_PAIRS_HISTORY):
    """
    功能：保留最近N论对话
    :param messages:
    :param max_pairs:保留对话的轮数
    :return:系统消息与最近的{MAX_PAIRS_HISTORY}条消息
    """
    # 分离system和对话
    system_msgs = [m for m in messages if m["role"] == "system"]
    conversation_msgs = [m for m in messages if m["role"] == "conversation"]
    # 只保留最近的
    recent_msgs = conversation_msgs[-(max_pairs*2):]
    # 返回system+最近对话
    return system_msgs + recent_msgs


# 1. 基础配置
MODEL_NAME = "deepseek:deepseek-v4-flash"
MAX_PAIRS_HISTORY = 10
EXIT_WORD = "exit"

# 2. 初始化模型
model = init_chat_model(
    model = MODEL_NAME,
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = os.getenv("DEEPSEEK_BASE_URL"),


)

# 3. 初始化消息列表
message = [
    {
    "role":"system",
    "content": "你是一名专业的营养师，你要负责我的健康"
}
]

# 4. 启动提示
print(f"请输入对话，输入{EXIT_WORD}结束对话")
# 5. 多轮对话主循环
i=1   # 轮次记录

while True:
    print("\n", "=" * 10, f'-> 第 {i} 轮对话开始 <-', "=" * 10, "\n")
    user_input = input("请输入")

    # 退出判断
    if user_input == EXIT_WORD:
        break

    # 追加用户信息
    message.append({"role":"user", "content":user_input})

    # 流式输出模型回复
    print("AI营养师：",end = "",flush=True)

    reply_content = ""

    # 优化历史记忆
    memory_message = keep_recent_messages(message,max_pairs = MAX_PAIRS_HISTORY)
    # 控制发给模型的信息长度
    for chunk in model.stream(memory_message):
         if chunk.content:
             print(chunk.content,end = "",flush=True)
             reply_content += chunk.content
    print("\n", "=" * 10, f'-> 第 {i} 轮对话结束 <-', "=" * 10, "\n")
    i+=1

    # 追加AI回复
    message.append({"role":"conversation", "content":reply_content})

