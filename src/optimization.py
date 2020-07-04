import numpy as np
from typing import List, Dict, Callable, Tuple
from itertools import product

from pulp import LpProblem, LpMinimize, LpVariable, lpSum
from scipy.optimize import linprog
from .household_product import HouseholdProduct
from .exceptions import IncorectOrderSizeException


def get_product_list_from_order_code(products: List[HouseholdProduct], order_codes) -> List[HouseholdProduct]:
    indices = np.array(order_codes) == 1
    products_array = np.array(products)
    selected_products = products_array[indices]

    return selected_products.tolist()


def get_all_orders_sets_prices(products: List[HouseholdProduct], evaluate_order_price: Callable[[List[HouseholdProduct]], float]) -> Dict[List[int], float]:
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


def get_best_orders_set(products: List[HouseholdProduct], evaluate_order_price: Callable[[List[HouseholdProduct]], float]) -> Tuple[List[List[HouseholdProduct]], float]:
    orders_sets_prices = get_all_orders_sets_prices(products, evaluate_order_price)
    orders_codes = list(orders_sets_prices.keys())

    prob = LpProblem("Optimal orders problem", LpMinimize)
    orders_vars = LpVariable.dicts("Order", orders_codes, lowBound=0, cat='Integer')
    prob += lpSum([orders_sets_prices[order_code] * orders_vars[order_code] for order_code in orders_codes])
    for product in range(len(products)):
        prob += lpSum([order_code[product] * orders_vars[order_code] for order_code in orders_codes]) >= 1
    prob.solve()

    x = np.array([int(v.varValue) for v in prob.variables()])
    optimal_orders_indices = [arg[0] for arg in np.argwhere(x == 1)]

    base_price = sum([product.price for product in products])
    discounted_price = sum([orders_sets_prices[orders_codes[i]] for i in optimal_orders_indices])
    discount = base_price - discounted_price

    return [get_product_list_from_order_code(products, orders_codes[i]) for i in optimal_orders_indices], discount
