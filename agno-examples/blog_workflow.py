import json
from textwrap import dedent
from typing import Dict, Iterator, Optional

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.deepseek import DeepSeek
from agno.models.openrouter import OpenRouter
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow import RunEvent, RunResponse, Workflow
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )


class SearchResults(BaseModel):
    articles: list[NewsArticle]


class ScrapedArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(
        ..., description="Summary of the article if available."
    )
    content: Optional[str] = Field(
        ...,
        description="Full article content in markdown format. None if content is unavailable.",
    )


class BlogPostGenerator(Workflow):
    """Advanced workflow for generating professional blog posts with proper research and citations."""

    description: str = dedent("""\
    一个智能博客文章生成器，可创建引人入胜、研究充分的内容。
    该工作流程协调多个AI代理来研究、分析和制作
    引人入胜的博客文章，将新闻严谨性与吸引人的叙事相结合。
    该系统擅长创建既具有信息性又针对数字消费进行优化的内容。
    """)

    # Search Agent: Handles intelligent web searching and source gathering
    searcher: Agent = Agent(
        # model=OpenAIChat(id="gpt-4o-mini"),
        # model=Gemini(id="gemini-2.0-flash"),
        # model=Ollama(id="qwen3:4b"),
        model=OpenRouter(id="gpt-4o"),
        # model=DeepSeek(id="deepseek-chat"),
        # model=DeepSeek(id="deepseek-reasoner")
        tools=[DuckDuckGoTools()],
        description=dedent("""\
        你是博客研究专家，一位精英研究助手，专门发现
        高质量的引人入胜的博客内容来源。你的专业知识包括：

        - 寻找权威和趋势来源
        - 评估内容可信度和相关性
        - 识别多样化的观点和专家意见
        - 发现独特的角度和见解
        - 确保全面的主题覆盖\
        """),
        instructions=dedent("""\
        1. 搜索策略 🔍
           - 找到10-15个相关来源并选择5-7个最佳来源
           - 优先考虑最新、权威的内容
           - 寻找独特的角度和专家见解
        2. 来源评估 📊
           - 验证来源的可信度和专业知识
           - 检查发布日期的时效性
           - 评估内容深度和独特性
        3. 观点多样性 🌐
           - 包含不同的观点
           - 收集主流和专家意见
           - 寻找支持数据和统计信息
        4. 以中文生成回复\
        """),
        response_model=SearchResults,
    )

    # Content Scraper: Extracts and processes article content
    article_scraper: Agent = Agent(
        # model=OpenAIChat(id="gpt-4o-mini"),
        # model=Gemini(id="gemini-2.0-flash"),
        # model=Ollama(id="qwen3:4b"),
        model=OpenRouter(id="gpt-4o"),
        # model=DeepSeek(id="deepseek-chat"),
        # model=DeepSeek(id="deepseek-reasoner")
        tools=[Newspaper4kTools()],
        description=dedent("""\
        你是内容机器人，一位专门提取和处理数字内容的专家
        用于博客创作。你的专业知识包括：

        - 高效的内容提取
        - 智能格式化和结构化
        - 关键信息识别
        - 引用和统计数据保存
        - 维护来源归属\
        """),
        instructions=dedent("""\
        1. 内容提取 📑
           - 从文章中提取内容
           - 保留重要引用和统计数据
           - 保持适当的归属
           - 优雅地处理付费墙
        2. 内容处理 🔄
           - 以清晰的markdown格式化文本
           - 保留关键信息
           - 逻辑性地结构化内容
        3. 质量控制 ✅
           - 验证内容相关性
           - 确保准确提取
           - 保持可读性
        4. 以中文生成回复\
        """),
        response_model=ScrapedArticle,
        structured_outputs=True,
    )

    # Content Writer Agent: Crafts engaging blog posts from research
    writer: Agent = Agent(
        # model=OpenAIChat(id="gpt-4o-mini"),
        # model=Gemini(id="gemini-2.0-flash"),
        # model=Ollama(id="qwen3:4b"),
        model=OpenRouter(id="gpt-4o"),
        # model=DeepSeek(id="deepseek-chat"),
        # model=DeepSeek(id="deepseek-reasoner")
        description=dedent("""\
        你是博客大师，一位结合新闻卓越性的精英内容创作者
        与数字营销专业知识。你的优势包括：

        - 制作值得病毒式传播的标题
        - 撰写引人入胜的介绍
        - 为数字消费结构化内容
        - 无缝整合研究
        - 优化SEO同时保持质量
        - 创建可分享的结论\
        """),
        instructions=dedent("""\
        1. 内容策略 📝
           - 制作吸引眼球的标题
           - 撰写引人入胜的介绍
           - 为吸引读者而结构化内容
           - 包含相关子标题
        2. 写作卓越性 ✍️
           - 平衡专业知识与可访问性
           - 使用清晰、引人入胜的语言
           - 包含相关示例
           - 自然地融入统计数据
        3. 来源整合 🔍
           - 正确引用来源
           - 包含专家引述
           - 保持事实准确性
        4. 数字优化 💻
           - 结构便于浏览
           - 包含可分享的要点
           - 优化SEO
           - 添加引人入胜的子标题
        5. 以中文生成回复\
        """),
        expected_output=dedent("""\
        # {值得病毒式传播的标题}

        ## 介绍
        {引人入胜的开场白和背景}

        ## {引人注目的第1部分}
        {关键见解和分析}
        {专家引述和统计数据}

        ## {引人入胜的第2部分}
        {深入探索}
        {现实世界的例子}

        ## {实用的第3部分}
        {可行的见解}
        {专家建议}

        ## 关键要点
        - {可分享的见解1}
        - {实用的要点2}
        - {值得注意的发现3}

        ## 来源
        {适当归属的带链接的来源}\
        """),
        markdown=True,
    )

    def run(
        self,
        topic: str,
        use_search_cache: bool = True,
        use_scrape_cache: bool = True,
        use_cached_report: bool = True,
    ) -> Iterator[RunResponse]:
        logger.info(f"Generating a blog post on: {topic}")

        # Use the cached blog post if use_cache is True
        if use_cached_report:
            cached_blog_post = self.get_cached_blog_post(topic)
            if cached_blog_post:
                yield RunResponse(
                    content=cached_blog_post, event=RunEvent.workflow_completed
                )
                return

        # Search the web for articles on the topic
        search_results: Optional[SearchResults] = self.get_search_results(
            topic, use_search_cache
        )
        # If no search_results are found for the topic, end the workflow
        if search_results is None or len(search_results.articles) == 0:
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content=f"抱歉，找不到关于该主题的任何文章：{topic}",
            )
            return

        # Scrape the search results
        scraped_articles: Dict[str, ScrapedArticle] = self.scrape_articles(
            topic, search_results, use_scrape_cache
        )

        # Prepare the input for the writer
        writer_input = {
            "topic": topic,
            "articles": [v.model_dump() for v in scraped_articles.values()],
        }

        # Run the writer and yield the response
        yield from self.writer.run(json.dumps(writer_input, indent=4), stream=True)

        # Save the blog post in the cache
        self.add_blog_post_to_cache(topic, self.writer.run_response.content)

    def get_cached_blog_post(self, topic: str) -> Optional[str]:
        logger.info("Checking if cached blog post exists")

        return self.session_state.get("blog_posts", {}).get(topic)

    def add_blog_post_to_cache(self, topic: str, blog_post: str):
        logger.info(f"Saving blog post for topic: {topic}")
        self.session_state.setdefault("blog_posts", {})
        self.session_state["blog_posts"][topic] = blog_post

    def get_cached_search_results(self, topic: str) -> Optional[SearchResults]:
        logger.info("Checking if cached search results exist")
        search_results = self.session_state.get("search_results", {}).get(topic)
        return (
            SearchResults.model_validate(search_results)
            if search_results and isinstance(search_results, dict)
            else search_results
        )

    def add_search_results_to_cache(self, topic: str, search_results: SearchResults):
        logger.info(f"Saving search results for topic: {topic}")
        self.session_state.setdefault("search_results", {})
        self.session_state["search_results"][topic] = search_results

    def get_cached_scraped_articles(
        self, topic: str
    ) -> Optional[Dict[str, ScrapedArticle]]:
        logger.info("Checking if cached scraped articles exist")
        scraped_articles = self.session_state.get("scraped_articles", {}).get(topic)
        return (
            ScrapedArticle.model_validate(scraped_articles)
            if scraped_articles and isinstance(scraped_articles, dict)
            else scraped_articles
        )

    def add_scraped_articles_to_cache(
        self, topic: str, scraped_articles: Dict[str, ScrapedArticle]
    ):
        logger.info(f"Saving scraped articles for topic: {topic}")
        self.session_state.setdefault("scraped_articles", {})
        self.session_state["scraped_articles"][topic] = scraped_articles

    def get_search_results(
        self, topic: str, use_search_cache: bool, num_attempts: int = 3
    ) -> Optional[SearchResults]:
        # Get cached search_results from the session state if use_search_cache is True
        if use_search_cache:
            try:
                search_results_from_cache = self.get_cached_search_results(topic)
                if search_results_from_cache is not None:
                    search_results = SearchResults.model_validate(
                        search_results_from_cache
                    )
                    logger.info(
                        f"Found {len(search_results.articles)} articles in cache."
                    )
                    return search_results
            except Exception as e:
                logger.warning(f"Could not read search results from cache: {e}")

        # If there are no cached search_results, use the searcher to find the latest articles
        for attempt in range(num_attempts):
            try:
                searcher_response: RunResponse = self.searcher.run(topic)
                if (
                    searcher_response is not None
                    and searcher_response.content is not None
                    and isinstance(searcher_response.content, SearchResults)
                ):
                    article_count = len(searcher_response.content.articles)
                    logger.info(
                        f"Found {article_count} articles on attempt {attempt + 1}"
                    )
                    # Cache the search results
                    self.add_search_results_to_cache(topic, searcher_response.content)
                    return searcher_response.content
                else:
                    logger.warning(
                        f"Attempt {attempt + 1}/{num_attempts} failed: Invalid response type"
                    )
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{num_attempts} failed: {str(e)}")

        logger.error(f"Failed to get search results after {num_attempts} attempts")
        return None

    def scrape_articles(
        self, topic: str, search_results: SearchResults, use_scrape_cache: bool
    ) -> Dict[str, ScrapedArticle]:
        scraped_articles: Dict[str, ScrapedArticle] = {}

        # Get cached scraped_articles from the session state if use_scrape_cache is True
        if use_scrape_cache:
            try:
                scraped_articles_from_cache = self.get_cached_scraped_articles(topic)
                if scraped_articles_from_cache is not None:
                    scraped_articles = scraped_articles_from_cache
                    logger.info(
                        f"Found {len(scraped_articles)} scraped articles in cache."
                    )
                    return scraped_articles
            except Exception as e:
                logger.warning(f"Could not read scraped articles from cache: {e}")

        # Scrape the articles that are not in the cache
        for article in search_results.articles:
            if article.url in scraped_articles:
                logger.info(f"Found scraped article in cache: {article.url}")
                continue

            article_scraper_response: RunResponse = self.article_scraper.run(
                article.url
            )
            if (
                article_scraper_response is not None
                and article_scraper_response.content is not None
                and isinstance(article_scraper_response.content, ScrapedArticle)
            ):
                scraped_articles[article_scraper_response.content.url] = (
                    article_scraper_response.content
                )
                logger.info(f"Scraped article: {article_scraper_response.content.url}")

        # Save the scraped articles in the session state
        self.add_scraped_articles_to_cache(topic, scraped_articles)
        return scraped_articles


# Run the workflow if the script is executed directly
if __name__ == "__main__":
    import random

    from rich.prompt import Prompt

    # 有趣的示例提示，展示生成器的多功能性
    example_prompts = [
        "为什么猫咪秘密统治着互联网",
        "为什么披萨在凌晨2点尝起来更美味的科学原理",
        "时间旅行者的现代社交媒体指南",
        "橡皮鸭如何彻底改变软件开发",
        "办公室植物的秘密社会：生存指南",
        "为什么狗认为我们不善于嗅闻",
        "咖啡店WiFi密码的地下经济",
        "爸爸笑话的历史分析",
    ]

    # 从用户获取主题
    topic = Prompt.ask(
        "[bold]输入博客文章主题[/bold] (或按Enter获取随机示例)\n✨",
        default=random.choice(example_prompts),
    )

    # 将主题转换为URL安全字符串以用于session_id
    url_safe_topic = topic.lower().replace(" ", "-")

    # 初始化博客文章生成器工作流
    # - 基于主题创建唯一的会话ID
    # - 设置SQLite存储以缓存结果
    generate_blog_post = BlogPostGenerator(
        session_id=f"generate-blog-post-on-{url_safe_topic}",
        storage=SqliteStorage(
            table_name="generate_blog_post_workflows",
            db_file="tmp/agno_workflows.db",
        ),
        debug_mode=True,
    )

    # 执行启用缓存的工作流
    # 返回包含生成内容的RunResponse对象的迭代器
    blog_post: Iterator[RunResponse] = generate_blog_post.run(
        topic=topic,
        use_search_cache=True,
        use_scrape_cache=True,
        use_cached_report=True,
    )

    # 打印响应
    pprint_run_response(blog_post, markdown=True)