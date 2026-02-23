import re
import pandas as pd


# Function for extracting info from tree node at any depth"""
all_categories_names_and_links = []
def extract_tree_info(node, depth=0):
    title = node.get('title')
    entries = node.get('entries')
    children = node.get('children', [])
    web_link = "https://www.technopolis.bg/bg"
    category_details = {
        'title':'title',
        'link': 'link'
    }
    # Get title
    if title:
        category_details['title'] = title

    # Get url
    if entries:
        for entry in entries:
            title = entry.get('link').get('linkName')
            category_details['title'] = title
            link = entry.get('link').get('url')
            if link:
                category_details['link'] = web_link + link
                all_categories_names_and_links.append(category_details)

    # Recursively process children
    for child in children:
        extract_tree_info(child, depth + 1)

def get_all_categories(data):
    for category in data:
        root_node = category.get('navigationNode')
        if root_node:
            extract_tree_info(root_node)




# Function for extracting product details for current product
def extract_product_data(current_product):
    raw_name = current_product.get('name')
    brand_name = current_product.get('brand')
    model = extract_model(raw_name, brand_name)
    purchasable = current_product.get('purchasable')
    price = float(current_product.get('price', {}).get("value"))
    link = "https://www.technopolis.bg" + current_product.get("url", "")
    code = current_product.get("code", "")
    return {
        "code": code,
        "brand": brand_name,
        "model": model,
        "price": price,
        "purchasable": purchasable,
        "link": link,
    }


# Function for exporting extracted products details in Excel sheet
def export_to_excel(list_of_products, period):
    df = pd.DataFrame(list_of_products)
    df.to_excel(f"Technopolis promotion {period}.xlsx", index=False)
    print('Exported to excel...')


def export_categories_to_csv(categories):
    df = pd.DataFrame(categories)
    df.to_csv("../database/categories.csv", index=False, encoding="utf-8-sig")


def extract_model(name: str, brand: str) -> str:
    """
    Опитва се да извлече модела от името на продукта след марката.
    """
    if not brand or not name:
        return ""

    # 1. Нормализираме – премахваме излишни интервали и правим case-insensitive
    name_clean  = re.sub(r'\s+', ' ', name.strip())
    brand_clean = brand.strip().upper()

    # 2. Намираме къде започва марката (приблизително)
    #    Търсим я като дума или в началото
    pattern_brand = r'(?:^|\s|[-/])' + re.escape(brand_clean) + r'(?:\s|[-/]|$)'
    match_brand = re.search(pattern_brand, name_clean.upper(), re.IGNORECASE)

    if not match_brand:
        # марката я няма → връщаме първата дума след типа или цялото име без типа
        return guess_model_without_brand(name_clean)

    # Започваме от края на марката
    start_pos = match_brand.end()

    # Взимаме текста след марката
    after_brand = name_clean[start_pos:].strip()

    # 3. Типични патерни за модел (най-често срещаните в твоите примери)
    model_patterns = [
        r'^([A-Z0-9]{2,}[ /-]?[A-Z0-9]{2,}[ /-]?[A-Z0-9]{1,5})\b',          # MO655, Pura80, EOS2000D, 24HG01
        r'^([A-Z]+ ?[0-9]{2,}(?: ?Pro| ?Ultra| ?Lite| ?Max)?)\b',           # Pura 80 Pro
        r'^([A-Z0-9]+(?:[- ][A-Z0-9]+){1,3})\b',                             # EOS 2000D, 24HG01VC
        r'^([A-Z]{2,} ?[0-9]{3,})\b',                                        # MO 655
    ]

    for pat in model_patterns:
        m = re.match(pat, after_brand, re.IGNORECASE)
        if m:
            model = m.group(1).strip()
            # премахваме евентуални оставащи интервали
            return re.sub(r'\s+', ' ', model)

    # Ако нищо не пасна → взимаме първите 2–4 токена след марката
    words = after_brand.split()
    if len(words) >= 2:
        return " ".join(words[:2])   # Pura 80, MO 655, EOS 2000D
    elif words:
        return words[0]

    return ""

def guess_model_without_brand(name: str) -> str:
    # Ако марката не е намерена – опит за типичен модел в края или средата
    # Пример: "DSLR фотоапарат CANON EOS 2000D ..." → EOS 2000D
    m = re.search(r'\b([A-Z0-9]{2,}[ /-]?[A-Z0-9]{2,}[ /-]?[A-Z0-9]{1,5})\b', name, re.I)
    if m:
        return m.group(1)
    return ""