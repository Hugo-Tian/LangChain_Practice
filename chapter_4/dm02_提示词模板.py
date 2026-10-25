from langchain_core.prompts import ChatPromptTemplate

# 定义聊天提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个有帮助的AI机器人，你的名字是{name}。"),
        ("human", "你好，最近怎么样？"),
        ("ai", "我很好，谢谢！"),
        ("human", "{user_input}"),
    ]
)

# 格式化聊天提示词模板中的变量
prompt = chat_prompt_template.invoke({"name":"Hugo","user_input":"你是谁"})

print(prompt)