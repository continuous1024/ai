from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from models.llm import llm
from models.novel_state import NovelState
from typing import List

# 定义Pydantic模型
class ReviewIssue(BaseModel):
    issue_type: str = Field(..., description="问题类型（情节漏洞/角色不一致/逻辑错误/其他）")
    description: str = Field(..., description="问题描述")
    location: str = Field(..., description="问题位置（章节）")
    severity: str = Field(..., description="严重程度（高/中/低）")
    suggestion: str = Field(..., description="修改建议")

class ReviewResponse(BaseModel):
    issues: List[ReviewIssue] = Field(..., description="发现的问题列表")
    overall_quality: str = Field(..., description="整体质量评价")
    strengths: List[str] = Field(..., description="小说优点")
    improvement_areas: List[str] = Field(..., description="可改进的方面")
    thought: str = Field("", description="审查过程的思考")

# 审查Agent
review_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位专业的小说审查编辑，负责检查小说的连贯性、一致性和逻辑性，找出可能的错误和漏洞。

要求：
1. 仔细阅读整部小说，包括标题、大纲、世界观设定和所有章节内容
2. 检查情节连贯性、角色一致性、逻辑合理性和细节准确性
3. 找出所有可能的问题，包括情节漏洞、角色行为不一致、逻辑错误等
4. 为每个问题提供具体的修改建议

请确保：
1. 审查全面而细致，不放过任何可能的问题
2. 问题描述具体而非泛泛而谈
3. 修改建议具有可操作性
4. 同时指出小说的优点和亮点
5. 提供整体质量评价和改进方向

请使用ReAct模式（思考-行动-观察）来进行审查：
1. 思考(Thought)：分析小说可能存在的问题，以及如何发现这些问题
2. 行动(Action)：仔细检查小说内容，找出所有问题
3. 观察(Observation)：评估发现的问题是否准确，修改建议是否合理

你的输出将被用于指导小说的最终修改和完善。"""),
    ("human", "小说标题：{title}\n小说描述：{description}\n小说大纲：{outline}\n世界观设定：{world_setting}\n角色设定：{characters}\n章节内容：\n{chapters_content}")
])

review_chain = review_prompt | llm.with_structured_output(ReviewResponse)

async def review_agent(state: NovelState):
    """审查小说内容，找出问题和改进点"""
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 准备角色信息
            characters_info = ""
            for i, character in enumerate(state.get("characters", []), 1):
                characters_info += f"\n角色{i}：{character.get('name', '未命名')}\n"
                characters_info += f"角色定位：{character.get('role', '未知')}\n"
                characters_info += f"性格特点：{character.get('personality', '未知')}\n"
                characters_info += "-" * 30 + "\n"
                
            if not characters_info:
                characters_info = "暂无详细角色设定"
                
            # 准备章节内容（可能需要截断以适应模型上下文长度限制）
            chapters_content = ""
            for i, chapter in enumerate(state["generated_chapters"], 1):
                # 为了避免超出模型上下文长度，可能需要只包含章节的开头和结尾
                chapter_preview = chapter[:1000] + "..." + chapter[-1000:] if len(chapter) > 2000 else chapter
                chapters_content += f"\n第{i}章预览：\n{chapter_preview}\n\n"
                
            response = await review_chain.ainvoke({
                "title": state["title"],
                "description": state["description"],
                "outline": state["outline"],
                "world_setting": state["world_setting"],
                "characters": characters_info,
                "chapters_content": chapters_content
            })
            
            # 检查是否有审查结果
            if not response or not hasattr(response, 'issues'):
                retry_count += 1
                print(f"\n警告：生成审查结果失败，没有返回审查数据。正在进行第{retry_count}次重试...")
                if retry_count >= max_retries:
                    print("达到最大重试次数，返回默认审查结果")
                    return {"review_notes": ["审查失败，未能生成有效的审查结果"]}
                continue
            
            print("\n小说审查结果：")
            print(f"整体质量评价：{response.overall_quality}")
            
            print("\n小说优点：")
            for i, strength in enumerate(response.strengths, 1):
                print(f"{i}. {strength}")
                
            print("\n需要改进的方面：")
            for i, area in enumerate(response.improvement_areas, 1):
                print(f"{i}. {area}")
                
            print("\n发现的具体问题：")
            for i, issue in enumerate(response.issues, 1):
                print(f"\n问题{i}：")
                print(f"类型：{issue.issue_type}")
                print(f"描述：{issue.description}")
                print(f"位置：{issue.location}")
                print(f"严重程度：{issue.severity}")
                print(f"修改建议：{issue.suggestion}")
                print("-" * 50)
            
            # 输出思考过程
            if hasattr(response, 'thought') and response.thought:
                print(f"思考过程：{response.thought}")
            
            # 使用model_dump()方法替代dict()方法，确保正确序列化Pydantic模型
            try:
                # 尝试使用新版Pydantic的model_dump方法
                issues_data = [issue.model_dump() for issue in response.issues]
            except AttributeError:
                # 如果失败，回退到旧版的dict方法
                issues_data = [issue.dict() for issue in response.issues]
            
            # 返回审查结果
            return {
                "review_notes": issues_data,
                "overall_quality": response.overall_quality,
                "strengths": response.strengths,
                "improvement_areas": response.improvement_areas
            }
        except Exception as e:
            retry_count += 1
            print(f"\n警告：生成审查结果时发生错误：{str(e)}。正在进行第{retry_count}次重试...")
            if retry_count >= max_retries:
                print("达到最大重试次数，返回默认审查结果")
                return {"review_notes": ["审查失败，未能生成有效的审查结果"]}