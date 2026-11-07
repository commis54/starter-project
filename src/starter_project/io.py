import csv
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED_COLUMNS = {"product", "category", "quantity", "unit_price"}


def load_sales_csv(file_path: str | Path) -> Iterator[dict[str, object]]:
    """Load sales data from a CSV file and validate the data."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    try:
        with file_path.open(mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
                raise ValueError(f"Missing required columns in CSV file: {file_path}")
            if len(reader.fieldnames) > len(REQUIRED_COLUMNS):
                raise ValueError(f"Extra columns found in CSV file: {file_path}")
            data = False
            for row in reader:
                data = True
                for i in REQUIRED_COLUMNS:
                    if row[i] is None or row[i].strip() == "":
                        raise ValueError(f"Missing required data in CSV file: {file_path}. Row: {row}")
                if len(row) != len(REQUIRED_COLUMNS):
                    raise ValueError(f"Missing or unexpected data in CSV file: {file_path}. Row: {row}")
                try:
                    row["product"] = str(row["product"].strip())
                    row["category"] = str(row["category"].strip())
                    row["quantity"] = int(row["quantity"].strip())
                    row["unit_price"] = Decimal(row["unit_price"].strip())
                except (ValueError, InvalidOperation, TypeError, AttributeError) as e:
                    raise ValueError(f"Invalid data type in CSV file or the data missing: {file_path}. Error: {e} in row: {row}")
                if not row["unit_price"].is_finite() or row["quantity"] < 0 or row["unit_price"] < 0:
                    raise ValueError(f"Negative or non-finite values found in CSV file: {file_path}. Row: {row}")
                yield row
            if data is False:
                raise ValueError(f"No data found in CSV file: {file_path}")
    except PermissionError:
        raise PermissionError("Access Denied")

 
def write_report(summary: dict[str, object], input_path: str | Path, output_path: str | Path):
    """Write the summary report to a Markdown file."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    try:
        if not output_path.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(f"# Sales Summary Report\n\n")
            file.write("## Dataset Information\n\n")
            file.write(f"- Input file: {input_path}\n")
            file.write(f"- Records analyzed: {summary['record_count']}\n\n")
            file.write("## Quantity Statistics\n\n")
            file.write("| Metric | Value |\n")
            file.write("|---|---:|\n")
            file.write(f"| Total quantity | {summary['total_quantity']} |\n")
            file.write(f"| Average quantity | {summary['average_quantity']} |\n")
            file.write(f"| Minimum quantity | {summary['minimum_quantity']} |\n")
            file.write(f"| Maximum quantity | {summary['maximum_quantity']} |\n")
            file.write("\n")
            file.write("## Price Statistics\n\n")
            file.write("| Metric | Value |\n")
            file.write("|---|---:|\n")
            file.write(f"| Average unit price | {summary['average_unit_price']} |\n")
            file.write(f"| Total revenue | {summary['total_revenue']} |\n")
    except PermissionError:
        raise PermissionError("Access Denied")
        

