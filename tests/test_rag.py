import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock
from services.rag.rag import RAG, SlidingWindowChunking, crawl4ai_crawl_many, CrawlResult, DB_Site
from services.rag.search import Searcher
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, CrawlResult, MarkdownGenerationResult
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from schemas import *

pytest_plugins = 'pytest_asyncio'
from pydantic import BaseModel

@pytest.fixture
def mock_rag():
    with patch('services.rag.rag.Searcher') as MockSearcher, \
         patch('services.rag.rag.VecDb') as MockVecDb, \
         patch('services.rag.rag.RAGOpenai') as MockRAGOpenai:
        MockSearcher.return_value = AsyncMock()
        MockVecDb.return_value = AsyncMock()
        MockRAGOpenai.return_value = AsyncMock()
        yield RAG(cheap_models=[], brave_api_key="test_key")

@pytest.mark.asyncio
async def test_rag_initialization(mock_rag):
    assert mock_rag.sr is not None
    assert mock_rag.db is not None
    assert mock_rag.llm is not None
    assert mock_rag.top_results == 4

@pytest.mark.asyncio
async def test_search_and_crawl(mock_rag):
    mock_rag.sr.search.return_value = [SearchItem(title="Example", url="http://example.com", is_source_local=False, is_source_both=False)]
    with patch('services.rag.rag.crawl4ai_crawl_many', new_callable=AsyncMock) as mock_crawl:
        mock_crawl.return_value = [CrawlResult(url="http://example.com", html="<html></html>", success=True)]
        results = await mock_rag.search_and_crawl("test query")
        assert len(results) == 1
        assert results[0].url == "http://example.com"

@pytest.mark.asyncio
async def test_CrawlResult_to_DB_Site(mock_rag):
    mock_site = CrawlResult(url="http://example.com", html="<html></html>", success=True, cleaned_html="<html></html>", _markdown=MarkdownGenerationResult(raw_markdown="markdown", markdown_with_citations="markdown with citations", references_markdown="references"))
    mock_rag.llm.summarize.return_value = "summarized markdown"
    db_site = await mock_rag.CrawlResult_to_DB_Site(mock_site)

@pytest.mark.asyncio
async def test_add_chunks(mock_rag):
    mock_site = CrawlResult(url="http://example.com", html="<html></html>", success=True, cleaned_html="<html></html>", _markdown=MarkdownGenerationResult(raw_markdown="markdown", markdown_with_citations="markdown with citations", references_markdown="references"))
    mock_rag.CrawlResult_to_DB_Site = AsyncMock(return_value=DB_Site(url="http://example.com", content="content", title="title", chunks=["chunk"]))
    results = await mock_rag.add_chunks([mock_site])
    assert len(results) == 1
    assert results[0].url == "http://example.com"
    assert len(results[0].chunks) > 0

@pytest.mark.asyncio
async def test_search_store(mock_rag):
    mock_rag.search_and_crawl = AsyncMock(return_value=[CrawlResult(url="http://example.com", html="<html></html>", success=True)])
    mock_rag.add_chunks = AsyncMock(return_value=[DB_Site(url="http://example.com", content="content", title="title", chunks=["chunk"])])
    mock_rag.db.insert_sites_n_chunks = AsyncMock(return_value=True)
    result = await mock_rag.search_store("test query")
    assert result is True

@pytest.mark.asyncio
async def test_retrieve_no_search(mock_rag):
    mock_rag.db.retrieve_no_search = AsyncMock(return_value=["result1", "result2"])
    results = await mock_rag.retrieve_no_search("test query")
    assert len(results) == 2
    assert results[0] == "result1"

@pytest.mark.asyncio
async def test_retrieve_with_search(mock_rag):
    mock_rag.search_store = AsyncMock()
    mock_rag.db.retrieve_no_search = AsyncMock(return_value=["result1", "result2"])
    results = await mock_rag.retrieve_with_search("test query")
    assert len(results) == 2
    assert results[0] == "result1"