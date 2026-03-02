import pandas as pd

def export_categories_to_csv(categories):
    df = pd.DataFrame(categories)
    df = df.drop_duplicates(subset=["link"])
    df.to_csv("../../database/categories_technomarket.csv", index=False, encoding="utf-8-sig")

