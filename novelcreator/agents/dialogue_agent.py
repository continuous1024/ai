from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState
from typing import List, Dict
import re

# 定义Pydantic模型
class DialogueSet(BaseModel):
    character: str = Field(..., description="说话的角色")
    dialogues: List[str] = Field(..., description="优化后的对话列表")
    tone: str = Field(..., description="对话语气")
    speech_patterns: List[str] = Field(..., description="特有的语言模式")
    context: str = Field(..., description="对话发生的场景或情境")

class DialogueResponse(BaseModel):
    dialogue_sets: List[DialogueSet] = Field(..., description="生成的对话集合")
    thought: str = Field("", description="对话优化的思考过程")

# 对话生成Agent
dialogue_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的小说对话设计师，负责创建自然、生动且符合角色特点的对话内容。

要求：
1. 基于小说角色设定和情节，为每个主要角色创建特色鲜明的对话风格
2. 对话应该反映角色的性格、背景、教育水平和社会地位
3. 对话应该推动情节发展，揭示角色关系和内心世界
4. 对话应该自然流畅，避免生硬和刻意

请确保：
1. 每个角色都有独特的语言习惯和表达方式
2. 对话符合角色的情感状态和所处情境
3. 对话中包含适当的口头禅、方言或特殊用语
4. 对话长度和节奏变化适当，避免过于冗长或简短
5. 对话中的潜台词和弦外之音能够增加故事深度

请使用ReAct模式（思考-行动-观察）来设计对话：
1. 思考(Thought)：分析角色需要什么样的对话风格，以及如何设计这些对话使其符合角色特点
2. 行动(Action)：创建详细的对话示例
3. 观察(Observation)：评估对话是否符合角色特点，是否需要调整

你的输出将被用于指导小说创作过程中的对话设计。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}\n世界观设定：{world_setting}\n角色设定：{characters}\n已有章节内容：{chapter_preview}")
])

dialogue_chain = dialogue_prompt | llm.with_structured_output(DialogueResponse)

# 对话提取函数
def extract_dialogues(chapter_content):
    """从章节内容中提取对话"""
    # 使用正则表达式匹配引号内的对话内容
    dialogue_pattern = r'["\'](.*?)["\']'
    dialogues = re.findall(dialogue_pattern, chapter_content)
    # 过滤掉空对话和过短的对话
    dialogues = [d.strip() for d in dialogues if len(d.strip()) > 3]
    return dialogues

async def dialogue_agent(state: NovelState):
    """生成小说对话设定"""
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
                characters_info += f"背景故事：{character.get('background', '未知')}\n"
                characters_info += f"动机与目标：{character.get('motivation', '未知')}\n"
                characters_info += f"语言特点：{character.get('speech_patterns', '未知')}\n"
                characters_info += "-" * 30 + "\n"
                
            if not characters_info:
                characters_info = "暂无详细角色设定"
            
            # 获取当前章节内容预览
            chapter_preview = state.get("current_chapter_content", "")
            if not chapter_preview:
                chapter_preview = "暂无章节内容"
            
            response = await dialogue_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"],
                "world_setting": state["world_setting"],
                "characters": characters_info,
                "chapter_preview": chapter_preview
            })
            
            # 检查是否有对话设定
            if not response or not hasattr(response, 'dialogue_sets') or len(response.dialogue_sets) == 0:
                retry_count += 1
                print(f"\n警告：生成对话设定失败，没有返回对话数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认对话设定")
                    return {"dialogues": []}
                continue
            
            print("生成的对话设定：")
            for i, dialogue_set in enumerate(response.dialogue_sets, 1):
                print(f"\n角色{i}：{dialogue_set.character}")
                print(f"对话语气：{dialogue_set.tone}")
                print(f"语言模式：{', '.join(dialogue_set.speech_patterns)}")
                print(f"对话情境：{dialogue_set.context}")
                print("对话示例：")
                for j, dialogue in enumerate(dialogue_set.dialogues, 1):
                    print(f"  {j}. {dialogue}")
                print("-" * 50)
            
            # 输出思考过程
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                dialogue_sets_data = [ds.model_dump() for ds in response.dialogue_sets]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                dialogue_sets_data = [ds.dict() for ds in response.dialogue_sets]
            
            # 返回对话设定
            return {"dialogues": dialogue_sets_data}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成对话设定时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认对话设定")
                return {"dialogues": []}