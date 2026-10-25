from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage



# 原始模板
template = ChatPromptTemplate.from_messages([
    ("system","你是{role},目标用户是{audience}"),
    ("user","{task}")
])

# 用partial()函数进行部分变量预填充
customer_support_template = template.partial(
    role = "客服专员",
    audience="普通用户"
)
# 现在就只需要填充task
messages = customer_support_template.invoke({"task":"介绍一下产品"})
print(messages)