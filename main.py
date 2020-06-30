from src.household_product import HouseholdProduct
from src.optimization import  get_all_orders_sets_prices

ALL_PRODUCTS = [
    HouseholdProduct(name="Fridge", price=2499),
    HouseholdProduct(name="Dish Washer", price=1599),
    HouseholdProduct(name="Washing Machine", price=1399),
    HouseholdProduct(name="Induction cooker", price=1649),
    HouseholdProduct(name="Canopy", price=499),
    HouseholdProduct(name="Oven", price=1699)
]

result = get_all_orders_sets_prices(ALL_PRODUCTS, 5)
print(result)