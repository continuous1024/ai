from langchain_core.prompts import ChatPromptTemplate
from models.llm import llm
from models.novel_state import NovelState

# 章节内容生成Agent
content_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深小说家，请根据以下信息续写小说章节：
已生成章节：{previous_chapter}
当前章节信息：{current_chapter}
请保持：1. 语言风格一致 2. 剧情连贯 3. 适当使用伏笔"""),
])

content_chain = content_prompt | llm

async def content_agent(state: NovelState):
    """生成小说章节内容"""
    current_chapter = state["chapters"][state["current_chapter_index"]]
    previous_content = state["generated_chapters"][-1] if state["generated_chapters"] else ""
    
    response = await content_chain.ainvoke({
        "previous_chapter": previous_content,
        "current_chapter": current_chapter
    })
    
    return {
        "generated_chapters": state["generated_chapters"] + [response.content],
        "current_chapter_index": state["current_chapter_index"] + 1
    }