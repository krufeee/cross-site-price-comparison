from playwright.sync_api import sync_playwright
import pandas as pd


def run():
    with sync_playwright() as p:
        # Starting Chromium browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Opening website...")

        try:

            # Чакаме само зареждане на DOM, за да не увисва на реклами
            page.goto("https://www.technopolis.bg/bg/",
                      wait_until="domcontentloaded",
                      timeout=60000)

            # Кликване на бисквитките (ако се появят)
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

            # Кликване на технополис приложението (ако се появи)
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

            # Взимаме всички продуктови категории
            try:
                with page.expect_response(
                        lambda r: "components/topnavigation/topNavigationBarMenu" in r.url and r.status == 200
                ) as resp_info:
                    page.reload()
                    response = resp_info.value
                    data = response.json()
                    test_data_json = data["components"]["component"]
                    all_categories = test_data_json


            except:
                print("Cannot find categories")

        except Exception as e:
            print(f"Error: {e}.")

        print("\nClosing after 5 seconds...")
        page.wait_for_timeout(5000)
        browser.close()





if __name__ == "__main__":
    run()

