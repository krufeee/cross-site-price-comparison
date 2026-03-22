import re

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
    slug = url.split('/')[-3]  # 'Televizor-TELEFUNKEN-24HA6001-LED'

    # Намираме всички части с главни букви
    parts = slug.split('-')
    try:
        upper_parts = [p for p in parts if p.isupper() or (p[0].isupper() and re.search(r'\d', p))]

    except Exception as e:
        return None, None


    if not upper_parts:
        return None, None

    brand = upper_parts[0]
    model = '-'.join(upper_parts[1:]) if len(upper_parts) > 1 else None

    return brand, model

# Function for extracting product details for current product
def extract_product_data(current_product):
    brand_name = None
    model = None
    image_url = ''
    image = current_product.get('images', [])
    if image:
        image_url = image[0].get('url', "")

    raw_name = current_product.get('name')
    current_url = current_product.get("url", "")
    brand_name, model = extract_model(current_url)
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
        "image_url": image_url,
    }

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
