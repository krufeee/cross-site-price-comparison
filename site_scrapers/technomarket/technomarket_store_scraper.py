
import re
import pandas as pd
from playwright.sync_api import sync_playwright

def technomarket_store_scraper():
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
                page.locator('.main-navigation > button:nth-child(1)').click()
                categories_menu = page.locator('a.menu-link')
                category_menu_entries = categories_menu.all()
                categories = []
                for menu_entry in category_menu_entries:
                    menu_entry.click()
                    category_container_entries = page.locator('.menu-popup-container > div ')
                    all_category_container_entries = category_container_entries.all()
                    for category_entry in all_category_container_entries:
                        category_locator = category_entry.locator('h4 > a')
                        sub_category_locator = category_entry.locator('div > div > a')
                        if sub_category_locator.count() > 0:
                            all_subcategory_entries = sub_category_locator.all()
                            for sub_category_entry in all_subcategory_entries:
                                sub_category_name = sub_category_entry.inner_text()
                                sub_category_link = sub_category_entry.get_attribute('href')
                                categories.append({'name' : sub_category_name, 'link' : sub_category_link})
                        else:
                            category = category_locator.first
                            category_name = category.inner_text()
                            category_link = category.get_attribute('href')
                            categories.append({'name' : category_name, 'link' : category_link})


                df = pd.DataFrame(categories)
                df = df.drop_duplicates(subset=["link"])
                df.to_csv(f"../../database/categories_technomarket.csv", index=False, encoding="utf-8-sig")

                print('Categories extracted')

                df = pd.read_csv('../../data/categories/categories_technomarket.csv')
                categories_dict_from_csv = df.to_dict(orient="records")

                for category in categories_dict_from_csv:
                    current_link = base_url + category['link']
                    current_name = category['name']
                    print(f'Extracting category - {current_name} ...')
                    page.goto(current_link)
                    pagination = page.locator('.pages > a')
                    if pagination.count() > 0:
                        next_page_button = pagination.last
                        next_button = next_page_button.get_attribute('.class')
                        print(next_button)
                    else:
                        print('Only one page here')







            except Exception as e:
                print(e)

            context.close()
            browser.close()

    except Exception as e:
        print(e)


technomarket_store_scraper()