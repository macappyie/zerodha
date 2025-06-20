import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Zerodha 6-Month P&L", layout="wide")
st.title("📈 Zerodha 6-Month P&L Dashboard")

try:
    df = pd.read_csv("daily_pnl.csv", parse_dates=['date'])
    six_months_ago = datetime.now() - timedelta(days=180)
    df = df[df['date'] >= six_months_ago]
    df['color'] = df['net_pnl'].apply(lambda x: 'green' if x >= 0 else 'red')

    # 📊 Daily P&L
    st.subheader("🔁 Daily Net Profit & Loss")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'], y=df['net_pnl'],
        marker_color=df['color'],
        text=[f"₹{x:,.0f}" for x in df['net_pnl']],
        textposition="auto"
    ))
    fig.update_layout(
        height=400, plot_bgcolor='white',
        yaxis_title='Net P&L (₹)', xaxis_title='Date',
        margin=dict(l=20, r=20, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📈 Summary
    st.subheader("📌 Summary (Last 6 Months)")
    total = df['net_pnl'].sum()
    profit_days = df[df['net_pnl'] > 0].shape[0]
    loss_days = df[df['net_pnl'] < 0].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Profit Days", profit_days)
    col2.metric("🔴 Loss Days", loss_days)
    col3.metric("🧾 Net P&L", f"₹{total:,.0f}", delta="Profit" if total >= 0 else "Loss")

except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")

