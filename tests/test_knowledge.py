import pytest

def test_knowledge_base_content(cached_knowledge_base, setup_logging):
    """Test knowledge base content structure using cached content"""
    content = cached_knowledge_base
    
    # Check for required sections
    required_keywords = [
        "apeworx",
        "vyper",
        "silverback",
        "contract",
        "deploy",
        "test"
    ]
    
    for keyword in required_keywords:
        assert keyword.lower() in content.lower(), f"Missing content about: {keyword}"
    
    setup_logging.info("Knowledge base content validation successful")

def test_knowledge_base_stats(knowledge_base_stats, setup_logging):
    """Test knowledge base statistics"""
    assert knowledge_base_stats["total_length"] > 0, "Knowledge base is empty"
    assert knowledge_base_stats["line_count"] > 0, "Knowledge base has no lines"
    
    setup_logging.info(f"""Knowledge base stats:
    - Total length: {knowledge_base_stats['total_length']} characters
    - Line count: {knowledge_base_stats['line_count']} lines
    - Has Python code: {knowledge_base_stats['has_python_code']}
    - Has Vyper code: {knowledge_base_stats['has_vyper_code']}
    """)

def test_code_examples(cached_knowledge_base):
    """Test if knowledge base contains code examples"""
    content = cached_knowledge_base
    
    code_indicators = ["```python", "```vyper", "@external", "def "]
    found_code = any(indicator in content for indicator in code_indicators)
    assert found_code, "No code examples found in knowledge base"