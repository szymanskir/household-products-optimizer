from typing import List

from src.exceptions import IncorectOrderSizeException
from src.household_product import HouseholdProduct


def evaluate_order_price_example(products: List[HouseholdProduct]) -> float:
    item_number = len(products)

    if item_number > 5 or item_number < 1:
        raise IncorectOrderSizeException

    def get_discounted_price(price: float, item_number: int):
        discount_price = {
            1: price,
            2: 0.88 * price,
            3: 0.66 * price,
            4: 0.33 * price,
            5: 1,
        }

        return discount_price[item_number]

    sorted_products_prices = sorted([product.price for product in products], reverse=True)
    sorted_products_prices[-1] = get_discounted_price(
        sorted_products_prices[-1], item_number
    )

    return sum(sorted_products_prices)
