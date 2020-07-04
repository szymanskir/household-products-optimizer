import pytest

from typing import List, Tuple
from scipy.special import binom

from src.evaluation import evaluate_order_price_example
from src.household_product import HouseholdProduct
from src.optimization import get_product_list_from_order_code, get_all_orders_sets_prices, \
    get_best_orders_set


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

    result = get_all_orders_sets_prices(products, evaluate_order_price_example)

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

    result = len(get_all_orders_sets_prices(products, evaluate_order_price_example))

    assert result == expected_result


@pytest.mark.parametrize(
    "products, expected_result",
    [
        (
            [
                HouseholdProduct(name="cheap", price=10),
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="just-mid", price=1000),
            ],
            (
                [
                    [
                        HouseholdProduct(name="mid-cheap", price=100),
                        HouseholdProduct(name="just-mid", price=1000),
                    ],
                    [
                        HouseholdProduct(name="cheap", price=10),
                    ],
                ],
                12
            ),
        ),
        (
            [
                HouseholdProduct(name="mid-cheap", price=100),
                HouseholdProduct(name="mid-cheap-2", price=100),
                HouseholdProduct(name="just-mid", price=1000),
            ],
            (
                [
                    [
                        HouseholdProduct(name="mid-cheap", price=100),
                        HouseholdProduct(name="mid-cheap-2", price=100),
                        HouseholdProduct(name="just-mid", price=1000),
                    ],
                ],
                34
            ),
        ),
    ]
)
def test_get_best_orders_set(products: List[HouseholdProduct], expected_result: Tuple[List[List[HouseholdProduct]], float]):
    result = get_best_orders_set(products, evaluate_order_price_example)

    assert result == expected_result
