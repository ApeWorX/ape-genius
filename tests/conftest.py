import pytest
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def setup_logging():
    """Configure logging for tests"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

@pytest.fixture
def tokens():
    """Bot tokens and IDs from environment variables"""
    return {
        "telegram": os.getenv('TELEGRAM_TOKEN'),
        "claude": os.getenv('CLAUDE_KEY'),
        "admin_id": 1978731049,  # Chris | ApeWorX
        "group_id": -4718382612,  # ApeClaudeCouncil
        "bot_id": 7879249317     # ApeCluade bot
    }

@pytest.fixture(scope="session")
def cached_knowledge_base(request):
    """Cache the knowledge base content using file hash as key"""
    kb_path = Path("knowledge-base/all.txt")
    
    # Generate hash of file content for cache key
    file_hash = hashlib.md5(kb_path.read_bytes()).hexdigest()
    cache_key = f"knowledge_base_content_{file_hash}"
    
    # Try to get content from cache
    cached_content = request.config.cache.get(cache_key, None)
    
    if cached_content is None:
        # Cache miss - read file and store in cache
        content = kb_path.read_text(encoding='utf-8')
        request.config.cache.set(cache_key, content)
        return content
    
    return cached_content

@pytest.fixture(scope="session")
def knowledge_base_stats(cached_knowledge_base):
    """Provide basic stats about the knowledge base"""
    content = cached_knowledge_base
    return {
        "total_length": len(content),
        "line_count": len(content.splitlines()),
        "has_python_code": "```python" in content,
        "has_vyper_code": "```vyper" in content
    }