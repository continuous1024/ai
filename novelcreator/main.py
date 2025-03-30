from langchain_core.runnables import RunnableConfig
from workflow import create_workflow

# 运行示例
async def main():
    # 创建工作流
    chapter_count = 2  # 生成5章小说
    app = create_workflow()
    
    # 设置初始状态
    config = RunnableConfig()
    result = await app.ainvoke({
        "description": "一部关于斗罗大陆的同人小说，主角是男的，武魂是威能全失的主神空间",
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