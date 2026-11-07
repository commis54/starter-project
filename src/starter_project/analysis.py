def calculate_summary(records: list[dict[str, object]]) -> dict[str, object]:
    """Calculate summary statistics from validated sales records."""
    if len(records) == 0:
        raise ValueError("The data list is empty. Cannot calculate summary.")
    
    quantity = [row["quantity"] for row in records]   
    unit_price = [row["unit_price"] for row in records]

    number_of_records = len(records)
    total_quantity = sum(quantity)
    average_quantity = round(total_quantity / len(quantity), 2)
    minimum_quantity = min(quantity)
    maximum_quantity = max(quantity)
    average_unit_price = round(sum(unit_price) / len(unit_price), 2)
    total_revenue = sum(q * p for q, p in zip(quantity, unit_price))
    summary = {
    "record_count": number_of_records,
    "total_quantity": total_quantity,
    "average_quantity": average_quantity,
    "minimum_quantity": minimum_quantity,
    "maximum_quantity": maximum_quantity,
    "average_unit_price": average_unit_price,
    "total_revenue": total_revenue,
    }
    return summary
