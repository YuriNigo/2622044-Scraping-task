import csv
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

START_URL = "https://www.musashino-u.ac.jp/"
DOMAIN = urlparse(START_URL).netloc
MAX_PAGES = 100  # ★最大100件で自動終了するように設定

sitemap = {}
visited = set()
to_visit = [START_URL]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("スクレイピングを開始します（最大100件で終了します）...")

while to_visit and len(sitemap) < MAX_PAGES:
    current_url = to_visit.pop(0).split("#")[0]

    if current_url in visited or urlparse(current_url).netloc != DOMAIN:
        continue

    visited.add(current_url)

    try:
        time.sleep(1)  # 負荷軽減

        response = requests.get(current_url, headers=headers, timeout=10)

        # 文字化け防止対策
        response.encoding = response.apparent_encoding

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "No Title"

        sitemap[current_url] = title
        print(f"取得成功 [{len(sitemap)}/{MAX_PAGES}件]: {title}")

        for a_tag in soup.find_all("a", href=True):
            next_url = urljoin(current_url, a_tag["href"]).split("#")[0]
            if (
                urlparse(next_url).netloc == DOMAIN
                and next_url not in visited
                and next_url not in to_visit
            ):
                to_visit.append(next_url)

    except Exception as e:
        print(f"エラー ({current_url}): {e}")

# CSVファイルへ出力
csv_filename = "sitemap.csv"
with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])
    for url, title in sitemap.items():
        writer.writerow([url, title])

print(
    f"\n完了！ データを {csv_filename} に保存しました（合計: {len(sitemap)}件）。"
)