import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from utils import calculate_sma, calculate_ema

def fetch_data(symbol="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()

    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    return df

def main():
    df = fetch_data()
    df["SMA_5"] = calculate_sma(df["price"], 5)
    df["EMA_5"] = calculate_ema(df["price"], 5)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["price"], label="Preço")
    plt.plot(df.index, df["SMA_5"], label="SMA 5 dias")
    plt.plot(df.index, df["EMA_5"], label="EMA 5 dias")
    plt.title("Tendência de Preço - Bitcoin (USD)")
    plt.xlabel("Data")
    plt.ylabel("Preço (USD)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
