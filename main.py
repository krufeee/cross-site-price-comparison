from database.sqlite_db import init_db
from price_monitoring.technopolis_store_scraper import technopolis_store_scraper

if __name__ == "__main__":
    init_db()
    technopolis_store_scraper()
