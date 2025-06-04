# news_filter.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def is_market_news_positive(ticker):
    """
    Evalúa si las noticias recientes para el ticker son mayormente positivas.
    """
    if not FINNHUB_API_KEY:
        raise ValueError("API key de Finnhub no definida en el entorno.")

    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-12-01&to=2025-12-31&token={FINNHUB_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        noticias = response.json()

        positivas = 0
        negativas = 0

        for noticia in noticias:
            headline = noticia.get("headline", "").lower()
            summary = noticia.get("summary", "").lower()
            if any(p in headline or p in summary for p in ["beats", "record", "growth", "rises", "surge", "strong"]):
                positivas += 1
            elif any(n in headline or n in summary for n in ["falls", "misses", "drop", "warning", "lawsuit", "loss"]):
                negativas += 1

        return positivas >= negativas

    except Exception as e:
        print(f"❌ Error al analizar noticias de {ticker}: {e}")
        return False
