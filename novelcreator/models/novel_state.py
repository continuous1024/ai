from typing import Dict, TypedDict, List

# 定义小说状态结构
class NovelState(TypedDict):
    description: str
    chapters: List[Dict]
    generated_chapters: List[str]
    current_chapter_index: int