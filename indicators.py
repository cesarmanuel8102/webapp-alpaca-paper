
import yfinance as yf
import pandas as pd
import numpy as np

def calcular_todos_los_indicadores(ticker):
    df = yf.download(ticker, period='3mo', interval='1d')
    df.dropna(inplace=True)

    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MFI
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    money_flow = typical_price * df['Volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    positive_mf = positive_flow.rolling(window=14).sum()
    negative_mf = negative_flow.rolling(window=14).sum()
    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
    df['MFI'] = mfi

    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    sma20 = df['Close'].rolling(window=20).mean()
    std20 = df['Close'].rolling(window=20).std()
    df['UpperBB'] = sma20 + (std20 * 2)
    df['LowerBB'] = sma20 - (std20 * 2)

    # ADX
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                  np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
    df['+DM'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), 
                         np.maximum(df['High'] - df['High'].shift(1), 0), 0)
    df['-DM'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), 
                         np.maximum(df['Low'].shift(1) - df['Low'], 0), 0)
    tr14 = df['TR'].rolling(window=14).sum()
    plus_dm14 = df['+DM'].rolling(window=14).sum()
    minus_dm14 = df['-DM'].rolling(window=14).sum()
    plus_di14 = 100 * (plus_dm14 / tr14)
    minus_di14 = 100 * (minus_dm14 / tr14)
    dx = 100 * abs(plus_di14 - minus_di14) / (plus_di14 + minus_di14)
    df['ADX'] = dx.rolling(window=14).mean()

    # OBV
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'][i] > df['Close'][i-1]:
            obv.append(obv[-1] + df['Volume'][i])
        elif df['Close'][i] < df['Close'][i-1]:
            obv.append(obv[-1] - df['Volume'][i])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv

    # EMA 50
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # Volumen promedio 20 días
    df['Vol_20d'] = df['Volume'].rolling(window=20).mean()

    return df.iloc[-1]  # Última fila con todos los indicadores

def get_indicators(ticker):
    return calcular_todos_los_indicadores(ticker)
