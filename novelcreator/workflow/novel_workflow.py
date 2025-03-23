from langgraph.graph import END, StateGraph
from models.novel_state import NovelState
from agents.chapter_agent import chapter_agent
from agents.content_agent import content_agent

# 构建工作流
def create_workflow():
    workflow = StateGraph(NovelState)

    # 添加节点
    workflow.add_node("generate_chapters", chapter_agent)
    workflow.add_node("generate_content", content_agent)

    # 设置初始节点
    workflow.set_entry_point("generate_chapters")

    # 定义流转逻辑
    def route_chapters(state: NovelState):
        if "chapters" in state and len(state["chapters"]) > 0:
            return "generate_content"
        return END

    workflow.add_conditional_edges(
        "generate_chapters",
        route_chapters
    )

    # 定义章节生成循环
    def should_continue(state: NovelState):
        if state["current_chapter_index"] < len(state["chapters"]):
            return "generate_content"
        return END

    workflow.add_conditional_edges(
        "generate_content",
        should_continue
    )

    # 编译执行
    return workflow.compile()