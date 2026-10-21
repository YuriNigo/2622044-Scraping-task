import requests
from bs4 import BeautifulSoup

# 対象のURL
url = "http://abehiroshi.la.coocan.jp/movie/eiga.htm"

# ページを取得
response = requests.get(url)
response.encoding = response.apparent_encoding  # 文字化け防止

# HTMLの解析
soup = BeautifulSoup(response.text, "html.parser")

# 映画タイトルの要素を取得して表示
print("--- 出演映画一覧 ---")
for tag in soup.find_all(["td", "li", "p"]):
    text = tag.get_text(strip=True)
    if text:
        print(text)