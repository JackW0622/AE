import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time


def get_all_subpage_urls(main_url, max_pages=3):
    """Extracts all subpage URLs from the main page and paginated pages"""
    subpage_urls = []
    current_url = main_url
    page_count = 1

    while current_url and page_count < max_pages:
        print(f"Scraping page {page_count + 1}: {current_url}")

        # Fetch page with error handling
        try:
            response = requests.get(current_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract news links (UPDATE SELECTOR BASED ON ACTUAL WEBSITE STRUCTURE)
        news_items = soup.select('div.news-item a')  # Change to correct selector
        for item in news_items:
            href = item.get('href')
            if href and 'combat-losses' in href.lower():  # Filter for combat loss reports
                full_url = urljoin(main_url, href)
                subpage_urls.append(full_url)

        # Find next page link (UPDATE SELECTOR)
        next_page = soup.find('a', class_='next')  # Change to correct selector
        current_url = urljoin(main_url, next_page['href']) if next_page else None
        page_count += 1

        time.sleep(2)  # Respectful delay between requests

    print(f"Found {len(subpage_urls)} combat loss reports")
    return subpage_urls

def extract_daily_losses(url):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract date (adjust selector)
    date_element = soup.find('time')
    date = date_element['datetime'] if date_element else "Unknown Date"

    # Extract main content (focus on the loss data section)
    content = soup.find('div', class_='news-content').get_text()  # Adjust class

    # Structured data extraction using regex
    losses = {
        "date": date,
        "personnel": re.search(r'personnel[:\s]*([\d,]+)', content, re.IGNORECASE).group(1).replace(',',
                                                                                                    '') if re.search(
            r'personnel', content, re.IGNORECASE) else "N/A",
        "tanks": re.search(r'tanks[:\s]*([\d,]+)', content, re.IGNORECASE).group(1).replace(',', '') if re.search(
            r'tanks', content, re.IGNORECASE) else "N/A",
        "artillery": re.search(r'artillery[:\s]*([\d,]+)', content, re.IGNORECASE).group(1).replace(',',
                                                                                                    '') if re.search(
            r'artillery', content, re.IGNORECASE) else "N/A"
    }

    return losses

sample_url = "https://mod.gov.ua/en/news?tags=Combat"
def scrape_daily_reports(main_url, days_back=7):
    # Step 1: Get all subpage URLs from the main page (use pagination if needed)
    subpage_urls = get_all_subpage_urls(main_url)  # Implement this as in previous examples

    # Step 2: Process only the most recent 'days_back' reports
    losses_data = []
    for url in subpage_urls[:days_back]:
        data = extract_daily_losses(url)
        if data:
            losses_data.append(data)
        time.sleep(1)  # Be polite

    return losses_data


# Save to CSV
import pandas as pd

df = pd.DataFrame(scrape_daily_reports(sample_url, days_back=30))
df.to_csv('daily_losses.csv', index=False)