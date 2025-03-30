import os
import json
from typing import List, Dict
import re

def generate_novel_title(description: str) -> str:
    """
    根据小说描述生成小说标题
    """
    # 从描述中提取关键词作为标题
    # 这里使用简单的方法，实际项目中可以使用LLM生成更好的标题
    words = description.split()
    if len(words) > 3:
        title = "".join(words[:3])
    else:
        title = description
    
    # 清理标题，移除特殊字符
    title = re.sub(r'[^\w\s]', '', title)
    title = title.strip()
    
    # 如果标题为空，使用默认标题
    if not title:
        title = "未命名小说"
    
    return title

def save_novel(title: str, description: str, outline: str, world_setting: str, chapters: List[Dict], generated_chapters: List[str]) -> str:
    """
    保存小说到data目录
    
    Args:
        description: 小说描述
        chapters: 章节信息列表
        generated_chapters: 生成的章节内容列表
        
    Returns:
        保存路径
    """
    # 使用传入的标题
    novel_title = title
    
    # 创建保存目录
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    novel_dir = os.path.join(base_dir, novel_title)
    
    # 确保目录存在
    os.makedirs(novel_dir, exist_ok=True)
    
    # 保存小说信息
    info = {
        "title": novel_title,
        "description": description,
        "outline": outline,
        "world_setting": world_setting,
        "chapter_count": len(chapters)
    }
    
    with open(os.path.join(novel_dir, "info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    # 保存章节信息
    with open(os.path.join(novel_dir, "chapters.json"), "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)
    
    # 保存完整小说内容
    full_content = f"# {novel_title}\n\n"
    full_content += f"## 简介\n{description}\n\n"
    full_content += f"## 大纲\n{outline}\n\n"
    full_content += f"## 世界观设定\n{world_setting}\n\n"
    
    for i, (chapter_info, chapter_content) in enumerate(zip(chapters, generated_chapters)):
        chapter_title = chapter_info.get("title", f"第{i+1}章")
        full_content += f"## {chapter_title}\n{chapter_content}\n\n"
        
        # 单独保存每个章节
        chapter_filename = f"chapter_{i+1:02d}.txt"
        with open(os.path.join(novel_dir, chapter_filename), "w", encoding="utf-8") as f:
            f.write(f"# {chapter_title}\n\n{chapter_content}")
    
    # 保存完整小说
    with open(os.path.join(novel_dir, "full_novel.md"), "w", encoding="utf-8") as f:
        f.write(full_content)
    
    return novel_dir