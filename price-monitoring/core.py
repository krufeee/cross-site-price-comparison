all_categories_names_and_links = []

def extract_tree_info(node, depth=0):
    #Function for extracting info from tree node at any depth"""
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
    return {
        "name": current_product.get("name"),
        "price": float(current_product.get("price", {}).get("value")),
        "link": "https://www.technopolis.bg" + current_product.get("url", ""),

    }


# Function for exporting extracted products details in excel sheet
def export_to_excel(list_of_products, period):
    df = pd.DataFrame(list_of_products)
    df.to_excel(f"Technopolis promotion {period}.xlsx", index=False)
    print('Exported to excel...')