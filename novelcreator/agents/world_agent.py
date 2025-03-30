from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class WorldSettingResponse(BaseModel):
    world_setting: str = Field(..., description="生成的小说世界观设定")

# 世界观生成Agent
world_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的小说世界观创作助手，负责生成一个详细、丰富且具有内在逻辑的世界观设定。

要求：
1. 基于小说标题、描述和大纲，生成一个详细的世界观设定
2. 世界观应该包含该小说世界的基本规则、背景历史、地理环境、社会结构等
3. 世界观应该为后续章节内容提供坚实的基础

请确保：
1. 世界观设定具有内在一致性和逻辑性
2. 世界观设定与小说标题、描述和大纲高度相关
3. 世界观设定包含足够的细节，但不过于冗长
4. 世界观设定能够支撑小说情节的发展

直接返回一个结构完整的世界观设定，无需解释你的思考过程。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}")
])

world_chain = world_prompt | llm.with_structured_output(WorldSettingResponse)

async def world_agent(state: NovelState):
    """生成小说世界观设定"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await world_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"]
            })
            
            # 检查是否有世界观设定
            if not response or not hasattr(response, 'world_setting') or not response.world_setting.strip():
                retry_count += 1
                print(f"\n警告：生成世界观设定失败，没有返回世界观数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认世界观设定")
                    return {"world_setting": "未能生成世界观设定"}
                continue
            
            print("生成的小说世界观设定：")
            print(f"\n世界观：\n{response.world_setting}")
            print("-" * 50)
            
            # 返回世界观设定
            return {"world_setting": response.world_setting}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成世界观设定时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认世界观设定")
                return {"world_setting": "未能生成世界观设定"}