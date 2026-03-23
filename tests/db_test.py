# if __name__ == "__main__":
#     # 1. Initialize Database
#     init_db()
from database.sqlite_db import add_product, add_price

# try:
#     add_product('634342', 'wwf', 'frizer', True, )
#
# except sqlite3.IntegrityError:
#     print("⚠️ Product code already exists!")


#
# product = get_product_id_by_prod_code("634342")
# product_id = product[0]
# price = 554
#
# try:
#     old_price = get_price_by_prod_id(product_id)
#     last_old_price = old_price[-1][2]
#     if last_old_price != price:
#         add_price(product_id, price)
#     else:
#         print('price is equal to old_price')
# except sqlite3.IntegrityError:
#     print("No product found")

add_price(333,222)

