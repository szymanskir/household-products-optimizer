import pytest

from typing import List
from src.household_product import HouseholdProduct
from src.optimization import evaluate_order_price


@pytest.mark.parametrize(
    "order,expected_price", [
        ([HouseholdProduct(name="test", price=100)], 100),
        ([HouseholdProduct(name="cheap", price=100),
            HouseholdProduct(name="expensive", price=1000)], 1088)
    ]
)
def test_order_price_evaluation(order: List[HouseholdProduct], expected_price):
    result_price = evaluate_order_price(order)
    assert result_price == expected_price
