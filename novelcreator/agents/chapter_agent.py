from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class Chapter(BaseModel):
    title: str = Field(..., description="章节标题")
    keywords: list[str] = Field(..., description="3-5个关键词")

class ChapterList(BaseModel):
    chapters: list[Chapter]

# 章节生成Agent
chapter_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的小说创作助手。根据用户提供的小说描述，生成章节列表。
要求：
1. 包含多个章节
2. 每个章节包含标题和3-5个关键词"""),
    ("human", "小说描述：{description}")
])

chapter_chain = chapter_prompt | llm.with_structured_output(ChapterList)

async def chapter_agent(state: NovelState):
    """生成小说章节列表"""
    response = await chapter_chain.ainvoke({
        "description": state["description"]
    })
    return {"chapters": [c.dict() for c in response.chapters]}
