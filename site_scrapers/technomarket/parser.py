import sqlite3

from database.queries import add_product, add_price


# Function that receives products locator on current page and returns dict with product details
def scrape_products(products, conn):
    cursor = conn.cursor()
    products_on_current_page = []
    number_of_products = products.count()
    for i in range(number_of_products):
        current_product = products.nth(i)
        product_image_locator = current_product.locator('a > picture > img')
        product_image_link = product_image_locator.first.get_attribute('src', '')
        product_details_locator = current_product.locator('.title').first
        product_category = product_details_locator.get_attribute('data-category', '')
        product_link = product_details_locator.get_attribute('href', '')
        product_type_locator = product_details_locator.locator('.type').first
        product_type = product_type_locator.inner_text()
        product_type_plus_category = product_type+"/"+product_category
        product_brand_locator = product_details_locator.locator('.brand').first
        product_brand = product_brand_locator.inner_text()
        product_model_locator = product_details_locator.locator('.name').first
        product_model = product_model_locator.inner_text()
        product_code_locator = current_product.locator('.code').last
        product_code = product_code_locator.inner_text().split()[-1]
        product_price_locator = current_product.locator('.euro_price').first
        product_price_raw = product_price_locator.inner_text().split()
        product_price = float(product_price_raw[0])
        product_name = product_brand + product_model
        store = 'technomarket'
        product_ean = 'ean'
        last_entry_id = ''
        is_product_purchasable = False
        is_purchasable = current_product.locator('.button-text')

        if is_purchasable.is_visible():
                is_product_purchasable = True




        try:
            last_entry_id = add_product(conn, product_name, product_code, product_ean, product_brand, product_model,
                                        product_type_plus_category, product_link,
                                        is_product_purchasable, store, product_image_link)
        except sqlite3.IntegrityError as e:
            print(e)

        try:
            add_price(cursor, last_entry_id, product_price)
        except Exception as e:
            print(e)
    return products_on_current_page