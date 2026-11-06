import pytest
from decimal import Decimal
from starter_project.analysis import calculate_summary

def test_analysis():
    records = [
        {"product": "Widget", "category": "Tech", "quantity": 5, "unit_price": Decimal("10.50")},
        {"product": "Gadget", "category": "Tech", "quantity": 3, "unit_price": Decimal("15.00")},
    ]
    summary = calculate_summary(records)
    assert summary[0][1] == 2  
    assert summary[1][1] == 8
    assert summary[2][1] == 4
    assert summary[3][1] == 3
    assert summary[4][1] == 5
    assert summary[5][1] == pytest.approx(Decimal("12.75"))
    assert summary[6][1] == pytest.approx(Decimal("97.50"))

def test_analysis_empty_records():
    with pytest.raises(ValueError, match="The data list is empty"):
        calculate_summary([])