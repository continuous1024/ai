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

# 补充内容生成的提示模板
supplement_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深小说家，请基于已有内容继续补充当前章节，使其更加丰富和完整：

已有章节内容：{existing_content}
当前章节标题：{chapter_title}
当前正在生成：第{current_chapter_index}章

请补充内容，确保：
1. 与已有内容保持一致的风格和语调
2. 内容自然衔接，不重复已有内容
3. 补充更多细节、对话或情节发展
4. 补充内容应该是已有内容的延续，而不是新的章节

你需要补充至少{min_words}字的内容。"""),
])

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
5. 章节内容必须不少于5000字，为确保字数达标，请采取以下策略：
   - 详细描述场景和人物心理活动
   - 增加对话和互动细节
   - 适当扩展支线情节
   - 在观察阶段主动检查字数，不足时继续补充内容

你必须提供完整的思考过程、行动和观察结果，这些将被保存在结构化输出中。"""),
])

content_chain = content_prompt | llm.with_structured_output(ContentResponse)
supplement_chain = supplement_prompt | llm.with_structured_output(ContentResponse)

async def generate_content_with_min_length(previous_content, current_chapter, chapter_title, current_chapter_index, min_length=5000, max_attempts=3):
    """分段生成内容，确保达到最小字数要求"""
    # 初始内容生成
    response = await content_chain.ainvoke({
        "previous_chapter": previous_content,
        "current_chapter": current_chapter,
        "chapter_title": chapter_title,
        "current_chapter_index": current_chapter_index
    })
    
    # 检查response是否有效
    if response is None or not hasattr(response, 'content') or not response.content.strip():
        print(f"\n警告：生成内容失败，返回空响应")
        return None
    
    # 初始内容
    full_content = response.content
    thought = response.thought if hasattr(response, 'thought') else ""
    action = response.action if hasattr(response, 'action') else ""
    observation = response.observation if hasattr(response, 'observation') else ""
    
    # 如果内容长度不足，进行补充
    attempt = 0
    while len(full_content) < min_length and attempt < max_attempts:
        attempt += 1
        print(f"\n当前内容字数：{len(full_content)}，不足{min_length}字，正在进行第{attempt}次补充...")
        
        try:
            # 计算还需要补充的字数
            words_needed = min_length - len(full_content)
            
            # 调用补充内容的链
            supplement_response = await supplement_chain.ainvoke({
                "existing_content": full_content,
                "chapter_title": chapter_title,
                "current_chapter_index": current_chapter_index,
                "min_words": words_needed
            })
            
            # 检查补充内容是否有效
            if supplement_response and hasattr(supplement_response, 'content') and supplement_response.content.strip():
                # 合并内容
                full_content += "\n\n" + supplement_response.content
                
                # 更新思考过程
                if hasattr(supplement_response, 'thought') and supplement_response.thought:
                    thought += "\n补充内容思考：" + supplement_response.thought
                if hasattr(supplement_response, 'action') and supplement_response.action:
                    action += "\n补充内容行动：" + supplement_response.action
                if hasattr(supplement_response, 'observation') and supplement_response.observation:
                    observation += "\n补充内容观察：" + supplement_response.observation
                
                print(f"补充后内容字数：{len(full_content)}")
            else:
                print(f"补充内容失败，尝试下一次补充")
        except Exception as e:
            print(f"补充内容时发生错误：{str(e)}")
    
    # 创建完整的响应对象
    complete_response = ContentResponse(
        content=full_content,
        thought=thought,
        action=action,
        observation=observation
    )
    
    return complete_response

async def content_agent(state: NovelState):
    """使用ReAct模式生成小说章节内容"""
    current_chapter = state["chapters"][state["current_chapter_index"]]
    previous_content = state["generated_chapters"][-1] if state["generated_chapters"] else ""
    chapter_title = current_chapter.get("title", f"第{state['current_chapter_index']+1}章")
    
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 使用分段生成函数来确保内容达到5000字
            response = await generate_content_with_min_length(
                previous_content=previous_content,
                current_chapter=current_chapter,
                chapter_title=chapter_title,
                current_chapter_index=state['current_chapter_index'] + 1,
                min_length=3000,
                max_attempts=3
            )
            
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
                
            # 检查生成内容的字数是否达到5000字
            if len(response.content) < 3000:
                retry_count += 1
                print(f"\n警告：生成第{state['current_chapter_index']+1}章内容字数不足5000字（当前字数：{len(response.content)}）。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，使用当前生成的内容")
                else:
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