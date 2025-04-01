import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from services.rag.rag import SlidingWindowChunking, crawl4ai_crawl_many, CrawlResult, DB_Site, RAG
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai import CrawlerRunConfig

pytest_plugins = 'pytest_asyncio'
