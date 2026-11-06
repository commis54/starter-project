from starter_project.io import load_sales_csv, write_report
from starter_project.analysis import calculate_summary

def test_full_sales_pipeline_integration(tmp_path):
    input_path = tmp_path / "valid_sales.csv"
    input_path.write_text(
        "product,category,quantity,unit_price\n"
        "Widget,Tech,5,10.00\n"
        "Gadget,Tech,2,20.00\n"
        "Sprocket,Hardware,1,5.50\n",
        encoding="utf-8"
    )
    output_path = tmp_path / "test_report.md"

    sales_data = list(load_sales_csv(input_path))

    summary = calculate_summary(sales_data)

    write_report(summary, input_path, output_path)

    assert output_path.exists(), "Integration Test Failed: Report file was not created."
    report_content = output_path.read_text(encoding="utf-8")

    assert "# Sales Summary Report" in report_content
    assert "## Dataset Information" in report_content
    assert f"- Input file: {input_path}" in report_content
    assert f"- Records analyzed: {summary['record_count']}" in report_content