
from config import searched_products, THRESHOLD
from database.queries import get_last_price_for_products
from utils.matching import get_score

results = {}
all_products = get_last_price_for_products()

for search_term in searched_products:
    matches = []

    for product in all_products:

        score = get_score(search_term, product)

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


