from playwright.sync_api import sync_playwright
import pandas as pd
from functions_lobby import all_categories_names_and_links, get_all_categories, export_categories_to_csv, extract_product_data
from pathlib import Path

def run():
    with sync_playwright() as p:

        # Starting Chromium browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        print("Opening website...")
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

            # Checking if csv is created
            categories_csv_path = Path("../database/categories.csv")

            if not categories_csv_path.exists():
                print("Extracting categories...")
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
                        # [print(i.get("title")+"-"+i.get("url")) for i in all_categories_names_and_links]
                except:
                    print("Cannot find categories")
            else:
                print("Categories are already extracted.")


            # Extracting products for each category
            try:
                # Function for extracting products from current page
                def get_page_number_return_products(page_number):
                    with page.expect_response(lambda r: "products/search" in r.url and r.status == 200) as res_info:
                        page_size_90_button = page.get_by_role("button", name="90")
                        if page_size_90_button.is_visible():
                            page_size_90_button.click()
                        if not page_number == 1:
                            page.get_by_role("link", name=f"{page_number}", exact=True).click()
                        curr_response = res_info.value
                        curr_data = curr_response.json()
                        return curr_data
                # Reading categories from csv
                df = pd.read_csv("../database/categories.csv")
                # Converting to dict
                categories_list_from_csv = df.to_dict(orient="records")
                sum_products = 0
                # Cycle through categories
                for category in categories_list_from_csv:
                    title = category.get("title")
                    category_link = category.get("link")
                    try:
                        page.goto(category_link)
                        page.wait_for_load_state("networkidle", timeout=30000)
                        current_data = get_page_number_return_products(1)
                        pagination =current_data["pagination"]
                        number_of_pages = int(pagination["totalPages"])
                        number_of_products = pagination["totalResults"]
                        print(f'Found {number_of_products} products in {title}.')
                        sum_products += number_of_products
                    except Exception as e:
                        page.screenshot(path=f"error_{title.replace(' ', '_')}.png", full_page=True)
                        print(f"Cannot process category '{title}': {e}")
                    # Cycle through pages in current category
                    for curr_page in range(1,number_of_pages+1):
                        products = get_page_number_return_products(curr_page)
                        for product in products:
                            current_product = extract_product_data(product)



            except ValueError as e:
                page.screenshot(path=".", type='png')
                print(f"Cannot find products {e}")


        except Exception as e:
            print(f"Error: {e}.")

        print("\nClosing after 5 seconds...")
        page.wait_for_timeout(5000)
        browser.close()





if __name__ == "__main__":
    run()

