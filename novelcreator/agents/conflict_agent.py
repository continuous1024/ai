from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState
from typing import List

# 定义Pydantic模型
class Conflict(BaseModel):
    title: str = Field(..., description="冲突标题")
    type: str = Field(..., description="冲突类型（内部冲突/外部冲突/环境冲突等）")
    description: str = Field(..., description="冲突详细描述")
    involved_characters: List[str] = Field(..., description="涉及的角色")
    trigger: str = Field(..., description="冲突触发条件")
    escalation: str = Field(..., description="冲突升级过程")
    climax: str = Field(..., description="冲突高潮")
    resolution: str = Field(..., description="冲突解决方式")
    chapter_placement: str = Field(..., description="建议放置的章节")
    impact: str = Field(..., description="对故事和角色的影响")

class ConflictResponse(BaseModel):
    conflicts: List[Conflict] = Field(..., description="生成的冲突列表")
    thought: str = Field("", description="冲突设计的思考过程")

# 冲突生成Agent
conflict_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的小说冲突设计师，负责创建引人入胜的情节冲突和转折点。

要求：
1. 基于小说标题、描述、大纲、世界观和角色设定，设计3-5个关键冲突
2. 每个冲突都应该有明确的起因、发展、高潮和解决方式
3. 冲突应该推动故事发展，并促进角色成长
4. 冲突类型应该多样化，包括内部冲突、人际冲突、环境冲突等

请确保：
1. 冲突与故事主题和世界观高度相关
2. 冲突能够测试角色的能力、信念或价值观
3. 冲突的解决方式符合角色性格和故事逻辑
4. 冲突的安排有节奏感，避免平铺直叙
5. 冲突的设计为故事高潮和结局做好铺垫

请使用ReAct模式（思考-行动-观察）来设计冲突：
1. 思考(Thought)：分析小说需要什么样的冲突，以及如何设计这些冲突使其符合故事需求
2. 行动(Action)：创建详细的冲突设定
3. 观察(Observation)：评估冲突设定是否符合小说需求，是否需要调整

你的输出将被用于指导小说创作过程中的情节设计。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}\n世界观设定：{world_setting}\n角色设定：{characters}")
])

conflict_chain = conflict_prompt | llm.with_structured_output(ConflictResponse)

async def conflict_agent(state: NovelState):
    """生成小说冲突设定"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 准备角色信息
            characters_info = ""
            for i, character in enumerate(state.get("characters", []), 1):
                characters_info += f"\n角色{i}：{character.get('name', '未命名')}\n"
                characters_info += f"角色定位：{character.get('role', '未知')}\n"
                characters_info += f"性格特点：{character.get('personality', '未知')}\n"
                characters_info += f"动机与目标：{character.get('motivation', '未知')}\n"
                characters_info += "-" * 30 + "\n"
                
            if not characters_info:
                characters_info = "暂无详细角色设定"
            
            response = await conflict_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"],
                "world_setting": state["world_setting"],
                "characters": characters_info
            })
            
            # 检查是否有冲突设定
            if not response or not hasattr(response, 'conflicts') or len(response.conflicts) == 0:
                retry_count += 1
                print(f"\n警告：生成冲突设定失败，没有返回冲突数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认冲突设定")
                    return {"conflicts": []}
                continue
            
            print("生成的冲突设定：")
            for i, conflict in enumerate(response.conflicts, 1):
                print(f"\n冲突{i}：{conflict.title}")
                print(f"类型：{conflict.type}")
                print(f"描述：{conflict.description}")
                print(f"涉及角色：{', '.join(conflict.involved_characters)}")
                print(f"触发条件：{conflict.trigger}")
                print(f"升级过程：{conflict.escalation}")
                print(f"冲突高潮：{conflict.climax}")
                print(f"解决方式：{conflict.resolution}")
                print(f"建议章节：{conflict.chapter_placement}")
                print(f"影响：{conflict.impact}")
                print("-" * 50)
            
            # 输出思考过程
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                conflicts_data = [c.model_dump() for c in response.conflicts]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                conflicts_data = [c.dict() for c in response.conflicts]
            
            # 返回冲突设定
            return {"conflicts": conflicts_data}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成冲突设定时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认冲突设定")
                return {"conflicts": []}