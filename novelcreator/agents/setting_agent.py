from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState
from typing import List

# 定义Pydantic模型
class Setting(BaseModel):
    name: str = Field(..., description="场景名称")
    location: str = Field(..., description="场景位置")
    time_period: str = Field(..., description="时间背景")
    atmosphere: str = Field(..., description="场景氛围")
    description: str = Field(..., description="详细描述")
    sensory_details: dict = Field(..., description="感官细节（视觉、听觉、嗅觉、触觉、味觉）")
    significance: str = Field(..., description="场景在故事中的意义")
    associated_characters: List[str] = Field(..., description="与场景相关的角色")
    objects: List[str] = Field(..., description="场景中的重要物品")
    chapter_placement: str = Field(..., description="建议放置的章节")

class SettingResponse(BaseModel):
    settings: List[Setting] = Field(..., description="生成的场景列表")
    thought: str = Field("", description="场景设计的思考过程")

# 场景生成Agent
setting_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的小说场景设计师，负责创建生动、沉浸式的场景和环境描述。

要求：
1. 基于小说标题、描述、大纲、世界观和角色设定，设计5-8个关键场景
2. 每个场景都应该有详细的环境描述，包括视觉、听觉、嗅觉、触觉和味觉等感官细节
3. 场景描述应该与故事情节和角色情感相呼应
4. 场景设计应该有助于塑造故事氛围和推动情节发展

请确保：
1. 场景与故事主题和世界观高度相关
2. 场景描述具体而生动，能够让读者身临其境
3. 场景设计考虑到不同时间段和季节的变化
4. 场景中包含能够反映角色心理状态的环境元素
5. 场景描述避免过度堆砌形容词，保持简洁有力

请使用ReAct模式（思考-行动-观察）来设计场景：
1. 思考(Thought)：分析小说需要什么样的场景，以及如何设计这些场景使其符合故事需求
2. 行动(Action)：创建详细的场景设定
3. 观察(Observation)：评估场景设定是否符合小说需求，是否需要调整

你的输出将被用于指导小说创作过程中的场景描写。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}\n世界观设定：{world_setting}\n角色设定：{characters}\n冲突设定：{conflicts}")
])

setting_chain = setting_prompt | llm.with_structured_output(SettingResponse)

async def setting_agent(state: NovelState):
    """生成小说场景设定"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 准备角色信息
            characters_info = ""
            for i, character in enumerate(state.get("characters", []), 1):
                characters_info += f"\n角色{i}：{character.get('name', '未命名')}\n"
                characters_info += f"角色定位：{character.get('role', '未知')}\n"
                characters_info += "-" * 30 + "\n"
                
            if not characters_info:
                characters_info = "暂无详细角色设定"
                
            # 准备冲突信息
            conflicts_info = ""
            for i, conflict in enumerate(state.get("conflicts", []), 1):
                conflicts_info += f"\n冲突{i}：{conflict.get('title', '未命名')}\n"
                conflicts_info += f"描述：{conflict.get('description', '未知')}\n"
                conflicts_info += "-" * 30 + "\n"
                
            if not conflicts_info:
                conflicts_info = "暂无详细冲突设定"
            
            response = await setting_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"],
                "world_setting": state["world_setting"],
                "characters": characters_info,
                "conflicts": conflicts_info
            })
            
            # 检查是否有场景设定
            if not response or not hasattr(response, 'settings') or len(response.settings) == 0:
                retry_count += 1
                print(f"\n警告：生成场景设定失败，没有返回场景数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认场景设定")
                    return {"settings": []}
                continue
            
            print("生成的场景设定：")
            for i, setting in enumerate(response.settings, 1):
                print(f"\n场景{i}：{setting.name}")
                print(f"位置：{setting.location}")
                print(f"时间背景：{setting.time_period}")
                print(f"氛围：{setting.atmosphere}")
                print(f"描述：{setting.description}")
                print(f"感官细节：")
                for sense, detail in setting.sensory_details.items():
                    print(f"  - {sense}：{detail}")
                print(f"意义：{setting.significance}")
                print(f"相关角色：{', '.join(setting.associated_characters)}")
                print(f"重要物品：{', '.join(setting.objects)}")
                print(f"建议章节：{setting.chapter_placement}")
                print("-" * 50)
            
            # 输出思考过程
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                settings_data = [s.model_dump() for s in response.settings]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                settings_data = [s.dict() for s in response.settings]
            
            # 返回场景设定
            return {"settings": settings_data}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成场景设定时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认场景设定")
                return {"settings": []}