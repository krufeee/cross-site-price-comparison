import time

from playwright.sync_api import sync_playwright
import pandas as pd
from database.sqlite_db import get_connection, add_multiple_products
from utils.functions_lobby import all_categories_names_and_links, get_all_categories, export_categories_to_csv, \
    get_products_from_api,counter


def technopolis_store_scraper():
    with get_connection() as conn:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                extra_http_headers={
                    "Accept": "application/json",
                    "Accept-Language": "bg,en;q=0.9",
                }
            )
            page = context.new_page()
            print('Opening browser...')
            try:
                # Loading DOM
                page.goto("https://www.technopolis.bg/bg/",
                          wait_until="domcontentloaded",
                          timeout=60000)

                # Accepting cookies
                selector = "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    page.click(selector)
                    print("Accepted cookies.")
                except:
                    print("Cookies are accepted already.")

                page.wait_for_timeout(2000)

                # Closing ad
                selector = ".modal-container"
                button = ".modal-close"
                try:
                    page.wait_for_selector(selector, timeout=2000)
                    page.wait_for_timeout(2000)
                    page.wait_for_selector(button, timeout=2000)
                    page.click(button)
                    print('Ad closed.')
                except:
                    print("Ad did not show up.")

                # Extracting categories
                try:
                    with page.expect_response(
                            lambda r: "components/topnavigation/topNavigationBarMenu" in r.url and r.status == 200
                    ) as resp_info:
                        page.reload()
                        response = resp_info.value
                        data = response.json()
                        all_categories = data["components"]["component"]
                        # getting categories
                        get_all_categories(all_categories)
                        # exporting categories into csv
                        export_categories_to_csv(all_categories_names_and_links)

                except Exception as e:
                    print(f"Error: {e}.")

                # Extracting products for each category
                try:
                    # Reading categories from csv
                    df = pd.read_csv("./database/categories.csv")

                    # Converting to dict
                    categories_list_from_csv = df.to_dict(orient="records")

                        # Cycle through categories
                    for category in categories_list_from_csv:
                        time.sleep(0.2)
                        title = category.get("title")
                        code = category.get("code")
                        if code == 'Promotions':
                            continue
                        data = get_products_from_api(page, code,1,90)
                        if not data:
                            continue
                        pagination = data.get("pagination", {})
                        number_of_pages = pagination.get("totalPages", 0)
                        number_of_products = pagination.get("totalResults", 0)
                        if number_of_pages == 0:
                            continue

                        print(f'Extracting category {title}, pages found: {number_of_pages} with {number_of_products} products.')

                        counter(number_of_products,'')

                        for curr_page in range(number_of_pages):
                            data = ''
                            for attempt in range(3):
                                data = get_products_from_api(page, code, curr_page, 90)
                                if data:
                                    break
                                time.sleep(1)
                            products = data.get("products")
                            if not products:
                                continue
                            add_multiple_products(conn, products, title)
                            time.sleep(0.2)

                        print(f'Extracting {title} finished successfully.')

                        scraped_products = counter('','')[1]
                        expected_products = counter('','')[0]
                    print(f'Found {expected_products}, extracted {scraped_products} products.')
                    conn.commit()

                except ValueError as e:
                    page.screenshot(path=".", type='png')
                    print(f"Cannot find products {e}")

                print('Finished.')

            except Exception as e:
                print(f"Error: {e}.")

            print("\nClosing after 1 seconds...")
            page.wait_for_timeout(1000)
            browser.close()

