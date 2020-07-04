from src.evaluation import evaluate_order_price_rtv_euro_agd
from src.household_product import HouseholdProduct
from src.optimization import get_best_orders_set

ALL_PRODUCTS = [
    HouseholdProduct(name="Fridge", price=2499),
    HouseholdProduct(name="Dish Washer", price=1599),
    HouseholdProduct(name="Washing Machine", price=1399),
    HouseholdProduct(name="Induction cooker", price=1649),
    HouseholdProduct(name="Canopy", price=499),
    HouseholdProduct(name="Oven", price=1699),
    HouseholdProduct(name="Sink", price=739),
]

result = get_best_orders_set(ALL_PRODUCTS, evaluate_order_price_rtv_euro_agd)
print(result)
