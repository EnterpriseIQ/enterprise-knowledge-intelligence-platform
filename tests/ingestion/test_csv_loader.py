from pathlib import Path

from src.ingestion.csv_loader import load_csv


def test_load_csv_happy_path(tmp_path: Path):
    """Test loading a standard CSV file."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name,value\n1,foo,10\n2,bar,20\n", encoding="utf-8")

    result = load_csv(csv_file)

    assert "CSV dataset: test.csv" in result
    assert "Columns: id, name, value" in result
    assert "Row count: 2" in result
    assert "- id=1; name=foo; value=10" in result
    assert "- id=2; name=bar; value=20" in result

def test_load_csv_empty(tmp_path: Path):
    """Test loading a CSV file with only headers."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("id,name,value\n", encoding="utf-8")

    result = load_csv(csv_file)

    assert "CSV dataset: empty.csv" in result
    assert "Columns: id, name, value" in result
    assert "Row count: 0" in result
    assert "Records:" in result

def test_load_csv_max_rows(tmp_path: Path):
    """Test loading a CSV file and truncating to max_rows."""
    csv_file = tmp_path / "large.csv"
    content = "id,value\n" + "\n".join(f"{i},{i*10}" for i in range(1, 10))
    csv_file.write_text(content, encoding="utf-8")

    result = load_csv(csv_file, max_rows=3)

    assert "Row count: 9" in result # total count should still be reported
    assert "- id=1; value=10" in result
    assert "- id=3; value=30" in result
    assert "- id=4; value=40" not in result # shouldn't include row 4
