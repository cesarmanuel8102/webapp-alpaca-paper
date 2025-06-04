
import pandas as pd

def is_bullish_market(rsi, ema, macd):
    return rsi > 50 and ema > 0 and macd > 0

def is_bearish_market(rsi, ema, macd):
    return rsi < 50 and ema < 0 and macd < 0

def get_market_trend_signal(data):
    try:
        if 'EMA_50' in data.columns and 'RSI' in data.columns and 'MACD' in data.columns:
            ema = data['EMA_50'].iloc[-1] - data['EMA_50'].mean()
            rsi = data['RSI'].iloc[-1]
            macd = data['MACD'].iloc[-1]
            if is_bullish_market(rsi, ema, macd):
                return 'bullish'
            elif is_bearish_market(rsi, ema, macd):
                return 'bearish'
        return 'neutral'
    except Exception as e:
        print(f"[market_conditions] Error evaluating trend: {e}")
        return 'neutral'
