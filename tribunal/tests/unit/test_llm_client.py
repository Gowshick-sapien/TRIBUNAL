"""Unit tests for LLMClient."""

import pytest
from tribunal.planner.exceptions import LLMClientError
from tribunal.planner.llm_client import LLMClient


def test_llm_client_custom_caller():
    def mock_caller(prompt: str) -> str:
        return '{"intent": "pattern_detection", "pattern": "structuring"}'

    client = LLMClient(custom_caller=mock_caller)
    res = client.parse_query("Find structuring")
    assert "pattern_detection" in res
    assert "structuring" in res


def test_llm_client_empty_query():
    client = LLMClient()
    with pytest.raises(LLMClientError, match="cannot be empty"):
        client.parse_query("")


def test_llm_client_unreachable_ollama():
    client = LLMClient(endpoint="http://localhost:59999/nonexistent", timeout=0.1)
    with pytest.raises(LLMClientError, match="Failed to connect to Ollama"):
        client.parse_query("Find structuring")
