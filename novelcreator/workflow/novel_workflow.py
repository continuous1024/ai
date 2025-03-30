from langgraph.graph import END, StateGraph
from models.novel_state import NovelState
from agents.title_agent import title_agent
from agents.outline_agent import outline_agent
from agents.world_agent import world_agent
from agents.character_agent import character_agent
from agents.conflict_agent import conflict_agent
from agents.setting_agent import setting_agent
from agents.chapter_agent import chapter_agent
from agents.content_agent import content_agent
from agents.dialogue_agent import dialogue_agent
from agents.review_agent import review_agent
from models.novel_saver import save_novel
from workflow.save_node import save_novel_node

# 构建工作流
def create_workflow():
    workflow = StateGraph(NovelState)

    # 添加节点
    workflow.add_node("generate_title", title_agent)
    workflow.add_node("generate_outline", outline_agent)
    workflow.add_node("generate_world", world_agent)
    workflow.add_node("generate_characters", character_agent)
    workflow.add_node("generate_conflicts", conflict_agent)
    workflow.add_node("generate_settings", setting_agent)
    workflow.add_node("generate_chapters", chapter_agent)
    workflow.add_node("generate_content", content_agent)
    workflow.add_node("optimize_dialogues", dialogue_agent)
    workflow.add_node("review_novel", review_agent)

    # 设置初始节点
    workflow.set_entry_point("generate_title")

    # 定义标题生成后的流转逻辑
    def route_title(state: NovelState):
        if "title" in state and state["title"]:
            return "generate_outline"
        return END

    workflow.add_conditional_edges(
        "generate_title",
        route_title
    )
    
    # 定义大纲生成后的流转逻辑
    def route_outline(state: NovelState):
        if "outline" in state and state["outline"]:
            return "generate_world"
        return END

    workflow.add_conditional_edges(
        "generate_outline",
        route_outline
    )
    
    # 定义世界观生成后的流转逻辑
    def route_world(state: NovelState):
        if "world_setting" in state and state["world_setting"]:
            return "generate_characters"
        return END

    workflow.add_conditional_edges(
        "generate_world",
        route_world
    )
    
    # 定义角色生成后的流转逻辑
    def route_characters(state: NovelState):
        if "characters" in state and len(state["characters"]) > 0:
            return "generate_conflicts"
        return "generate_conflicts"  # 即使没有角色也继续流程

    workflow.add_conditional_edges(
        "generate_characters",
        route_characters
    )
    
    # 定义冲突生成后的流转逻辑
    def route_conflicts(state: NovelState):
        if "conflicts" in state and len(state["conflicts"]) > 0:
            return "generate_settings"
        return "generate_settings"  # 即使没有冲突也继续流程

    workflow.add_conditional_edges(
        "generate_conflicts",
        route_conflicts
    )
    
    # 定义场景生成后的流转逻辑
    def route_settings(state: NovelState):
        if "settings" in state and len(state["settings"]) > 0:
            return "generate_chapters"
        return "generate_chapters"  # 即使没有场景也继续流程

    workflow.add_conditional_edges(
        "generate_settings",
        route_settings
    )
    
    # 定义章节生成后的流转逻辑
    def route_chapters(state: NovelState):
        if "chapters" in state and len(state["chapters"]) > 0:
            return "generate_content"
        return END

    workflow.add_conditional_edges(
        "generate_chapters",
        route_chapters
    )

    # 添加保存节点
    workflow.add_node("save_novel", save_novel_node)
    
    # 定义章节生成循环
    def should_continue(state: NovelState):
        if state["current_chapter_index"] < len(state["chapters"]):
            return "generate_content"
        return "optimize_dialogues"

    workflow.add_conditional_edges(
        "generate_content",
        should_continue
    )
    
    # 定义对话优化后的流转逻辑
    def route_dialogues(state: NovelState):
        if "dialogues" in state and len(state["dialogues"]) > 0:
            return "review_novel"
        return "review_novel"  # 即使没有优化对话也继续流程

    workflow.add_conditional_edges(
        "optimize_dialogues",
        route_dialogues
    )
    
    # 定义小说审查后的流转逻辑
    def route_review(state: NovelState):
        if "review_notes" in state and len(state["review_notes"]) > 0:
            return "save_novel"
        return "save_novel"  # 即使没有审查笔记也继续流程

    workflow.add_conditional_edges(
        "review_novel",
        route_review
    )
    
    # 保存完成后结束
    workflow.add_edge("save_novel", END)

    # 编译执行
    return workflow.compile()