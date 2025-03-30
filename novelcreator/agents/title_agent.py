from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class TitleResponse(BaseModel):
    title: str = Field(..., description="生成的小说标题")

# 标题生成Agent
title_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的小说标题创作助手，负责生成一个引人入胜的小说标题。

要求：
1. 生成一个简洁、有吸引力且能反映小说主题的标题
2. 标题应该能够引起读者的兴趣和好奇心
3. 标题应该与小说描述高度相关

请确保：
1. 标题简洁有力，通常不超过10个字
2. 标题能够反映小说的核心主题或冲突
3. 标题具有文学性和吸引力
4. 标题与小说描述高度相关

直接返回一个最适合的标题，无需解释你的思考过程。"""),
    ("human", "小说描述：{description}")
])

title_chain = title_prompt | llm.with_structured_output(TitleResponse)

async def title_agent(state: NovelState):
    """生成小说标题"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await title_chain.ainvoke({
                "description": state["description"]
            })
            
            # 检查是否有标题
            if not response or not hasattr(response, 'title') or not response.title.strip():
                retry_count += 1
                print(f"\n警告：生成标题失败，没有返回标题数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认标题")
                    return {"title": "未命名小说"}
                continue
            
            print("生成的小说标题：")
            print(f"\n标题：{response.title}")
            print("-" * 50)
            
            # 返回标题
            return {"title": response.title}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成标题时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认标题")
                return {"title": "未命名小说"}