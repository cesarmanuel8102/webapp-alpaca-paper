
import datetime
import pytz
from indicators import get_indicators  # Debes implementar este módulo con RSI, MFI, MACD, etc.
from news_filter import is_market_news_positive  # Valida eventos desde fuentes confiables
from market_conditions import is_market_open, is_volatility_ok, is_post_event_day  # Filtros externos
from strategy_selector import choose_strategy  # Bull Put o Bear Call
from risk_control import should_exit_trade, compute_position_size  # Stop técnico y TP dinámico

# Parámetros del modelo
TRADING_WINDOW_START = datetime.time(hour=10, minute=30)
TRADING_WINDOW_END = datetime.time(hour=11, minute=15)
MAX_WEEKLY_OPERATIONS = 6
CAPITAL_USAGE_RATIO = 0.8
BASE_COST_PER_OPERATION = 250
STARTING_CAPITAL = 500

# Estado del modelo
capital = STARTING_CAPITAL
weekly_operations = 0
last_trade_result = "WIN"

def should_trade_now():
    now = datetime.datetime.now(pytz.timezone("US/Eastern")).time()
    return TRADING_WINDOW_START <= now <= TRADING_WINDOW_END

def can_open_trade():
    global weekly_operations, last_trade_result
    if weekly_operations >= MAX_WEEKLY_OPERATIONS:
        return False
    if last_trade_result == "LOSS":
        return False  # Enfriamiento si hubo pérdida previa
    return True

def model_main(ticker):
    global capital, weekly_operations, last_trade_result

    if not is_market_open():
        print("⛔ Mercado cerrado.")
        return
    if not should_trade_now():
        print("⏰ Fuera del horario óptimo.")
        return
    if not is_volatility_ok():
        print("⚠️ VIX demasiado alto.")
        return
    if is_post_event_day(ticker):
        print("📅 Día post-evento. No se opera.")
        return
    if not can_open_trade():
        print("📛 Límite de operaciones alcanzado o pérdida previa.")
        return
    if not is_market_news_positive(ticker):
        print("📰 Noticias negativas detectadas.")
        return

    indicators = get_indicators(ticker)
    if not indicators["valid"]:
        print("📉 Indicadores no alineados.")
        return

    strategy = choose_strategy(ticker, indicators)
    buying_power = check_buying_power()
    position_size = compute_position_size(capital, BASE_COST_PER_OPERATION, CAPITAL_USAGE_RATIO)

    if buying_power < position_size * BASE_COST_PER_OPERATION:
        print("❌ Sin fondos suficientes.")
        return

    success = place_trade(ticker, strategy, position_size)

    if success:
        weekly_operations += 1
        result = should_exit_trade(strategy)
        last_trade_result = "WIN" if result == "take_profit" else "LOSS" if result == "stop_loss" else last_trade_result
        capital += result["pnl"]
        print(f"✅ Trade ejecutado: {strategy['type']} | Resultado: {last_trade_result} | Capital: ${capital:.2f}")
    else:
        print("❌ Fallo al ejecutar la operación.")

if __name__ == "__main__":
    model_main("SPY")
