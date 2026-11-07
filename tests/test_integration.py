from starter_project.io import load_sales_csv, write_report
from starter_project.analysis import calculate_summary
from decimal import Decimal

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
    assert "## Quantity Statistics" in report_content
    assert "## Price Statistics" in report_content
    assert f"- Input file: {input_path}" in report_content
    assert f"- Records analyzed: {summary['record_count']}" in report_content

    assert f"| {summary['total_quantity']} |" in report_content
    assert f"| {summary['average_quantity']} |" in report_content
    assert f"| {summary['minimum_quantity']} |" in report_content
    assert f"| {summary['maximum_quantity']} |" in report_content
    assert f"| {summary['average_unit_price']} |" in report_content
    assert f"| {summary['total_revenue']} |" in report_content

    assert summary['record_count'] == 3
    assert summary['total_quantity'] == 8
    assert summary['average_quantity'] == round((5 + 2 + 1) / 3, 2)
    assert summary['minimum_quantity'] == 1
    assert summary['maximum_quantity'] == 5
    assert summary['average_unit_price'] == round(Decimal(str((10.00/3 + 20.00/3 + 5.50/3))), 2)
    assert summary['total_revenue'] == Decimal(str((5 * 10.00) + (2 * 20.00) + (1 * 5.50)))
