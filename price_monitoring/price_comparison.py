from rapidfuzz import fuzz


from config import searched_products, THRESHOLD
from database.queries import get_last_price_for_products
from utils.normalize import normalize

results = {}
all_products = get_last_price_for_products()

for search_term in searched_products:
    norm_search = normalize(search_term)
    matches = []

    for product in all_products:
        # Сравняваме по model и name
        norm_model = normalize(product['model'])
        norm_name = normalize(product['name'])

        score_model = fuzz.partial_ratio(norm_search, norm_model)
        score_name = fuzz.partial_ratio(norm_search, norm_name)
        score = max(score_model, score_name)

        if score >= THRESHOLD:
            matches.append({
                'store': product['store'],
                'name': product['name'],
                'price': product['price'],
                'url': product['url'],
                'score': score,
                'scraped_at': product['scraped_at']
            })

    # Сортираме по цена
    matches.sort(key=lambda x: x['price'])
    results[search_term] = matches

for search_term, matches in results.items():
    print(f"\n{'=' * 60}")
    print(f"Търсено: {search_term}")

    if not matches:
        print("  Няма намерени продукти")
        continue

    for m in matches:
        print(f"  {m['store']:<15} {m['price']:>10.2f} лв.  (score: {m['score']})  {m['url']}")

    if len(matches) >= 2:
        diff = matches[-1]['price'] - matches[0]['price']
        print(f"  >>> Разлика: {diff:.2f} лв. — по-евтино в {matches[0]['store']}")


