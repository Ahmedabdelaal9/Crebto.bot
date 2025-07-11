import streamlit as st
import ccxt
import pandas as pd
import ta

st.set_page_config(page_title="Crypto Signal App", layout="centered")
st.title("📈 تطبيق الإشارات الذكي الخاص بك")
st.subheader("تحليل عملات رقمية باستخدام EMA + RSI + Volume")

# إعداد Binance
exchange = ccxt.binance()

# اختيار العملة
symbol = st.selectbox("اختر عملة:", ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT"])

# تحميل البيانات
with st.spinner("جارٍ تحميل البيانات..."):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=100)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

# حساب المؤشرات
df["ema10"] = ta.trend.ema_indicator(df["close"], window=10).ema_indicator()
df["ema20"] = ta.trend.ema_indicator(df["close"], window=20).ema_indicator()
df["ema50"] = ta.trend.ema_indicator(df["close"], window=50).ema_indicator()
df["rsi"] = ta.momentum.rsi(df["close"], window=14)

# إشارات التداول
last = df.iloc[-1]
vol_avg = df["volume"].rolling(20).mean().iloc[-1]

if last["ema10"] > last["ema20"] > last["ema50"] and last["rsi"] > 50 and last["volume"] > vol_avg:
    st.success("✅ إشارة شراء متاحة!")
else:
    st.warning("❌ لا توجد إشارة حاليًا.")

# عرض بيانات تفصيلية
with st.expander("عرض بيانات المؤشرات"):
    st.dataframe(df.tail(10))
