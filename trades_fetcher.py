from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta
import os

API_KEY = "awh2j04pcd83zfvq"
ACCESS_TOKEN = "ZRhKTJpPt9SFCFmELIA0qJnL1pos2tFr"
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)




def fetch_trades():
    trades = kite.trades()
    df = pd.DataFrame(trades)

    df['date'] = pd.to_datetime(df['exchange_timestamp']).dt.date
    df['pnl'] = df.apply(lambda row: row['quantity'] * row['average_price']
                         if row['transaction_type'] == 'SELL'
                         else -row['quantity'] * row['average_price'], axis=1)

    pnl_daily = df.groupby('date')['pnl'].sum().reset_index()
    pnl_daily.columns = ['date', 'net_pnl']
    pnl_daily['date'] = pd.to_datetime(pnl_daily['date'])

    return pnl_daily

def save_to_csv(new_data, filename="daily_pnl.csv"):
    if os.path.exists(filename):
        old_data = pd.read_csv(filename, parse_dates=['date'])
        combined = pd.concat([old_data, new_data]).drop_duplicates('date').sort_values('date')
    else:
        combined = new_data

    combined.to_csv(filename, index=False)

# Run fetch
if __name__ == "__main__":
    df = fetch_trades()
    save_to_csv(df)
    print("✅ Trades saved to daily_pnl.csv")


