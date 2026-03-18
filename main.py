from database.init_db import init_db
from site_scrapers.technomarket.technomarket_store_scraper import technomarket_store_scraper
from site_scrapers.technopolis.technopolis_store_scraper import technopolis_store_scraper

if __name__ == "__main__":
    init_db()
    # technopolis_store_scraper()
    technomarket_store_scraper()
