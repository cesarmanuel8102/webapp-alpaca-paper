
import pandas as pd
import numpy as np

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_mfi(data, period=14):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    money_flow = typical_price * data['volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(), 0)
    pos_mf = positive_flow.rolling(window=period).sum()
    neg_mf = negative_flow.rolling(window=period).sum()
    mfi = 100 - (100 / (1 + pos_mf / neg_mf))
    return mfi

def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = data['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(data, period=20, num_std=2):
    sma = data['close'].rolling(window=period).mean()
    std = data['close'].rolling(window=period).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return upper_band, lower_band

def calculate_adx(data, period=14):
    up_move = data['high'].diff()
    down_move = data['low'].diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr = pd.concat([
        data['high'] - data['low'],
        abs(data['high'] - data['close'].shift()),
        abs(data['low'] - data['close'].shift())
    ], axis=1).max(axis=1)
    tr_smooth = tr.rolling(window=period).mean()
    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / tr_smooth)
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / tr_smooth)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()
    return adx

def calculate_obv(data):
    obv = [0]
    for i in range(1, len(data)):
        if data['close'][i] > data['close'][i - 1]:
            obv.append(obv[-1] + data['volume'][i])
        elif data['close'][i] < data['close'][i - 1]:
            obv.append(obv[-1] - data['volume'][i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=data.index)

def calculate_ema(data, period=50):
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_avg_volume(data, period=20):
    return data['volume'].rolling(window=period).mean()
