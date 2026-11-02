import argparse
import sys
from pathlib import Path

from starter_project.io import load_sales_csv, write_report
from starter_project.analysis import calculate_summary

def main():
    parser = argparse.ArgumentParser(description="A script to process sales data.")

    parser.add_argument("--input", type=Path, help="Path to the input CSV file containing sales data.", required=True)
    parser.add_argument("--output", type=Path, help="Path to the output report file.", required=False, default=Path("reports/summary.md"))

    args = parser.parse_args()
    try:
        write_report(calculate_summary(list(load_sales_csv(args.input))), args.input, args.output)
        print(f"Report generated successfully at: {args.output}")
        return 0 
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1  
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

