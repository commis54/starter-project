## Project title

Reproducible Python Starter Repository.

## Description

The aim of the application is to train using programming features I have learned, such as Git, GitHub, Linux, Bash, Python.
The application takes data, analyzes it and gives a ready-to-use summary about data.

## Features

Reading, validation, analysis and reporting.

## Requirments

Requirments are in the file pyproject.toml

## Installation 

Create a virtual environment in python (.venv). Then install all the requirments from file to separate dependencies.

## Input format

CSV file should consist of columns (product,category,quantity,unit_price) and data type (str,str,int,float) accordingly.

## Usage

To run this application, firstly you should prepare data you want to analyze. After that in the terminal open the folder and write command:
python -m starter_project.main --input (input path - obligatory) --output (output path - unobligatory)
If you have problems, you also can gain help using: python -m starter_project.main --help

## Testing

To test application write this command: python3 -m pytest -v

## Output 

The output will be generated Markdown file that contains from Dataset Information, Quantity Statistics and Price Statistics.

## Error handling

The application detects various errors (ValueError, InvalidOperation, TypeError ), and writes what is the problem.
It may be: 
- Missing required columns 
- Extra columns found in CSV file 
- CSV file not found 
- Path is not a file 
- Invalid data type in CSV file
- Negative values found in CSV file
- No data found in CSV file
- The data list is empty for summary