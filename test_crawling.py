import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock
from rag import SlidingWindowChunking, crawl4ai_crawl_many, CrawlResult, DB_Site, RAG
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai import CrawlerRunConfig

pytest_plugins = 'pytest_asyncio'

@pytest.mark.asyncio
async def test_Crawling():
    urls = [
        "https://en.wikipedia.org/wiki/Fernando_de_Noronha",
        "https://en.wikipedia.org/wiki/Rio_de_Janeiro",
    ]
    results = await crawl4ai_crawl_many(urls)
    assert len(results) == 2
    assert all(isinstance(result, CrawlResult) for result in results)
    assert all(result.markdown for result in results)
    assert all(result.url for result in results)
    assert all(result.success for result in results)

@pytest.mark.asyncio
async def test_chunking_crawling_integration():
    chunker = SlidingWindowChunking()

    urls = [
        "https://en.wikipedia.org/wiki/Fernando_de_Noronha",
        "https://en.wikipedia.org/wiki/Rio_de_Janeiro",
    ]
    results = await crawl4ai_crawl_many(urls)
    assert len(results) == 2
    assert all(isinstance(result, CrawlResult) for result in results)
    assert all(hasattr(result, 'markdown') for result in results)
    assert all(result.url for result in results)
    assert all(result.success for result in results)
    sites =  [await chunker._add_chunks(site) for site in results]
    assert len(sites) == 2
    assert all(isinstance(site, DB_Site) for site in sites)
    assert all(site.chunks for site in sites)
    assert all(site.url for site in sites)
    assert all(site.title for site in sites)
    assert all(site.content for site in sites)
    #assert all(site.timestamp for site in sites) #timestamp was removed from DB_Site
    
    # for i, site in enumerate(sites):
    #     assert (site.content) != (str(results[i].markdown))