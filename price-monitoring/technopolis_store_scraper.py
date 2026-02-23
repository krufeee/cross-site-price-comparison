from playwright.sync_api import sync_playwright
import pandas as pd
from core import all_categories_names_and_links, get_all_categories


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
            # try:
            #     page.wait_for_selector()
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
                print("Ad popup.")
                page.wait_for_timeout(2000)
                page.wait_for_selector(button, timeout=2000)
                page.click(button)
                print('Ad closed.')

            except:
                print("Ad did not show up.")

            # Getting categories
            try:
                with page.expect_response(
                        lambda r: "components/topnavigation/topNavigationBarMenu" in r.url and r.status == 200
                ) as resp_info:
                    page.reload()
                    response = resp_info.value
                    data = response.json()
                    all_categories = data["components"]["component"]

                    get_all_categories(all_categories)

                    # [print(i.get("title")+"-"+i.get("url")) for i in all_categories_names_and_links]
            except:
                print("Cannot find categories")

            # Extracting products
            try:
                # Function for extracting products from current page
                def get_page_number_return_products(page_number):
                    with page.expect_response(lambda r: "products/search" in r.url and r.status == 200) as res_info:
                    #todo if not button.....
                        page.get_by_role("button", name="90").click()
                        if not page_number == 1:
                            page.get_by_role("link", name=f"{page_number}", exact=True).click()
                        curr_response = res_info.value
                        curr_data = curr_response.json()
                        return curr_data
                sum_products = 0
                for category in all_categories_names_and_links:
                    title = category.get("title")
                    category_link = category.get("link")
                    try:
                        page.goto(category_link)
                        page.wait_for_load_state("networkidle", timeout=30000)
                        # page.get_by_role("button", name="90").click()
                        current_data = get_page_number_return_products(1)
                        pagination =current_data["pagination"]
                        number_of_pages = pagination["totalPages"]
                        number_of_products = pagination["totalResults"]
                        print(f'Found {number_of_products} in {title}.')
                        sum_products += number_of_products
                    except Exception as e:
                        page.screenshot(path=f"error_{title.replace(' ', '_')}.png", full_page=True)
                        print(f"Cannot process category '{title}': {e}")
                print(f'Found {sum_products} products.')
                    # for page in range(1,number_of_pages+1):
                    #     products = get_page_number_return_products(page)

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

