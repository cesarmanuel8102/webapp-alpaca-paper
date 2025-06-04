import requests
import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def is_market_news_positive(ticker):
    """
    Analiza las noticias recientes para un ticker y devuelve True si el sentimiento general es positivo o neutral,
    y False si es mayoritariamente negativo.
    """
    try:
        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        news = response.json()

        # Filtrar por el ticker
        filtered = [item for item in news if ticker.upper() in item.get("headline", "") or ticker.upper() in item.get("summary", "")]

        # Análisis básico: contar negativos
        negative_keywords = ["fall", "plunge", "lawsuit", "crash", "loss", "drop", "slump", "fraud", "warning", "negative", "bad"]
        negative_count = 0

        for item in filtered:
            content = (item.get("headline", "") + " " + item.get("summary", "")).lower()
            if any(word in content for word in negative_keywords):
                negative_count += 1

        if len(filtered) == 0:
            return True  # Si no hay noticias, se asume neutral/positivo

        return (negative_count / len(filtered)) < 0.5

    except Exception as e:
        print(f"Error analizando noticias: {e}")
        return True  # En caso de error, se asume neutral para no bloquear operaciones
