import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings

# Reuse the standalone scraper by importing relative path
# or, simplest: execute the script file
SCRIPT_PATH = os.path.join(os.path.dirname(settings.BASE_DIR), "scripts", "scrape_ibps.py")
DATA_DIR = os.path.join(os.path.dirname(settings.BASE_DIR), "data")
CSV_PATH = os.path.join(DATA_DIR, "ibps_jobs.csv")

class Command(BaseCommand):
    help = "Scrape IBPS public notices into data/ibps_jobs.csv"

    def handle(self, *args, **options):
        # Execute the standalone script so both entrypoints behave the same
        os.system(f'python "{SCRIPT_PATH}"')

        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            self.stdout.write(self.style.SUCCESS(f"Scraped {len(df)} rows → {CSV_PATH}"))
        else:
            self.stdout.write(self.style.WARNING("CSV not found; scraper may have failed."))
