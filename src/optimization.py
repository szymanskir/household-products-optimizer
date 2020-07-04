import numpy as np
from typing import List, Dict
from itertools import product
from scipy.optimize import linprog
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

    sorted_products_prices = sorted([product.price for product in products], reverse=True)
    sorted_products_prices[-1] = get_discounted_price(
        sorted_products_prices[-1], item_number
    )

    return sum(sorted_products_prices)


def get_product_list_from_order_code(products: List[HouseholdProduct], order_codes) -> List[HouseholdProduct]:
    indices = np.array(order_codes) == 1
    products_array = np.array(products)
    selected_products = products_array[indices]

    return selected_products.tolist()


def get_all_orders_sets_prices(products: List[HouseholdProduct]) -> Dict[List[int], float]:
    products_count: int = len(products)
    orders_codes = product([0, 1], repeat=products_count)

    def evaluate_order_price_wrapper(products: List[HouseholdProduct]):
        try:
            result = evaluate_order_price(products)
        except IncorectOrderSizeException:
            result = None

        return result

    result = {order_code: evaluate_order_price_wrapper(get_product_list_from_order_code(products, order_code))
              for order_code in orders_codes}
    return {order_code: price for order_code, price in result.items() if price is not None}


def get_best_orders_set(products: List[HouseholdProduct]) -> List[List[HouseholdProduct]]:
    orders_sets_prices = get_all_orders_sets_prices(products)
    orders_codes = list(orders_sets_prices.keys())

    n = len(products)
    m = len(orders_sets_prices)
    c = np.array(list(orders_sets_prices.values()))
    A = - np.array(orders_codes).T
    b = - np.ones(n)
    bounds = [(0, 1) for i in range(m)]

    result = linprog(c, A, b, None, None, bounds)
    optimal_orders_indices = [arg[0] for arg in np.argwhere(result.x > 0.9)]

    return [get_product_list_from_order_code(products, orders_codes[i]) for i in optimal_orders_indices]
