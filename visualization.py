import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from datetime import datetime, timezone, timedelta
import pytz

def plot_data():
    df = pd.read_csv("data/iphone_prices.csv")
    
    # Convert the 'prices' column from string to list of floats
    df['prices'] = df['prices'].apply(ast.literal_eval)
    df = df.explode('prices')
    df['prices'] = df['prices'].astype(float)

    plt.figure(figsize=(12, 8))
    sns.boxplot(x="model", y="prices", data=df)
    plt.xticks(rotation=45, ha="right")
    plt.title("iPhone Price Distribution in Sri Lanka")
    plt.xlabel("iPhone Model")
    plt.ylabel("Price (LKR)")
    
    # Add current running time to the plot with Colombo, Sri Lanka time zone
    colombo_tz = pytz.timezone('Asia/Colombo')
    current_time = datetime.now(colombo_tz).strftime('%Y-%m-%d %H:%M:%S %z')
    plt.figtext(0.99, 0.01, f'Last update: {current_time}', horizontalalignment='right')
    
    plt.tight_layout()
    plt.savefig("data/iphone_price_distribution.png")
    # plt.show()

if __name__ == "__main__":
    plot_data()
    print("Plot saved as 'data/iphone_price_distribution.png'")
