# market_conditions.py

import pytz
from datetime import datetime

def is_market_open():
    """
    Devuelve True si el mercado está abierto en horario de Nueva York (EST),
    entre las 9:30 AM y 4:00 PM.
    """
    ny_timezone = pytz.timezone("America/New_York")
    now_ny = datetime.now(ny_timezone)

    # Verifica día hábil (lunes a viernes)
    if now_ny.weekday() >= 5:
        return False

    # Verifica hora dentro del rango de mercado
    market_open = now_ny.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now_ny.replace(hour=16, minute=0, second=0, microsecond=0)

    return market_open <= now_ny <= market_close
