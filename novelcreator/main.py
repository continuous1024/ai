from langchain_core.runnables import RunnableConfig
from workflow import create_workflow

# 运行示例
async def main():
    # 创建工作流
    chapter_count = 100
    app = create_workflow()
    
    # 设置初始状态
    config = RunnableConfig()
    result = await app.ainvoke({
        "description": "创建一本诸天流小说，主角是一位普通大学生，获得了穿梭各个经典小说、影视、游戏世界的能力。每到一个世界都会获得该世界的某种能力或物品，并将其带回现实或下一个世界。主角在穿越过程中逐渐发现各个世界之间存在某种神秘联系，背后似乎有一个更大的阴谋。请设计丰富的世界观、有趣的穿越规则和成长路线。",
        "title": "",
        "outline": "",
        "world_setting": "",
        "chapters": [],
        "generated_chapters": [],
        "current_chapter_index": 0,
        "chapter_count": chapter_count,
        "characters": [],
        "conflicts": [],
        "settings": [],
        "dialogues": {},
        "review_notes": []
    }, config)
    
    # 输出结果
    for idx, chapter in enumerate(result["generated_chapters"]):
        print(f"第{idx+1}章")
        print(chapter)
        print("---"*20)
    
    # 输出保存路径
    if "novel_saved_path" in result:
        print(f"\n小说已保存到: {result['novel_saved_path']}")
        print(f"完整小说文件: {result['novel_saved_path']}/full_novel.md")

# 运行
import asyncio
asyncio.run(main())