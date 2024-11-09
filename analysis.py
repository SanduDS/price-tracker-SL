import pandas as pd
import os
import ast

def analyze_data():
    data_dir = "data"
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    all_data = []

    for file in files:
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)

        # Handle 'prices' column if present
        if 'prices' in df.columns:
            df['prices'] = df['prices'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            df = df.explode('prices')
            df['prices'] = df['prices'].astype(float)
            df.rename(columns={'prices': 'price'}, inplace=True)

        all_data.append(df)

    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)

    # Basic statistics
    print("Basic Statistics for combined data:")
    print(combined_data.describe())

    # Price range analysis
    price_range = combined_data.groupby("model")["price"].agg(["min", "max", "mean"])
    print("\nPrice Range by Model for combined data:")
    print(price_range)

    # Save analysis results
    price_range.to_csv("data/combined_price_analysis.csv")
    print("\nAnalysis saved to combined_price_analysis.csv")

if __name__ == "__main__":
    analyze_data()
