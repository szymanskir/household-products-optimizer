from typing import List
from .household_product import HouseholdProduct
from .exceptions import IncorectOrderSizeException


def evaluate_order_price(products: List[HouseholdProduct]) -> float:
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

    sorted_products = sorted(products, key=lambda product: product.price, reverse=True)
    cheapest_product = sorted_products[-1]
    sorted_products[-1].price = get_discounted_price(
        cheapest_product.price, item_number
    )

    return sum([product.price for product in sorted_products])
