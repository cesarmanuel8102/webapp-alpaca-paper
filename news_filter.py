
import requests
import os
from datetime import datetime, timedelta

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

def filtrar_noticias(ticker, dias=3, impacto_clave=['downgrade', 'recall', 'miss', 'fraud']):
    if not FINNHUB_API_KEY:
        raise ValueError("La clave de API de Finnhub no está configurada en el entorno.")

    hoy = datetime.utcnow().date()
    inicio = hoy - timedelta(days=dias)

    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={inicio}&to={hoy}&token={FINNHUB_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    noticias = response.json()
    relevantes = []

    for noticia in noticias:
        titulo = noticia.get('headline', '').lower()
        if any(palabra in titulo for palabra in impacto_clave):
            relevantes.append({
                'titulo': noticia.get('headline'),
                'fecha': noticia.get('datetime'),
                'fuente': noticia.get('source'),
                'url': noticia.get('url')
            })

    return relevantes
