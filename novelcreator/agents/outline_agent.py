from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class OutlineResponse(BaseModel):
    outline: str = Field(..., description="生成的小说大纲")

# 大纲生成Agent
outline_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的小说大纲创作助手，负责生成一个结构清晰的小说大纲。

要求：
1. 基于小说标题和描述，生成一个详细的小说大纲
2. 大纲应该包含小说的主要情节线、关键转折点和结局
3. 大纲应该为后续章节生成提供足够的指导

请确保：
1. 大纲结构清晰，包含引入、发展、高潮、结局等部分
2. 大纲内容与小说标题和描述高度相关
3. 大纲为后续{chapter_count}章的内容提供足够的素材和指导
4. 大纲中包含主要人物的设定和发展轨迹

直接返回一个结构完整的大纲，无需解释你的思考过程。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n章节数量：{chapter_count}")
])

outline_chain = outline_prompt | llm.with_structured_output(OutlineResponse)

async def outline_agent(state: NovelState):
    """生成小说大纲"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await outline_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "chapter_count": state["chapter_count"]
            })
            
            # 检查是否有大纲
            if not response or not hasattr(response, 'outline') or not response.outline.strip():
                retry_count += 1
                print(f"\n警告：生成大纲失败，没有返回大纲数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认大纲")
                    return {"outline": "未能生成大纲"}
                continue
            
            print("生成的小说大纲：")
            print(f"\n大纲：\n{response.outline}")
            print("-" * 50)
            
            # 返回大纲
            return {"outline": response.outline}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成大纲时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认大纲")
                return {"outline": "未能生成大纲"}