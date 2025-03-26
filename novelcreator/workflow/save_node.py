from models.novel_saver import save_novel
from models.novel_state import NovelState

async def save_novel_node(state: NovelState):
    """
    保存小说节点，将生成的小说保存到data目录
    """
    # 获取小说信息
    description = state["description"]
    chapters = state["chapters"]
    generated_chapters = state["generated_chapters"]
    
    # 保存小说
    novel_dir = save_novel(description, chapters, generated_chapters)
    
    # 返回保存路径信息
    return {"novel_saved_path": novel_dir}