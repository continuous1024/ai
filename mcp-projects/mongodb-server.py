from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base


import logging
# logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    mongo_url = 'mongodb://admin:Abc123__@localhost:27017/?authMechanism=SCRAM-SHA-256&authSource=admin'
    logging.debug(f"Connecting to MongoDB at {mongo_url}")
    mongo_client = AsyncIOMotorClient(mongo_url)
    try:
        await mongo_client.admin.command('ping')
        logging.debug("MongoDB connection successful")
        db = mongo_client.get_database('bigdata')
        yield {"db": db}
    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
        raise
    finally:
        mongo_client.close()


mcp = FastMCP(
    "MyCompanyDataServer",
    dependencies=["motor"],
    lifespan=app_lifespan
)


# # ------------------------------
# # 资源：列出所有集合名称
# # schema://collections
# # ------------------------------
# @mcp.resource("schema://collections")
# async def list_collections() -> list[str]:
#     mongo_url = 'mongodb://admin:Abc123__@localhost:27017/?authMechanism=SCRAM-SHA-256&authSource=admin'
#     mongo_client = AsyncIOMotorClient(mongo_url)
#     db = mongo_client.get_database('bigdata')
#     try:
#         collections = await db.list_collection_names()
#     finally:
#         mongo_client.close()
#     return collections


# # ------------------------------
# # 资源：获取指定集合的字段列表
# # schema://{collection}
# # ------------------------------
# @mcp.resource("schema://{collection}")
# async def get_collection_schema(collection: str) -> dict:
#     """返回指定集合的模式信息，例如字段列表"""
#     mongo_url = 'mongodb://admin:Abc123__@localhost:27017/?authMechanism=SCRAM-SHA-256&authSource=admin'
#     mongo_client = AsyncIOMotorClient(mongo_url)
#     db = mongo_client.get_database('bigdata')
#     try:
#         doc = await db[collection].find_one()
#         if not doc:
#             return {"fields": []}
#         return {"fields": list(doc.keys())}
#     finally:
#         mongo_client.close()


# ------------------------------
# 工具：对 MongoDB 集合执行只读 SQL 查询
# ------------------------------
@mcp.tool()
async def run_sql_query(
    ctx: Context, collection: str, query: dict
) -> list[dict]:
    db = ctx.request_context.lifespan_context["db"]
    return await db[collection].find(query).to_list(length=None)


# ------------------------------
# Prompt：常见数据分析任务
# ------------------------------
@mcp.prompt()
def summarize_collection(collection: str) -> str:
    """提示：对集合进行汇总统计"""
    return (
        f"请对集合 `{collection}` 中的数据进行汇总统计，"
        "包括记录总数、各字段的分布情况，以及缺失值统计。"
    )


@mcp.prompt()
def descriptive_statistics(query_result: list[dict]) -> list[base.Message]:
    """提示：生成描述性统计报告"""
    text = f"以下是查询结果：\n{query_result}"
    return [
        base.UserMessage("请基于以下数据，生成一份描述性统计报告，包含均值、中位数、标准差等指标："),
        base.UserMessage(text),
    ]


@mcp.prompt()
def generate_visualization(query_result: list[dict]) -> list[base.Message]:
    """提示：给出可视化建议并生成示例代码"""
    text = f"以下是查询结果：\n{query_result}"
    return [
        base.UserMessage(
            "请基于以下数据，给出可视化图表的建议，并提供使用 matplotlib 的示例代码："
        ),
        base.UserMessage(text),
    ]


if __name__ == "__main__":
    mcp.run()
