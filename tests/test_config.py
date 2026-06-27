import importlib
import sys
from unittest.mock import MagicMock, patch

import src.config


def test_dotenv_success():
    """Test that load_dotenv is called correctly when dotenv is installed."""
    mock_dotenv = MagicMock()
    with patch.dict(sys.modules, {"dotenv": mock_dotenv}):
        # Reloading the module simulates a fresh import, which triggers the try/except block
        importlib.reload(src.config)
        mock_dotenv.load_dotenv.assert_called_once_with(src.config.PROJECT_ROOT / ".env")


def test_dotenv_failure():
    """Test that no exception is raised when dotenv is missing."""
    with patch.dict(sys.modules, {"dotenv": None}):
        # Should not raise an exception, meaning it safely skips load_dotenv
        importlib.reload(src.config)
