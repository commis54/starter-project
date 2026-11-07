# Reproducible Python Starter Repository

## Description

A command-line Python application that reads and validates CSV sales data, calculates summary statistics, and generates a Markdown report.

## Features

Reading, validation, analysis and reporting.

## Requirements

Requirements are in the file pyproject.toml

## Installation 

Create a virtual environment in python (.venv). Then install all the requirments from file to separate dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Input format

CSV file should consist of columns (product,category,quantity,unit_price) and data type (str,str,int,Decimal) accordingly.

## Usage

To run this application, firstly you should prepare data you want to analyze. After that in the terminal open the folder and write command:
```bash
python -m starter_project.main --input data/sales.csv --output reports/summary.md
```
If you have problems, you also can gain help using: 
```bash
python -m starter_project.main --help
```
The --input is obligatory in command, the --output is not.
If you have not written --output, it will automatically be saved to reports/summary.md

## Testing

The pytest is installed through the development dependencies.
To test application write this command: 
```bash
python3 -m pytest -v
```

## Output 

The output will be generated Markdown file that contains from Dataset Information, Quantity Statistics and Price Statistics.

## Error handling

The application detects various errors, and writes what is the problem.
It may be: 
- Missing required columns 
- Extra columns found in CSV file 
- CSV file not found 
- Path is not a file 
- Invalid data type in CSV file
- Negative or non-finite values found in CSV file
- No data found in CSV file
- The data list is empty for summary
- Incomplete record