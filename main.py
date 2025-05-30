import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import pytz
from utils import calculate_sma, calculate_ema

def fetch_data(symbol="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": "brl",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()

    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms').dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
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
    plt.title("Tendência de Preço - Bitcoin (BRL)")
    plt.xlabel("Data")
    plt.ylabel("Preço (BRL)")
    plt.legend()
    plt.grid()
    
    # Format x-axis dates to dd/MM/yyyy
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m/%Y'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    # Format y-axis to R$ format
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, p: f'R$ {x:,.2f}'.replace(',', '.')))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
