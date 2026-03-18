
import re
import time

import pandas as pd
from playwright.sync_api import sync_playwright

from database.connection import get_connection
from site_scrapers.technomarket.parser import scrape_products, get_categories


def technomarket_store_scraper():
    with get_connection() as conn:
        try:
            with sync_playwright() as p:
                print('Connecting to Browser...')
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                # Loading DOM
                base_url = "https://www.technomarket.bg"
                page.goto(base_url)
                try:
                    print('Accepting cookies...')
                    # Closing cookies and ads
                    page.get_by_role("button", name=" Приемам всички").click()
                    page.locator(".login-footer > .tm-button").click()
                    page.locator("#cdk-overlay-1").get_by_role("button").filter(has_text=re.compile(r"^$")).click()
                except Exception as e:
                    print(e)

                # Accessing categories
                try:
                    print('Extracting categories...')
                    categories = get_categories(page, base_url)
                    df = pd.DataFrame(categories)
                    df = df.drop_duplicates(subset=["link"])
                    df.to_csv(f'./data/categories/categories_technomarket.csv', index=False, encoding='utf-8-sig')

                    print('Categories extracted')

                    df = pd.read_csv('./data/categories/categories_technomarket.csv')
                    categories_dict_from_csv = df.to_dict(orient='records')
                    products_count = 0
                    for category in categories_dict_from_csv:
                        current_link = category['link']
                        current_name = category['name']
                        print(f'Extracting category - {current_name} - {current_link}')
                        page.goto(current_link)

                        page_num = 1
                        while True:

                            url = f"{current_link}?page={page_num}"
                            page.goto(url)

                            products = page.locator('tm-product-item')

                            if products.count() == 0:
                                break

                            scrape_products(products, conn)
                            products_count += products.count()

                            time.sleep(1)
                            page_num += 1

                    print(f'Total products scraped: {products_count}')

                except Exception as e:
                    print(e)

                context.close()
                browser.close()

        except Exception as e:
            print(e)

