from langchain_core.runnables import RunnableConfig
from workflow import create_workflow

# 运行示例
async def main():
    # 创建工作流
    app = create_workflow()
    
    # 设置初始状态
    config = RunnableConfig()
    result = await app.ainvoke({
        "description": "一部关于人工智能获得自我意识的科幻小说",
        "chapters": [],
        "generated_chapters": [],
        "current_chapter_index": 0
    }, config)
    
    # 输出结果
    for idx, chapter in enumerate(result["generated_chapters"]):
        print(f"第{idx+1}章")
        print(chapter)
        print("---"*20)

# 运行
import asyncio
asyncio.run(main())