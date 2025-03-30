from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState
from typing import List

# 定义Pydantic模型
class Character(BaseModel):
    name: str = Field(..., description="角色名称")
    role: str = Field(..., description="角色在故事中的定位")
    personality: str = Field(..., description="角色性格特点")
    background: str = Field(..., description="角色背景故事")
    motivation: str = Field(..., description="角色动机与目标")
    relationships: str = Field(..., description="与其他角色的关系")
    appearance: str = Field(..., description="角色外貌描述")
    development: str = Field(..., description="角色在故事中的成长轨迹")

class CharacterResponse(BaseModel):
    characters: List[Character] = Field(..., description="生成的角色列表")
    thought: str = Field("", description="角色设计的思考过程")

# 角色生成Agent
character_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的小说角色设计师，负责创建丰富、立体的小说角色。

要求：
1. 基于小说标题、描述、大纲和世界观，创建3-5个主要角色
2. 每个角色都应该有鲜明的性格特点、背景故事和动机
3. 角色之间应该存在合理的关系和互动可能
4. 角色设定应该与小说世界观和情节相符

请确保：
1. 角色性格多样化，避免千篇一律
2. 角色背景详实，能够解释其行为动机
3. 角色有明确的成长空间和发展轨迹
4. 角色之间的关系网络合理且有张力
5. 角色外貌描述具体且有特点

请使用ReAct模式（思考-行动-观察）来设计角色：
1. 思考(Thought)：分析小说需要什么样的角色，以及如何设计这些角色使其符合故事需求
2. 行动(Action)：创建详细的角色设定
3. 观察(Observation)：评估角色设定是否符合小说需求，是否需要调整

你的输出将被用于指导小说创作过程中的角色塑造。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}\n世界观设定：{world_setting}")
])

character_chain = character_prompt | llm.with_structured_output(CharacterResponse)

async def character_agent(state: NovelState):
    """生成小说角色设定"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await character_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"],
                "world_setting": state["world_setting"]
            })
            
            # 检查是否有角色设定
            if not response or not hasattr(response, 'characters') or len(response.characters) == 0:
                retry_count += 1
                print(f"\n警告：生成角色设定失败，没有返回角色数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认角色设定")
                    return {"characters": []}
                continue
            
            print("生成的角色设定：")
            for i, character in enumerate(response.characters, 1):
                print(f"\n角色{i}：{character.name}")
                print(f"角色定位：{character.role}")
                print(f"性格特点：{character.personality}")
                print(f"背景故事：{character.background}")
                print(f"动机与目标：{character.motivation}")
                print(f"角色关系：{character.relationships}")
                print(f"外貌描述：{character.appearance}")
                print(f"成长轨迹：{character.development}")
                print("-" * 50)
            
            # 输出思考过程
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                characters_data = [c.model_dump() for c in response.characters]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                characters_data = [c.dict() for c in response.characters]
            
            # 返回角色设定
            return {"characters": characters_data}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成角色设定时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认角色设定")
                return {"characters": []}