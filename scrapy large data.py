import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json


BASE_URL = "https://mod.gov.ua"
START_URL = "https://mod.gov.ua/en/news?tags=Combat"

# Configure headers to mimic a browser


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
responses=requests.get(START_URL, headers=headers)


def fetch_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_subpage_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    # Adjust selector based on actual HTML (inspect the page)
    for item in soup.select('.news-list a.news-link'):  # Example: change to correct selector
        href = item.get('href')
        if href:
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)
    return links


def scrape_subpage(url):
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Extract title, date, and content (adjust selectors)
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "No title"
    date = soup.find('time').get_text(strip=True) if soup.find('time') else "No date"
    content = soup.find('div', class_='news-content').get_text(separator='\n', strip=True) if soup.find('div',
                                                                                                        class_='news-content') else "No content"

    return {
        "url": url,
        "title": title,
        "date": date,
        "content": content
    }


def get_next_page_url(html):
    """Finds the 'Next' page link if it exists."""
    soup = BeautifulSoup(html, 'html.parser')
    next_button = soup.find('a', class_='next')  # Adjust selector (e.g., 'a.next-page')
    if next_button and next_button.get('href'):
        return urljoin(BASE_URL, next_button['href'])
    return None


def scrape_all_pages(start_url, max_pages=10):
    all_subpage_links = []
    current_url = start_url
    page_count = 0

    while current_url and page_count < max_pages:
        print(f"Scraping page: {current_url}")
        html = fetch_page(current_url)
        if not html:
            break

        # Extract subpage links from current page
        subpage_links = extract_subpage_links(html)
        all_subpage_links.extend(subpage_links)

        # Find next page URL
        current_url = get_next_page_url(html)
        page_count += 1

        # Delay to avoid overwhelming the server
        time.sleep(2)  # Adjust as needed

    return all_subpage_links


# Step 1: Scrape ALL subpage links (with pagination)
all_subpage_links = scrape_all_pages(START_URL, max_pages=5)  # Limit to 5 pages for demo
print(f"Total subpages found: {len(all_subpage_links)}")

# Step 2: Scrape data from each subpage (with progress tracking)
all_data = []
for i, url in enumerate(all_subpage_links[:10]):  # Limit to 10 subpages for demo
    print(f"Scraping subpage {i + 1}/{len(all_subpage_links)}: {url}")
    data = scrape_subpage(url)
    if data:
        all_data.append(data)
    time.sleep(1)  # Be polite

# Save to JSON
with open('../mod_gov_ua_combat_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f"Data saved for {len(all_data)} subpages.")