from importlib.resources import files
from pathlib import Path
import pandas as pd
import re

# csv_file = Path("../database/categories.csv")
#
# # if not csv_file.exists():
# #     print("File does not exist")
# # else:
# #     print("File exists")
#
#
# df = pd.read_csv("../database/categories.csv")
# # print(df.head(20))
# products = df.to_dict(orient="records")
# print(products)


# name = ['Фурнa за вграждане MIDEA MO 655 FBK 65, A ',
#         'Смартфон GSM HUAWEI Pura 80 Pro Glazed White 6.80 ", 512 GB, RAM 12 GB, 50+48+50+1.5 MP',
#         'Телевизор SMARTTECH 24HG01VC LED SMART TV, GOOGLE TV, 24.0 ", 60.0 см',
#         'DSLR фотоапарат CANON EOS 2000D EF-S 18-55 III DC 24.1 MPx, WI-FI',
#          ]
#
# brand = ['MIDEA', 'HUAWEI', 'SMARTTECH', 'CANON' ]
#


import pandas as pd

products = [
    {
        "product_code": "123",
        "product_name": "TV Samsung",
        "price": 999.99
    },
    {
        "product_code": "456",
        "product_name": "LG TV",
        "price": 799.99
    }
]

# df = pd.DataFrame(products)
# df.to_csv("products.csv", index=False, encoding="utf-8-sig")
# df = pd.read_csv("products.csv")
# print(df.head())

import csv
products_csv = Path(__file__).parent / "products.csv"
def load_existing_product_codes(product_csv_file):
    codes = set()

    try:
        with open(product_csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                codes.add(row["product_code"])
    except FileNotFoundError:
        print("CSV file not found. Will create new one.")

    return codes

existing_codes = load_existing_product_codes("products.csv")

new_products = []

for product in products:
    code = product["product_code"]

    if code not in existing_codes:
        print("New product:", code)
        # добавяш към CSV
        existing_codes.add(code)
        new_products.append(product)

