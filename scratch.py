import requests
from bs4 import BeautifulSoup
import re
import csv


def extract_numbers_to_csv(url, csv_filename):
    """
    从指定 URL 抓取网页后，提取页面内所有数字，并保存到 CSV 文件。
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.36"
        )
    }

    try:

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()


        soup = BeautifulSoup(response.text, 'html.parser')


        text_content = soup.get_text(separator=" ")


        numbers = re.findall(r"\d+", text_content)


        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["number"])
            for num in numbers:
                writer.writerow([num])

        print(f"已将页面内找到的所有数字共 {len(numbers)} 个，保存至 {csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


if __name__ == '__main__':
    target_url = "https://mod.gov.ua/en/news?tags=Combat"  # 示例链接
    csv_file = "../numbers.csv"
    extract_numbers_to_csv(target_url, csv_file)
