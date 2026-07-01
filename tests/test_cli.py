import json
import pytest
from unittest.mock import patch, MagicMock

from src.cli import main


@patch("src.cli.argparse.ArgumentParser.parse_args")
@patch("src.cli.RAGPipeline")
def test_cli_build_only(mock_pipeline_class, mock_parse_args, capsys):
    # Mock args
    mock_args = MagicMock()
    mock_args.build = True
    mock_args.query = None
    mock_args.role = None
    mock_args.user = None
    mock_args.top_k = None
    mock_args.json = False
    mock_parse_args.return_value = mock_args

    # Mock pipeline instance
    mock_pipeline = mock_pipeline_class.return_value
    mock_pipeline.build_index.return_value = {"chunks": 10}

    main()

    captured = capsys.readouterr()
    assert "Index built:" in captured.out
    assert "chunks" in captured.out
    mock_pipeline.query.assert_not_called()


@patch("src.cli.argparse.ArgumentParser.parse_args")
@patch("src.cli.RAGPipeline")
def test_cli_query_text_output(mock_pipeline_class, mock_parse_args, capsys):
    mock_args = MagicMock()
    mock_args.build = False
    mock_args.query = "What is remote policy?"
    mock_args.role = "HR"
    mock_args.user = None
    mock_args.top_k = 5
    mock_args.json = False
    mock_parse_args.return_value = mock_args

    mock_pipeline = mock_pipeline_class.return_value
    mock_pipeline.build_index.return_value = {"chunks": 10}

    mock_result = MagicMock()
    mock_result.query = "What is remote policy?"
    mock_result.role = "HR"
    mock_result.confidence = {"label": "high", "score": 0.9}
    mock_result.answer = "Remote work is allowed."
    mock_result.citations = [{"reference": "[1]", "snippet": "remote work"}]
    mock_result.route = {"rationale": "keyword match"}
    mock_result.authorised_count = 5
    mock_result.denied_count = 0
    mock_pipeline.query.return_value = mock_result

    main()

    captured = capsys.readouterr()
    assert "Q: What is remote policy?" in captured.out
    assert "Confidence: high (0.9)" in captured.out
    assert "Remote work is allowed." in captured.out
    assert "[1]" in captured.out


@patch("src.cli.argparse.ArgumentParser.parse_args")
@patch("src.cli.RAGPipeline")
def test_cli_query_json_output(mock_pipeline_class, mock_parse_args, capsys):
    mock_args = MagicMock()
    mock_args.build = False
    mock_args.query = "What is remote policy?"
    mock_args.role = "HR"
    mock_args.user = "hr_alice"
    mock_args.top_k = None
    mock_args.json = True
    mock_parse_args.return_value = mock_args

    mock_pipeline = mock_pipeline_class.return_value
    mock_pipeline.build_index.return_value = {"chunks": 10}

    mock_result = MagicMock()
    mock_result.to_dict.return_value = {"answer": "Remote work is allowed."}
    mock_pipeline.query.return_value = mock_result

    main()

    captured = capsys.readouterr()
    output_json = json.loads(captured.out)
    assert output_json["answer"] == "Remote work is allowed."
