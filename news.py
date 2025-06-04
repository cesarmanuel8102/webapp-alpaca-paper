
import requests
import os

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "ck69h2aad3ifhtrf1h30")

def get_news(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-01-01&to=2024-12-31&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def filter_negative_news(news_list):
    negative_keywords = ["layoff", "fraud", "investigation", "collapse", "warning", "bankruptcy"]
    filtered = []
    for item in news_list:
        headline = item.get("headline", "").lower()
        if any(word in headline for word in negative_keywords):
            filtered.append(item)
    return filtered

def has_negative_news(ticker):
    news_list = get_news(ticker)
    return len(filter_negative_news(news_list)) > 0
