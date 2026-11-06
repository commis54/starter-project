import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED_COLUMNS = {"product", "category", "quantity", "unit_price"}

def load_sales_csv(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    with file_path.open(mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
            raise ValueError(f"Missing required columns in CSV file: {file_path}")
        if len(reader.fieldnames) > len(REQUIRED_COLUMNS):
            raise ValueError(f"Extra columns found in CSV file: {file_path}")
        data = False
        for row in reader:
            data = True
            try:
                row["quantity"] = int(row["quantity"])
                row["unit_price"] = Decimal(row["unit_price"])
            except (ValueError, InvalidOperation, TypeError) as e:
                raise ValueError(f"Invalid data type in CSV file: {file_path}. Error: {e} in row: {row}")
            if row["quantity"] < 0 or row["unit_price"] < 0:
                raise ValueError(f"Negative values found in CSV file: {file_path}")
            yield row
        if data is False:
            raise ValueError(f"No data found in CSV file: {file_path}")
            
def write_report(summary, input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    if not output_path.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.touch()
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(f"# Sales Summary Report\n\n")
        file.write("## Dataset Information\n\n")
        file.write(f"- Input file: {input_path}\n")
        file.write(f"- Records analyzed: {len(summary)}\n\n")
        file.write("## Quantity Statistics\n\n")
        file.write("| Metric | Value |\n")
        file.write("|---|---:|\n")
        for i in range(len(summary)):
            if i >= 1 and i <= 4:
                line = f"| {summary[i][0]} | {summary[i][1]} |"
                file.write(f"{line}\n")
        file.write("\n")
        file.write("## Price Statistics\n\n")
        file.write("| Metric | Value |\n")
        file.write("|---|---:|\n")
        for i in range(len(summary)):
                if i >= 5 and i <= 6:
                    line = f"| {summary[i][0]} | {summary[i][1]} |"
                    file.write(f"{line}\n")

