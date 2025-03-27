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
        "description": "一部关于人工智能获得自我意识的科幻小说",
        "chapters": [],
        "generated_chapters": [],
        "current_chapter_index": 0,
        "chapter_count": chapter_count
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