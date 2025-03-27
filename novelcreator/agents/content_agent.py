from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState

# 定义Pydantic模型
class ContentResponse(BaseModel):
    content: str = Field(..., description="生成的章节内容")
    thought: str = Field("", description="章节内容的思考过程")
    action: str = Field("", description="基于思考采取的行动")
    observation: str = Field("", description="对生成内容的观察和评估")

# 章节内容生成Agent（使用ReAct模式）
content_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深小说家，请使用ReAct模式（思考-行动-观察）来续写小说章节：

已生成章节：{previous_chapter}
当前章节信息：{current_chapter}
当前章节标题：{chapter_title}
当前正在生成：第{current_chapter_index}章

请按照以下三个步骤生成内容：
1. 思考(Thought)：分析前文内容，规划当前章节的发展方向、人物情感变化和情节走向
2. 行动(Action)：基于思考结果，撰写当前第{current_chapter_index}章内容，确保以章节标题开始，并明确描述当前章节内容，而非下一章
3. 观察(Observation)：评估生成的内容是否符合整体故事发展，是否需要调整

请确保：
1. 语言风格一致
2. 剧情连贯
3. 适当使用伏笔
4. 每个步骤的思考过程、行动和观察结果都要详细记录

你必须提供完整的思考过程、行动和观察结果，这些将被保存在结构化输出中。"""),
])

content_chain = content_prompt | llm.with_structured_output(ContentResponse)

async def content_agent(state: NovelState):
    """使用ReAct模式生成小说章节内容"""
    current_chapter = state["chapters"][state["current_chapter_index"]]
    previous_content = state["generated_chapters"][-1] if state["generated_chapters"] else ""
    chapter_title = current_chapter.get("title", f"第{state['current_chapter_index']+1}章")
    
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = await content_chain.ainvoke({
                "previous_chapter": previous_content,
                "current_chapter": current_chapter,
                "chapter_title": chapter_title,
                "current_chapter_index": state['current_chapter_index'] + 1
            })
            
            # 检查response是否为None或内容为空
            if response is None or not hasattr(response, 'content') or not response.content.strip():
                retry_count += 1
                print(f"\n警告：生成第{state['current_chapter_index']+1}章内容失败，返回空响应。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认内容")
                    return {
                        "generated_chapters": state["generated_chapters"] + [f"第{state['current_chapter_index']+1}章：{chapter_title}\n\n(内容生成失败，请重试)"],
                        "current_chapter_index": state["current_chapter_index"] + 1,
                        "chapters": state["chapters"]
                    }
                continue
            
            # 输出思考过程
            print(f"\n生成第{state['current_chapter_index']+1}章内容：")
            print(f"章节标题：{chapter_title}")
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            if hasattr(response, 'action') and response.action:
                print(f"行动：{response.action}")
            if hasattr(response, 'observation') and response.observation:
                print(f"观察：{response.observation}")
            print("-" * 50)
            
            # 更新章节信息，同时保存思考过程
            current_chapter["thought"] = response.thought if hasattr(response, 'thought') else ""
            current_chapter["action"] = response.action if hasattr(response, 'action') else ""
            current_chapter["observation"] = response.observation if hasattr(response, 'observation') else ""
            
            return {
                "generated_chapters": state["generated_chapters"] + [response.content],
                "current_chapter_index": state["current_chapter_index"] + 1,
                "chapters": state["chapters"] # 更新包含思考过程的章节列表
            }
            
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成第{state['current_chapter_index']+1}章内容时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认内容")
                return {
                    "generated_chapters": state["generated_chapters"] + [f"第{state['current_chapter_index']+1}章：{chapter_title}\n\n(内容生成失败，请重试)"],
                    "current_chapter_index": state["current_chapter_index"] + 1,
                    "chapters": state["chapters"]
                }