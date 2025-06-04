
import yfinance as yf
import pandas as pd
import numpy as np

def get_indicators(ticker):
    df = yf.download(ticker, period="90d", interval="1d")

    if df.empty:
        return {}

    df.dropna(inplace=True)

    # RSI
    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi

    # MFI
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    money_flow = typical_price * df["Volume"]
    positive_flow = []
    negative_flow = []

    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i - 1]:
            positive_flow.append(money_flow[i])
            negative_flow.append(0)
        else:
            positive_flow.append(0)
            negative_flow.append(money_flow[i])

    positive_mf = pd.Series(positive_flow).rolling(window=14).sum()
    negative_mf = pd.Series(negative_flow).rolling(window=14).sum()
    mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
    df["MFI"] = mfi

    # MACD
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal_MACD"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    df["BB_Middle"] = df["Close"].rolling(window=20).mean()
    df["BB_StdDev"] = df["Close"].rolling(window=20).std()
    df["BB_Upper"] = df["BB_Middle"] + 2 * df["BB_StdDev"]
    df["BB_Lower"] = df["BB_Middle"] - 2 * df["BB_StdDev"]

    # ADX
    df["TR"] = np.maximum(df["High"] - df["Low"], 
                          np.maximum(abs(df["High"] - df["Close"].shift()), 
                                     abs(df["Low"] - df["Close"].shift())))
    df["+DM"] = np.where((df["High"] - df["High"].shift()) > (df["Low"].shift() - df["Low"]), 
                         np.maximum(df["High"] - df["High"].shift(), 0), 0)
    df["-DM"] = np.where((df["Low"].shift() - df["Low"]) > (df["High"] - df["High"].shift()), 
                         np.maximum(df["Low"].shift() - df["Low"], 0), 0)
    tr14 = df["TR"].rolling(14).sum()
    plus_dm14 = df["+DM"].rolling(14).sum()
    minus_dm14 = df["-DM"].rolling(14).sum()
    plus_di14 = 100 * (plus_dm14 / tr14)
    minus_di14 = 100 * (minus_dm14 / tr14)
    dx = 100 * (abs(plus_di14 - minus_di14) / (plus_di14 + minus_di14))
    adx = dx.rolling(14).mean()
    df["ADX"] = adx

    # OBV
    obv = [0]
    for i in range(1, len(df["Close"])):
        if df["Close"][i] > df["Close"][i - 1]:
            obv.append(obv[-1] + df["Volume"][i])
        elif df["Close"][i] < df["Close"][i - 1]:
            obv.append(obv[-1] - df["Volume"][i])
        else:
            obv.append(obv[-1])
    df["OBV"] = obv

    # EMA 50
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()

    # Volumen promedio 20 días
    df["Vol_Prom_20"] = df["Volume"].rolling(window=20).mean()

    # Filtro técnico de reversión
    df["Reversion_Filter"] = ((df["RSI"] < 30) & (df["MACD"] < df["Signal_MACD"]) & (df["Close"] < df["BB_Lower"]))

    latest = df.iloc[-1]
    indicadores = {
        "RSI": round(latest["RSI"], 2),
        "MFI": round(latest["MFI"], 2),
        "MACD": round(latest["MACD"], 4),
        "MACD_Signal": round(latest["Signal_MACD"], 4),
        "BB_Upper": round(latest["BB_Upper"], 2),
        "BB_Lower": round(latest["BB_Lower"], 2),
        "ADX": round(latest["ADX"], 2),
        "OBV": round(latest["OBV"], 2),
        "EMA_50": round(latest["EMA_50"], 2),
        "Volumen_Prom_20": round(latest["Vol_Prom_20"], 2),
        "Filtro_Reversion": bool(latest["Reversion_Filter"])
    }

    return indicadores
