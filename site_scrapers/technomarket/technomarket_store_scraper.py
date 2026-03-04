import re

from playwright.sync_api import sync_playwright

def technomarket_store_scraper():
    try:
        with sync_playwright() as p:
            print('Connecting to Browser...')
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            # Loading DOM
            base_url = "https://www.technomarket.bg/"
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
                all_categories = categories_menu.all()
                categories = []
                for c_link in all_categories:
                    category_name = c_link.inner_text()
                    # print(category_name)
                    categories_details = {
                        'name': 'name',
                        'link': 'link'
                    }
                    sub_category_container = page.locator('.menu-W002')
                    sub_category_container.is_visible()
                    c_link.click()
                    subcategories = page.locator('.menu-popup-container > div > h4 > a')
                    all_subcategories = subcategories.all()
                    for s_cat in all_subcategories:
                        main_name = s_cat.inner_text()
                        href = s_cat.get_attribute("href")
                        s_url = base_url + href
                        sub_subcategories = page.locator('.menu-popup-container > div:nth-child(1) > div:nth-child(2) > div > a')
                        # if sub_subcategories.count() == 0:
                        #     categories_details['link'] = s_url
                        #     categories_details['name'] = main_name
                        #     categories.append(categories_details)
                        #     continue
                        # all_sub_subcategories = sub_subcategories.all()
                        # for s_s_cat in all_sub_subcategories:
                        #     s_s_cat_href = s_s_cat.get_attribute("href")
                        #     s_s_cat_text = s_s_cat.inner_text()
                        #     s_s_cat_url = s_url + s_s_cat_href
                        #     s_s_cat_name = main_name + ' ' + s_s_cat_text
                        #     categories_details['link'] = s_s_cat_url
                        #     categories_details['name'] = s_s_cat_name
                        #     categories.append(categories_details)











            except Exception as e:
                print(e)


            # ---------------------
            context.close()
            browser.close()

    except Exception as e:
        print(e)




        # browser.close()



technomarket_store_scraper()