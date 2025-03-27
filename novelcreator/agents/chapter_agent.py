from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class Chapter(BaseModel):
    title: str = Field(..., description="章节标题")
    keywords: list[str] = Field(..., description="3-5个关键词")
    thought: str = Field("", description="章节的思考过程")
    action: str = Field("", description="基于思考采取的行动")
    observation: str = Field("", description="对生成内容的观察和评估")

class ChapterList(BaseModel):
    chapters: list[Chapter]

# ReAct模式的章节生成Agent
chapter_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的小说创作助手。使用ReAct模式（思考-行动-观察）来生成章节列表。

要求：
1. 生成指定数量的章节（{chapter_count}章）
2. 每个章节包含标题和3-5个关键词
3. 每个章节生成过程必须包含以下三个部分：
   - 思考(Thought)：分析前文内容，规划当前章节的主题和发展方向
   - 行动(Action)：基于思考结果生成章节标题和关键词
   - 观察(Observation)：评估生成的内容是否符合整体故事发展，是否需要调整

请确保：
1. 章节之间的连贯性和故事发展的合理性
2. 关键词能够反映章节的重要情节和主题
3. 整体结构符合小说的发展脉络
4. 每个章节的思考过程、行动和观察结果都要详细记录

开始生成前，请先思考整体故事架构。

你必须为每个章节提供完整的思考过程、行动和观察结果，这些将被保存在结构化输出中。"""),
    ("human", "小说描述：{description}")
])

chapter_chain = chapter_prompt | llm.with_structured_output(ChapterList)

async def chapter_agent(state: NovelState):
    """使用ReAct模式生成小说章节列表"""
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await chapter_chain.ainvoke({
                "description": state["description"],
                "chapter_count": state["chapter_count"]
            })
            
            # 检查是否有章节列表
            if not response or not hasattr(response, 'chapters') or len(response.chapters) == 0:
                retry_count += 1
                print(f"\n警告：生成章节列表失败，没有返回章节数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回空章节列表")
                    return {"chapters": []}
                continue
            
            print("生成的章节列表：")
            for i, chapter in enumerate(response.chapters, 1):
                print(f"\n第{i}章：{chapter.title}")
                print(f"关键词：{', '.join(chapter.keywords)}")
                if chapter.thought:
                    print(f"思考过程：{chapter.thought}")
                if chapter.action:
                    print(f"行动：{chapter.action}")
                if chapter.observation:
                    print(f"观察：{chapter.observation}")
                print("-" * 50)
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                chapters_data = [c.model_dump() for c in response.chapters]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                chapters_data = [c.dict() for c in response.chapters]
            
            # 确保返回的数据结构正确
            print(f"返回章节数据：{len(chapters_data)}章")
            # 直接返回chapters_data列表，而不是包装在字典中
            return {"chapters": chapters_data}
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成章节列表时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回空章节列表")
                return {"chapters": []}
