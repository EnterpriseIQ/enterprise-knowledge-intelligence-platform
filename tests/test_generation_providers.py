import os
import pytest
from unittest.mock import patch, MagicMock

from src.retrieval.hybrid_retriever import RetrievedChunk
from src.generation.providers.openai_provider import OpenAIProvider
from src.generation.providers.gemini_provider import GeminiProvider
from src.generation.providers.ollama_provider import OllamaProvider

def dummy_chunks():
    return [
        RetrievedChunk(
            chunk_id="d::0",
            text="Context.",
            metadata={"title": "Doc", "department": "HR"},
            fused_score=0.9,
        )
    ]

# ---------------- OpenAI Provider ----------------

def test_openai_initialization_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider()
    assert provider.is_available() is False
    assert provider.generate("query", dummy_chunks(), "system") is None

def test_openai_generate_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)

    # We patch the import so that it doesn't fail
    with patch.dict("sys.modules", {"openai": MagicMock()}):
        provider = OpenAIProvider()

        # Override the _client after initialization
        mock_client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "OpenAI response"
        mock_client.chat.completions.create.return_value.choices = [mock_choice]
        provider._client = mock_client

        assert provider.is_available() is True
        response = provider.generate("query", dummy_chunks(), "system")
        assert response == "OpenAI response"

def test_openai_generate_exception(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)

    with patch.dict("sys.modules", {"openai": MagicMock()}):
        provider = OpenAIProvider()

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        provider._client = mock_client

        assert provider.generate("query", dummy_chunks(), "system") is None

# ---------------- Gemini Provider ----------------

def test_gemini_initialization_no_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    provider = GeminiProvider()
    assert provider.is_available() is False
    assert provider.generate("query", dummy_chunks(), "system") is None

def test_gemini_generate_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy-key")

    with patch.dict("sys.modules", {"google.genai": MagicMock(), "google.genai.types": MagicMock()}):
        provider = GeminiProvider()

        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "Gemini response"
        mock_client.models.generate_content.return_value = mock_resp

        provider._client = mock_client
        provider._types = MagicMock()

        assert provider.is_available() is True
        response = provider.generate("query", dummy_chunks(), "system")
        assert response == "Gemini response"

def test_gemini_generate_exception(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy-key")

    with patch.dict("sys.modules", {"google.genai": MagicMock(), "google.genai.types": MagicMock()}):
        provider = GeminiProvider()

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API error")

        provider._client = mock_client
        provider._types = MagicMock()

        assert provider.generate("query", dummy_chunks(), "system") is None

# ---------------- Ollama Provider ----------------

@patch("requests.post")
def test_ollama_generate_success(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"message": {"content": "Ollama response"}}
    mock_post.return_value = mock_resp

    provider = OllamaProvider()
    assert provider.is_available() is True

    response = provider.generate("query", dummy_chunks(), "system")
    assert response == "Ollama response"

@patch("requests.post")
def test_ollama_generate_exception(mock_post):
    mock_post.side_effect = Exception("Connection error")

    provider = OllamaProvider()
    assert provider.generate("query", dummy_chunks(), "system") is None
