from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

# 配置阿里云模型（使用通义千问）
llm = ChatTongyi(
    model="qwen-max-latest",
    streaming=True,
    api_key="sk-ede344d4156c410abbbcb921148a1362"
)

# res = llm.stream([HumanMessage(content="hi")], streaming=True)
# for r in res:
#     print("chat resp:", r.content)