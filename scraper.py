import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs of e-commerce websites in Sri Lanka
URLS = [
    "https://appleasia.lk/product-category/iphone/"
]

URLS_IDEABEAM = [
    {"base_url": "https://www.ideabeam.com/mobile/brand/apple", "pages": 2}
]

def fetch_prices(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example parsing logic (customize based on website structure)
    items = soup.find_all("div", class_="product-grid-item")
    data = []

    for item in items:
        try:
            name_element = item.find("div", class_="product-element-bottom").find("h3", class_="wd-entities-title").find("a")
            name = name_element.text.strip()
            price_element = item.find("span", class_="price")
            print(name)
            if price_element:
                currency = price_element.find("span", class_="woocommerce-Price-currencySymbol").text.strip()
                price_values = [bdi.text.strip().replace("LKR", "").replace(",", "").strip() for bdi in price_element.find_all("bdi")]
                if "iphone" in name.lower():
                    print(name)
                    print(price_values)
                    data.append({"model": name, "currency": currency, "prices": price_values})
        except Exception as e:
            print(f"Error parsing item: {e}")
    print(f"Scraped {len(data)} items from {url}")
    return data

def fetch_prices_ideabeam(base_url, pages):
    headers = {"User-Agent": "Mozilla/5.0"}
    all_data = []

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("div", class_="product_box")
        data = []

        for item in items:
            try:
                name_element = item.find("span", itemprop="name")
                name = name_element.text.strip()
                price_element = item.find("meta", itemprop="price")
                if price_element:
                    price = price_element["content"]
                    currency = item.find("meta", itemprop="priceCurrency")["content"]
                    if "iphone" in name.lower():
                        data.append({"model": name, "currency": currency, "price": price})
            except Exception as e:
                print(f"Error parsing item: {e}")
        print(f"Scraped {len(data)} items from {url}")
        all_data.extend(data)

    return all_data

def scrape_all():
    all_data = []
    for url in URLS:
        data = fetch_prices(url)
        print(f"Scraped {len(data)} items from {url}")
        if data:
            all_data.extend(data)
    print(f"Total items scraped: {len(all_data)}")
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("data/iphone_prices.csv", index=False)
        print("Data scraped and saved to iphone_prices.csv")
    else:
        print("No data scraped.")

    for url_info in URLS_IDEABEAM:
        ideabeam_data = fetch_prices_ideabeam(url_info["base_url"], url_info["pages"])
        if ideabeam_data:
            df_ideabeam = pd.DataFrame(ideabeam_data)
            df_ideabeam.to_csv("data/iphone_prices_ideabeam.csv", index=False)
            print(f"Data scraped and saved to iphone_prices_ideabeam.csv from {url_info['base_url']}")
        else:
            print(f"No data scraped from {url_info['base_url']}.")

if __name__ == "__main__":
    scrape_all()