
from branch_example import branch
from json_test import test_data


# def get_category_details(current_category):
#         c_name = current_category.get('link').get('linkName'),
#         c_url = current_category.get('link').get('url'),
#         c_children = current_category.get('navigationNode').get('children'),
#         return c_name, c_url, c_children



# print(f"\n{current_category_details['name']}\n{current_category_details['url']}\n{current_category_details['children']}")

# result = [print(p) for p in current_category_details['children']]

# name = current_category.get('link').get('linkName')
# print (name)
#

# print (current_category)

# for category in test_data:
#     try:
#         name = get_category_details(category)[0][0]
#         children = get_category_details(category)[2]
#         if children:
#             for child in children:
#                 if child:
#                     for i in child:
#                         if i :
#                          print(i['title'])
        # children = get_category_details(category)[2]
        # print(children)
        # try:
        #     for child in children:
        #         child_name = child.get('entries').get('link').get('linkName')
        #         print(child_name)
        # except:
        #     print("No children")

    #
    # except:
    #     print("Empty data")


# category_details = get_category_details(test_data[9])
# category_name = category_details[0][0]
# category_url = category_details[1]
# category_children = category_details[2]
# first_child = category_children[0]
# grand_children = category_children[0].get("children")
#
# print(category_details[2])
#

# ex = {
#   "category_code": "P11090703",
#   "category_name": "Кабели",
#   "category_url": "/TV--Video-i-Gaming/TV-aksesoari/Kabeli/c/P11090703",
#   "category_path": "TV Аудио и Gaming > TV аксесоари > Кабели",
#   "depth": 3
# }

#
# def walk_node(node, path=None):
#     path = path or []
#
#     # 1. Ако има категория
#     for entry in node.get("entries", []):
#         link = entry.get("link", {})
#         name = link.get("linkName")
#         url = link.get("url")
#         code = link.get("categoryCode") or link.get("category")
#
#         if name and url:
#             yield {
#                 "category_code": code,
#                 "category_name": name,
#                 "category_url": url,
#                 "category_path": " > ".join(path + [name]),
#                 "depth": len(path) + 1
#             }
#
#     # 2. Слизаме към децата
#     for child in node.get("children", []):
#         child_title = child.get("title")
#         new_path = path + [child_title] if child_title else path
#         yield from walk_node(child, new_path)
#
#
#
# all_categories = test_data
#
# root_link = all_categories.get("link", {})
# root_name = root_link.get("linkName")
#
# for child in all_categories.get("navigationNode", {}).get("children", []):
#     all_categories.extend(
#         list(walk_node(child, [root_name]))
#     )


current_branch = branch
all_categories = test_data

# current_branch_name = current_branch.get('link').get('linkName')
# current_branch_node = current_branch.get('navigationNode')
# current_branch_children = current_branch_node['children']
# for child in current_branch_children:
#     child_entries = child.get('entries')
#     for entry in child_entries:
#         print(entry.get('link').get('linkName'))

# for category in all_categories:
#     branches = category.get('navigationNode')
#     branch_children = branches.get('children')
#     category_title = branches.get('title')
#     print(category_title)
#     for child in branch_children:
#         sub_child_title = child.get('title')
#         entries = child.get('entries')
#         print(f"  {sub_child_title}") if sub_child_title else None
#         if not entries:
#             subchild = child.get('children')
#             for sub_child in subchild:
#                 sub_child_title = sub_child.get('title')
#                 entries = sub_child.get('entries')
#                 print(f"    {sub_child_title}") if sub_child_title else None
all_categories_names_and_links = []

def extract_tree_info(node, depth=0):

    """Extract info from tree node at any depth"""
    title = node.get('title')
    entries = node.get('entries')
    children = node.get('children', [])
    category_details = {
        'title':'title',
        'url': 'url'
    }
    # Get title
    if title:
        category_details['title'] = title

    # Get url
    if entries:
        for entry in entries:
            title = entry.get('link').get('linkName')
            category_details['title'] = title
            url = entry.get('link').get('url')
            if url:
                category_details['url'] = url
                all_categories_names_and_links.append(category_details)

    # Recursively process children
    for child in children:
        extract_tree_info(child, depth + 1)




for category in all_categories:
    root_node = category.get('navigationNode')
    if root_node:
        extract_tree_info(root_node)






