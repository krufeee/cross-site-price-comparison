import sqlite3

from database.queries import add_product, add_price


# Function that receives products locator on current page and returns dict with product details
def scrape_products(products, conn, logger):
    cursor = conn.cursor()
    number_of_products = products.count()

    for i in range(number_of_products):
        product_image_link = None
        product_category = None
        product_link = None
        product_type = None
        product_brand = None
        product_model = None
        product_code = None
        product_price = None
        is_product_purchasable = False
        try:
            current_product = products.nth(i)
            product_image_locator = current_product.locator('a > picture > img')
            product_image_link = product_image_locator.first.get_attribute('src')
            product_details_locator = current_product.locator('.title').first
            product_category = product_details_locator.get_attribute('data-category')
            product_link = product_details_locator.get_attribute('href')
            product_brand_locator = product_details_locator.locator('.brand').first
            product_brand = product_brand_locator.inner_text()
            product_model_locator = product_details_locator.locator('.name').first
            product_model = product_model_locator.inner_text()
            product_code_locator = current_product.locator('.code').last
            product_code = product_code_locator.inner_text().split()[-1]
            product_price_locator = current_product.locator('.price')
            product_price_exact_locator = product_price_locator.locator('.euro_price')
            product_price_raw = product_price_exact_locator.inner_text().split()
            product_price = float((product_price_raw[0].replace(',', '')))
            product_name = product_brand + product_model
            store = 'technomarket'
            product_ean = ''
            last_entry_id = ''
            is_product_purchasable = False
            is_purchasable = current_product.locator('.button-text')

            if is_purchasable.count() > 0:
                    is_product_purchasable = True

        except Exception as e:
            logger.exception(f"Грешка при продукт %d на страницата "
                             f"категория -{product_category} - {product_link}", i  )
            continue

        if not all([product_name, product_code, product_price]):
            logger.warning("Пропуснат продукт %d — липсващи данни", i)
            continue


        try:
            last_entry_id = add_product(conn, product_name, product_code, product_ean, product_brand, product_model,
                                        product_category, product_link,
                                        is_product_purchasable, store, product_image_link)
        except sqlite3.IntegrityError as e:
            logger.error(e)

        try:
            add_price(cursor, last_entry_id, product_price)
        except Exception as e:
            logger.error(e)


def get_categories(page, base_url: str) -> list[dict]:
    """Extract all categories and subcategories from the navigation menu."""
    page.locator('.main-navigation > button:nth-child(1)').click()

    menu_links = page.locator('a.menu-link').all()
    categories = []

    for menu_entry in menu_links:
        menu_entry.click()
        container_entries = page.locator('.menu-popup-container > div').all()

        for entry in container_entries:
            categories.extend(_parse_category_entry(entry, base_url))

    return categories


def _parse_category_entry(entry, base_url: str) -> list[dict]:
    """Parse a single category entry, returning subcategories if present."""
    sub_category_links = entry.locator('div > div > a')

    if sub_category_links.count() > 0:
        return _parse_subcategories(sub_category_links.all(), base_url)

    return _parse_main_category(entry.locator('h4 > a').first, base_url)


def _parse_subcategories(sub_entries, base_url: str) -> list[dict]:
    return [
        {
            'name': entry.inner_text(),
            'link': base_url + entry.get_attribute('href')
        }
        for entry in sub_entries
    ]


def _parse_main_category(category, base_url: str) -> list[dict]:
    return [
        {
            'name': category.inner_text(),
            'link': f"{base_url}/produkti{category.get_attribute('href')}"
        }
    ]