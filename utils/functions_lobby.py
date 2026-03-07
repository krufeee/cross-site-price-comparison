import re
import pandas as pd
expected_number_of_products = 0
number_of_scraped_products = 0

# Function for exporting extracted products details in Excel sheet
def export_to_excel(list_of_products, period):
    df = pd.DataFrame(list_of_products)
    df.to_excel(f"Technopolis promotion {period}.xlsx", index=False)
    print('Exported to excel...')

# Functions that exports categories to csv
def export_categories_to_csv(categories, file_name):
    df = pd.DataFrame(categories)
    df = df.drop_duplicates(subset=["code"])
    df.to_csv(f"./data/categories/{file_name}.csv", index=False, encoding="utf-8-sig")




# Counter
def counter(expected=None, scraped=None):
    global expected_number_of_products
    global number_of_scraped_products

    if not expected and not scraped:
        return expected_number_of_products, number_of_scraped_products
    if expected and scraped:
        expected_number_of_products += expected
        number_of_scraped_products += scraped
        return expected_number_of_products, number_of_scraped_products
    elif expected:
        expected_number_of_products += expected
        return expected_number_of_products
    else:
        number_of_scraped_products += scraped
        return number_of_scraped_products
