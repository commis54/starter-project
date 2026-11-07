from pathlib import Path
from starter_project.main import main

def test_main_function(tmp_path, monkeypatch):
    input_path = tmp_path / "sales.csv"
    output_path = tmp_path / "reports" / "summary.md"

    # Create a valid CSV file
    input_path.write_text("product,category,quantity,unit_price\n"
                          "Widget,Tech,5,10.50\n", encoding="utf-8")

    # Patch sys.argv to simulate command-line arguments
    monkeypatch.setattr("sys.argv", ["main.py", "--input", str(input_path), "--output", str(output_path)])

    exit_code = main()
    assert exit_code == 0
    assert output_path.exists()
