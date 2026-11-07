import pytest
from decimal import Decimal
from pathlib import Path
from starter_project.io import load_sales_csv, write_report

# Test input

def test_load_sales_csv_valid_path(tmp_path):
    csv_file = tmp_path / "valid_sales.csv"
    csv_file.write_text("product,category,quantity,unit_price\n" 
                         "Widget,Tech,5,10.50\n", encoding="utf-8")

    data = list(load_sales_csv(csv_file))

    assert len(data) == 1 
    assert data[0]["product"] == "Widget"
    assert data[0]["category"] == "Tech"
    assert data[0]["quantity"] == 5
    assert data[0]["unit_price"] == Decimal("10.50")

def test_load_sales_csv_missing_columns(tmp_path):
    csv_file = tmp_path / "missing_cloumns.csv"
    csv_file.write_text("product,category,quantity\n"
                        "Widget,Tech,5\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required columns"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_missing_data(tmp_path):
    csv_file = tmp_path / "missing_data.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,5\n", encoding="utf-8")
    
    with pytest.raises(ValueError):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_empty_data(tmp_path):
    csv_file = tmp_path / "empty_data.csv"
    csv_file.write_text("product,category,quantity,unit_price\n", encoding="utf-8")

    with pytest.raises(ValueError, match="No data found"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_invalid_data_type(tmp_path):
    csv_file = tmp_path / "invalid_data_type.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,five,10.50\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid data type"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_extra_columns(tmp_path):
    csv_file = tmp_path / "extra_columns.csv"
    csv_file.write_text("product,category,quantity,unit_price,extra_column\n"
                        "Widget,Tech,5,10.50,value\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Extra columns found"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_missing_file():
    missing_path = Path("data/non_existent_file.csv")

    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        list(load_sales_csv(missing_path))

def test_load_sales_csv_directory_instead_of_file(tmp_path):
    dir_path = tmp_path / "some_folder"
    dir_path.mkdir()

    with pytest.raises(ValueError, match="Path is not a file"):
        list(load_sales_csv(dir_path))

def test_load_sales_csv_negative_values_quantity(tmp_path):
    csv_file = tmp_path / "negative_values.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,-5,10.50\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Negative or non-finite values found in CSV file"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_negative_values_unit_price(tmp_path):
    csv_file = tmp_path / "negative_values.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,5,-10.50\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Negative or non-finite values found in CSV file"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_infinite_values(tmp_path):
    csv_file = tmp_path / "infinite_values.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,5,Infinity\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Negative or non-finite values found in CSV file"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_non_finite_values(tmp_path):
    csv_file = tmp_path / "non_finite_values.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,Tech,5,NaN\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Negative or non-finite values found in CSV file"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_invalid_data_type_with_missing_value_product(tmp_path):
    csv_file = tmp_path / "invalid_data_type_missing_value.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        ",Tech,5,10.50\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required data in CSV file:"):
        list(load_sales_csv(csv_file))

def test_load_sales_csv_invalid_data_type_with_missing_value_category(tmp_path):
    csv_file = tmp_path / "invalid_data_type_missing_value.csv"
    csv_file.write_text("product,category,quantity,unit_price\n"
                        "Widget,,5,10.50\n", encoding="utf-8")

    with pytest.raises(ValueError, match=f"Missing required data in CSV file:"):
        list(load_sales_csv(csv_file))

def test_input_path_permission(monkeypatch, tmp_path):
    dummy_file = tmp_path / "input.csv"
    dummy_file.touch()

    def mock_open(*args, **kwargs):
        raise PermissionError("Cannot read the data file due to permission issues")

    monkeypatch.setattr(Path, "open", mock_open)

    generator = load_sales_csv(dummy_file)

    with pytest.raises(PermissionError, match="Access Denied"):
        next(generator)

# Test output

def test_write_report_creates_nested_output_path(tmp_path):
    input_path = tmp_path / "sales.csv"
    output_path = tmp_path / "reports" / "2026" / "summary.md"

    dummy_summary = {
            "record_count": 10,
            "total_quantity": 105,
            "average_quantity": 10.5,
            "minimum_quantity": 1,
            "maximum_quantity": 20,
            "average_unit_price": Decimal("27.5"),
            "total_revenue": Decimal("275.0"),
            }

    write_report(dummy_summary, input_path, output_path)

    assert output_path.exists()
    assert output_path.is_file()

    content = output_path.read_text(encoding="utf-8")
    assert "# Sales Summary Report" in content
    assert f"- Input file: {input_path}" in content
    assert "| Minimum quantity | 1 |" in content
    assert "| Average unit price | 27.5 |" in content

def test_output_path_permission(monkeypatch):
    def mock_open(*args, **kwargs):
        raise PermissionError("Cannot write to file due to permission issues")

    monkeypatch.setattr("builtins.open", mock_open)

    dummy_summary = {
        'record_count': 0, 'total_quantity': 0, 'average_quantity': 0,
        'minimum_quantity': 0, 'maximum_quantity': 0, 'average_unit_price': 0,
        'total_revenue': 0
    }

    result = write_report(dummy_summary, "input.csv", "output.md")
    assert result == "Access Denied"
