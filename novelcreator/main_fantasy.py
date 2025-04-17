from langchain_core.runnables import RunnableConfig
from workflow import create_workflow

# 运行示例
async def main():
    # 创建工作流
    chapter_count = 20  # 设置为20章，更适合一个完整的玄幻小说
    app = create_workflow()
    
    # 设置初始状态
    config = RunnableConfig()
    result = await app.ainvoke({
        "description": "创建一本中国风玄幻小说，讲述一个普通山村少年意外获得上古仙人传承，开始了修仙问道之路。在这个世界中，有着各种宗门势力，灵兽妖兽，天材地宝，以及神秘的上古遗迹。主角通过自己的努力和机缘，逐渐成长为一代强者，同时揭开了仙人传承背后的秘密，以及自己身世之谜。小说应当包含精彩的修炼场景、激烈的战斗描写、错综复杂的人物关系，以及深厚的东方文化底蕴。",
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