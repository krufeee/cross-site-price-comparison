product = (
            '<a class="product-image" href="/telefoni/nokia-105-ds-black-2025-09225845" aria-label="NOKIA 105 DS BLACK 2025">'
                '<div class="bottom-left product-ol">'
                    '<img width="60" height="60" alt="" src="https://cdn.technomarket.bg/ng/media/cache/min_thumb/uploads/BG/2025/badge-2025/NOKIAcharger/120x120/charger NOKIA 2-2_75 W-120x120.png.webp">'
                '</div>'
                '<picture>'
                    '<img loading="lazy" src="https://cdn.technomarket.bg/ng/240/uploads/library/product/09225845/6786287934a14.jpg.webp" width="240" height="240" alt="NOKIA 105 DS BLACK 2025">'
                '</picture>'
                '<div class="view-details">'
                    '<span class="icon-search"></span>'
                    '<span>Виж повече</span>'
                '</div>'
            '</a>'
            '<div class="overview">'
                '<a class="title" href="/telefoni/nokia-105-ds-black-2025-09225845" data-category="Телефони и Таблети|Мобилни телефони|NO OS" data-brand="NOKIA">'
                    '<span class="type">МОБИЛЕН ТЕЛЕФОН </span>'
                    '<span class="brand">NOKIA </span>'
                    '<span class="name">105 DS BLACK 2025</span>'
                '</a>'
                '<tm-star-rating>'
                    '<div class="stars empty">'
                        '<span class="icon-star_outline"></span>'
                        '<span class="icon-star_outline"></span>'
                        '<span class="icon-star_outline"></span>'
                        '<span class="icon-star_outline"></span>'
                        '<span class="icon-star_outline"></span>'
                        '<span class="count">(0)</span>'
                    '</div>'
                '</tm-star-rating>'
                '<div class="code">'
                    '<span class="b">Код на продукта: </span>'
                    '<span>09225845</span>'
                '</div>'
                '<div class="badges">'
                '</div>'
                '<div class="specifications">'
                    '<div class="line">'
                        '<span class="label">Резолюция</span>'
                        '<span class="value"> 120X160</span>'
                    '</div>'
                    '<div class="line">'
                        '<span class="label">Цвят</span>'
                        '<span class="value"> Черен</span>'
                    '</div>'
                    '<div class="line">'
                        '<span class="label">БАТЕРИЯ</span>'
                        '<span class="value"> 1000 mAh</span>'
                    '</div>'
                    '<div class="line">'
                        '<span class="label"></span>'
                        '<span class="value"> FM Радио</span>'
                    '</div>'
                '</div>'
                '<div class="energy-class-wrap">'
                '</div>'
            '</div>'
            '<div class="action">'
                '<div class="price-block">'
                    '<div class="old-price">'
                    '</div>'
                    '<div class="price">'
                        '<span>'
                            '<tm-price>'
                                '<span class="bgn_price">45.98 лв.'
                                    '<span class="divider">/'
                                    '</span>'
                                '</span>'
                                '<span class="euro_price"> 23.51 €'
                                    '<span class="divider">/'
                                    '</span>'
                                '</span>'
                            '</tm-price>'
                        '</span>'
                    '</div>'
                '</div>'
                '<div class="action-buttons">'
                    '<button data-action="addCart" class="tm-button gi2 add-cart">'
                        '<span class="icon-add_shopping_cart"></span>'
                        '<span class="button-text">Добави '
                        '<span class="addcart-hidetxt">в количка</span>'
                        '</span>'
                    '</button>'
                '</div>'
                '<div class="extra">'
                    '<button data-action="toggleCompare" aria-label="add to compare" class="tm-button compare" data-type="МОБИЛЕН ТЕЛЕФОН">'
                        '<span class="button-text">Сравни</span>'
                    '</button>'
                    '<button data-action="toggleFavorite" aria-label="add to favorite" class="tm-button fav">'
                        '<span class="button-text">Любими</span>'
                    '</button>'
                '</div>'
            '</div>'
)
# Function that receives products locator on current page and returns dict with product details
def scrape_products(products):
    products_on_current_page = []
    number_of_products = products.count()
    for i in range(number_of_products):
        current_product = products.nth(i)
        product_image_locator = current_product.locator('a > picture > img')
        product_image_link = product_image_locator.first.get_attribute('src')
        product_details_locator = current_product.locator('.title').first
        product_category = product_details_locator.get_attribute('data-category')
        product_link = product_details_locator.get_attribute('href')
        product_type_locator = product_details_locator.locator('.type').first
        product_type = product_type_locator.inner_text()
        product_brand_locator = product_details_locator.locator('.brand').first
        product_brand = product_brand_locator.inner_text()
        product_model_locator = product_details_locator.locator('.name').first
        product_model = product_model_locator.inner_text()
        product_code_locator = current_product.locator('.code').last
        product_code = product_code_locator.inner_text().split()[-1]
        product_price_locator = current_product.locator('.euro_price').first
        product_price_raw = product_price_locator.inner_text().split()
        product_price = float(product_price_raw[0])
        product_name = product_brand + product_model

        product_details = {
            'name': product_name,
            'price': product_price,
            'type': product_type,
            'code': product_code,
            'ean': 'ean',
            'brand': product_brand,
            'model': product_model,
            'category': product_category,
            'url': product_link,
            'available': True,
            'store' : 'technomarket',
            'image': product_image_link,
        }
        products_on_current_page.append(product_details)
        print(product_details)
        break
    return products_on_current_page