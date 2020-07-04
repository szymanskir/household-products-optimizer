from typing import List

import pytest

from src.evaluation import evaluate_order_price_example
from src.exceptions import IncorectOrderSizeException
from src.household_product import HouseholdProduct


@pytest.mark.parametrize(
    "order,expected_price",
    [
        # Single product case
        ([HouseholdProduct(name="test", price=100)], 100),
        # Two products case, cheap first
        (
            [
                HouseholdProduct(name="cheap", price=100),
                HouseholdProduct(name="expensive", price=1000),
            ],
            1088,
        ),
        # Two products case, expensive first
        (
            [
                HouseholdProduct(name="expensive", price=1000),
                HouseholdProduct(name="cheap", price=100),
            ],
            1088,
        ),
        # Three products case
        (
            [
                HouseholdProduct(name="cheap", price=10),
                HouseholdProduct(name="mid", price=100),
                HouseholdProduct(name="expensive", price=1000),
            ],
            1106.6,
        ),
        # Four products case
        (
            [
                HouseholdProduct(name="cheap", price=10),
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="mid-expensive", price=1000),
                HouseholdProduct(name="expensive", price=10000),
            ],
            11103.3,
        ),
        # Five products case
        (
            [
                HouseholdProduct(name="cheap", price=10),
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="just-mid", price=1000),
                HouseholdProduct(name="mid-expensive", price=10000),
                HouseholdProduct(name="expensive", price=100000),
            ],
            111101,
        ),
    ],
)
def test_order_price_evaluation(order: List[HouseholdProduct], expected_price):
    result_price = evaluate_order_price_example(order)
    assert result_price == expected_price


def test_order_price_evaluation_throws_exception_for_too_large_orders():
    products = [
            HouseholdProduct(name="cheap", price=10),
            HouseholdProduct(name="mid-cheap", price=100),
            HouseholdProduct(name="just-mid", price=1000),
            HouseholdProduct(name="mid-expensive", price=10000),
            HouseholdProduct(name="expensive", price=100000),
            HouseholdProduct(name="extra-product", price=100000),
    ]

    with pytest.raises(IncorectOrderSizeException):
        evaluate_order_price_example(products)


def test_order_price_evaluation_throws_exception_for_too_small_orders():
    products = [
    ]

    with pytest.raises(IncorectOrderSizeException):
        evaluate_order_price_example(products)
