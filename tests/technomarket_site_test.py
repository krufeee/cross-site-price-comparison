
import re
import pandas as pd
from playwright.sync_api import sync_playwright



from database import *
# page.locator('.main-navigation > button:nth-child(1)').click()
# categories_menu = page.locator('a.menu-link')
# category_menu_entries = categories_menu.all()
# categories = []
# for menu_entry in category_menu_entries:
#     menu_entry.click()
#     category_container_entries = page.locator('.menu-popup-container > div ')
#     all_category_container_entries = category_container_entries.all()
#     for category_entry in all_category_container_entries:
#         category_locator = category_entry.locator('h4 > a')
#         sub_category_locator = category_entry.locator('div > div > a')
#         if sub_category_locator.count() > 0:
#             all_subcategory_entries = sub_category_locator.all()
#             for sub_category_entry in all_subcategory_entries:
#                 sub_category_name = sub_category_entry.inner_text()
#                 sub_category_link = sub_category_entry.get_attribute('href')
#                 categories.append({'name' : sub_category_name, 'link' : base_url + sub_category_link})
#         else:
#             addon = '/produkti'
#             category = category_locator.first
#             category_name = category.inner_text()
#             category_link = category.get_attribute('href')
#             categories.append({'name' : category_name, 'link' : base_url + addon + category_link})

