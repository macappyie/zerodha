from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta
import os

API_KEY = "awh2j04pcd83zfvq"
ACCESS_TOKEN = "ZRhKTJpPt9SFCFmELIA0qJnL1pos2tFr"
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)





# === Fetch and Calculate Daily P&L ===
def fetch_daily_pnl():
    orders = kite.orders()
    df = pd.DataFrame(orders)

    # Filter completed trades only
    df = df[df['status'] == 'COMPLETE']
    df = df[df['transaction_type'].isin(['BUY', 'SELL'])]

    # Only last 6 months
    df['date'] = pd.to_datetime(df['exchange_timestamp']).dt.date
    six_months_ago = datetime.today().date() - timedelta(days=180)
    df = df[df['date'] >= six_months_ago]

    # Calculate P&L
    df['signed_pnl'] = df.apply(
        lambda row: -row['average_price'] * row['quantity'] if row['transaction_type'] == 'BUY'
        else row['average_price'] * row['quantity'], axis=1
    )

    pnl_by_day = df.groupby('date')['signed_pnl'].sum().reset_index()
    pnl_by_day.columns = ['date', 'net_pnl']
    pnl_by_day['date'] = pd.to_datetime(pnl_by_day['date'])

    return pnl_by_day

# === Save to CSV ===
def save_to_csv(new_data, filename="daily_pnl.csv"):
    if os.path.exists(filename):
        old_data = pd.read_csv(filename, parse_dates=['date'])
        combined = pd.concat([old_data, new_data]).drop_duplicates('date').sort_values('date')
    else:
        combined = new_data

    combined.to_csv(filename, index=False)
    print("✅ daily_pnl.csv updated")

# === Main ===
if __name__ == "__main__":
    try:
        df = fetch_daily_pnl()
        save_to_csv(df)
    except Exception as e:
        print(f"❌ Error fetching trades: {e}")
