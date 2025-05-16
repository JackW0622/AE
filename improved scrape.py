import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import re

main_url = "https://mod.gov.ua/en/news?tags=Combat"

def get_casualties_number (main_url, max_pages = 12):
    current_page = 1
    current_url = main_url

    while current_page <= max_pages:
        print(f"Scraping page {current_page + 1}: {current_url}")

        try:
            response = requests.get(current_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
            break


def