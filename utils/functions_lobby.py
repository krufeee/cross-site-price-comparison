import re
import pandas as pd
expected_number_of_products = 0
number_of_scraped_products = 0
all_categories_names_and_links = []
# Function that extracts info from category in any depth
def extract_tree_info(node, depth=0):
    title = node.get('title')
    entries = node.get('entries')
    children = node.get('children', [])
    web_link = "https://www.technopolis.bg/bg"
    category_details = {
        'code': 'code',
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
                category_code = link.split('/c/')[-1]
                category_details['code'] = category_code
                category_details['link'] = web_link + link
                all_categories_names_and_links.append(category_details)

    # Recursively process children
    for child in children:
        extract_tree_info(child, depth + 1)

# Function that cycles through categories and calls function for extracting info
def get_all_categories(data):
    for category in data:
        root_node = category.get('navigationNode')
        if root_node:
            extract_tree_info(root_node)

# Function that receives url and return brand and model for product
def extract_model(url):
    # Pattern за различни варианти
    pattern = r"Televizor-([A-Za-z0-9]+)-([A-Za-z0-9]+)"
    match = re.search(pattern, url)
    if match:
        return {
            'brand': match.group(1),
            'model': match.group(2),
            'success': True
        }
    else:
        return {
            'brand': None,
            'model': None,
            'success': False
        }

# Function for extracting product details for current product
def extract_product_data(current_product):
    brand_name = ''
    model = ''
    raw_name = current_product.get('name')
    current_url = current_product.get("url", "")
    extracted_data = extract_model(current_url)
    extracted_state = extracted_data.get('success')
    if extracted_state:
        brand_name = extracted_data.get('brand')
        model = extracted_data.get('model')
    ean = current_product.get("ean", "")
    purchasable = current_product.get('purchasable')
    price = float(current_product.get('price', {}).get("value"))
    if not price:
        formatted_price = current_product.get('price', {}).get("formattedValue")
        price = formatted_price.split()[0]
    link = "https://www.technopolis.bg" + current_url
    code = current_product.get("code", "")
    return {
        "ean": ean,
        "code": code,
        "name": raw_name,
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

# Functions that exports categories to csv
def export_categories_to_csv(categories):
    df = pd.DataFrame(categories)
    df = df.drop_duplicates(subset=["code"])
    df.to_csv("./database/categories_technopolis.csv", index=False, encoding="utf-8-sig")

# Function that adds products to sqlite

# Function for extracting products from API
def get_products_from_api(page_obj, curr_code, page_num, page_size):
    default_fields = ("products(DEFAULT,averageRating,images(FULL),classifications,manufacturer,numberOfReviews,"
                      "categories(FULL),baseOptions,baseProduct,variantOptions,variantType,potentialPromotions(FULL)),"
                      "facets,breadcrumbs,pagination(DEFAULT),sorts(DEFAULT),freeTextSearch,currentQuery,minPrice,"
                      "maxPrice,breadcrumbDatas,spellingSuggestion")
    api_url = "https://api.technopolis.bg/videoluxcommercewebservices/v2/technopolis-bg/products/search"
    params = {
        "fields": default_fields,
        "query": f":relevance:allCategories:{curr_code}",
        "currentPage": page_num,
        "pageSize": page_size,
        "categoryCode": curr_code,
        "lang": "bg",
        "curr": "EUR",
        "servicingStore": "1302",
        "postalCode": "1000"
    }

    res = page_obj.request.get(api_url, params=params)


    if not res.ok:
        print(f"API Error {res.status}: {res.text()[:200]}")
        return {}
    return res.json()

# Counter
def counter(expected=None, scraped=None):
    global expected_number_of_products
    global number_of_scraped_products

    if not expected and not scraped:
        return expected_number_of_products, number_of_scraped_products
    if expected and scraped:
        expected_number_of_products += expected
        number_of_scraped_products += scraped
        return expected_number_of_products, number_of_scraped_products
    elif expected:
        expected_number_of_products += expected
        return expected_number_of_products
    else:
        number_of_scraped_products += scraped
        return number_of_scraped_products
