import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Steven AI - Sniper", layout="wide")

st.title("🛡️ نظام Steven AI المتكامل")
st.write(f"📅 تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d | %H:%M')}")

# دالة لجلب البيانات بأمان ومنع الـ IndexError
def get_safe_data(symbol):
    try:
        data = yf.Ticker(symbol).history(period="5d")
        if not data.empty and len(data) >= 2:
            return data['Close'].iloc[-1], data['Close'].iloc[-1] - data['Close'].iloc[-2]
        return 0.0, 0.0
    except:
        return 0.0, 0.0

# شاشة الذهب والمؤشرات
st.subheader("💰 الذهب والمؤشرات العالمية")
cols = st.columns(3)

gold_p, gold_c = get_safe_data("GC=F")
with cols[0]:
    st.metric("الذهب (أونصة)", f"{gold_p:,.2f}", f"{gold_c:,.2f}")

egx_p, egx_c = get_safe_data("^EGX30")
with cols[1]:
    st.metric("مؤشر EGX30", f"{egx_p:,.2f}", f"{egx_c:,.2f}")

silver_p, silver_c = get_safe_data("SI=F")
with cols[2]:
    st.metric("الفضة", f"{silver_p:,.2f}", f"{silver_c:,.2f}")

st.divider()
st.success("✅ النظام شغال أونلاين وجاهز يا ستيفن!")
