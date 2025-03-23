from langchain_community.chat_models.tongyi import ChatTongyi

# 配置阿里云模型（使用通义千问）
llm = ChatTongyi(
    model="qwen-max",
    streaming=True,
    dashscope_api_key="sk-ede344d4156c410abbbcb921148a1362"
)