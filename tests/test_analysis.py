import pytest
from decimal import Decimal
from starter_project.analysis import calculate_summary

def test_analysis():
    records = [
        {"product": "Widget", "category": "Tech", "quantity": 5, "unit_price": Decimal("10.50")},
        {"product": "Gadget", "category": "Tech", "quantity": 3, "unit_price": Decimal("15.00")},
    ]
    summary = calculate_summary(records)
    assert summary["record_count"] == 2
    assert summary["total_quantity"] == 8
    assert summary["average_quantity"] == 4
    assert summary["minimum_quantity"] == 3
    assert summary["maximum_quantity"] == 5
    assert summary["average_unit_price"] == pytest.approx(Decimal("12.75"))
    assert summary["total_revenue"] == pytest.approx(Decimal("97.50"))

def test_analysis_empty_records():
    with pytest.raises(ValueError, match="The data list is empty"):
        calculate_summary([])