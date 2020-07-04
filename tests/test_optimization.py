import pytest

from typing import List
from scipy.special import binom
from src.household_product import HouseholdProduct
from src.optimization import evaluate_order_price, get_product_list_from_order_code, get_all_orders_sets_prices, \
    get_best_orders_set
from src.exceptions import IncorectOrderSizeException


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
    result_price = evaluate_order_price(order)
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
        evaluate_order_price(products)


def test_order_price_evaluation_throws_exception_for_too_small_orders():
    products = [
    ]

    with pytest.raises(IncorectOrderSizeException):
        evaluate_order_price(products)


def test_get_product_list_from_order_code():
    products = [
            HouseholdProduct(name="cheap", price=10),
            HouseholdProduct(name="mid-cheap", price=100),
            HouseholdProduct(name="just-mid", price=1000),
            HouseholdProduct(name="mid-expensive", price=10000),
            HouseholdProduct(name="expensive", price=100000),
            HouseholdProduct(name="extra-product", price=100000),
    ]

    order_code = (1, 0, 0, 1, 1, 1)

    result = get_product_list_from_order_code(products, order_code)

    expected_result = [
        HouseholdProduct(name="cheap", price=10),
        HouseholdProduct(name="mid-expensive", price=10000),
        HouseholdProduct(name="expensive", price=100000),
        HouseholdProduct(name="extra-product", price=100000),
    ]

    assert result == expected_result


def test_get_all_orders_sets_prices():
    products = [
        HouseholdProduct(name="cheap", price=10),
        HouseholdProduct(name="mid-cheap", price=100),
        HouseholdProduct(name="just-mid", price=1000),
    ]

    expected_result = {
        (0, 0, 1): 1000,
        (0, 1, 0): 100,
        (0, 1, 1): 1088,
        (1, 0, 0): 10,
        (1, 0, 1): 1008.8,
        (1, 1, 0): 108.8,
        (1, 1, 1): 1106.6
    }

    result = get_all_orders_sets_prices(products)

    assert result == expected_result


def test__get_all_orders_sets_prices_filters_out_too_large_orders():
    products = [
        HouseholdProduct(name="cheap", price=10),
        HouseholdProduct(name="mid-cheap", price=100),
        HouseholdProduct(name="just-mid", price=1000),
        HouseholdProduct(name="mid-expensive", price=10000),
        HouseholdProduct(name="expensive", price=100000),
        HouseholdProduct(name="extra-product", price=100000),
    ]

    expected_result = sum([binom(6, i) for i in range(1, 6)])

    result = len(get_all_orders_sets_prices(products))

    assert result == expected_result


@pytest.mark.parametrize(
    "products, expected_orders_set",
    [
        (
            [
                HouseholdProduct(name="cheap", price=10),
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="just-mid", price=1000),
            ],
            [
                [
                    HouseholdProduct(name="mid-cheap", price=100),
                    HouseholdProduct(name="just-mid", price=1000),
                ],
                [
                    HouseholdProduct(name="cheap", price=10),
                ],
            ],
        ),
        (
            [
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="mid-cheap-2", price=100),
                HouseholdProduct(name="just-mid", price=1000),
            ],
            [
                [
                    HouseholdProduct(name="mid-cheap", price=100),
                    HouseholdProduct(name="mid-cheap-2", price=100),
                    HouseholdProduct(name="just-mid", price=1000),
                ],
            ],
        ),
    ]
)
def test_get_best_orders_set(products: List[HouseholdProduct], expected_orders_set: List[List[HouseholdProduct]]):
    result = get_best_orders_set(products)

    assert result == expected_orders_set
