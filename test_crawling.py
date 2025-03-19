import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock
from rag.rag import SlidingWindowChunking, crawl4ai_crawl_many, CrawlResult, DB_Site, RAG
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai import CrawlerRunConfig

pytest_plugins = 'pytest_asyncio'
