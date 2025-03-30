from typing import Dict, TypedDict, List, Any

# 定义小说状态结构
class NovelState(TypedDict):
    description: str
    title: str
    outline: str
    world_setting: str  # 世界观设定
    chapters: List[Dict]
    generated_chapters: List[str]
    current_chapter_index: int
    chapter_count: int
    characters: List[Dict[str, Any]]  # 角色设定
    conflicts: List[Dict[str, Any]]  # 情节冲突
    settings: List[Dict[str, str]]  # 场景设定
    dialogues: Dict[str, List[str]]  # 优化的对话
    review_notes: List[str]  # 审查笔记