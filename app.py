import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Steven AI - Sniper", layout="wide")
st.title("🛡️ نظام Steven AI المتكامل")

# دالة لجلب البيانات بأمان ومنع الـ IndexError
def get_safe_data(symbol):
    try:
        # بنسحب بيانات أسبوع عشان نضمن وجود سعرين على الأقل
        data = yf.Ticker(symbol).history(period="1wk")
        if not data.empty and len(data) >= 2:
            price = data['Close'].iloc[-1]
            change = price - data['Close'].iloc[-2]
            return price, change
        return 0.0, 0.0
    except Exception as e:
        return 0.0, 0.0

# عرض الذهب والمؤشر
c1, c2 = st.columns(2)

gold_p, gold_c = get_safe_data("GC=F")
with c1:
    st.metric("الذهب العالمي", f"{gold_p:,.2f}", f"{gold_c:,.2f}")

egx30_p, egx30_c = get_safe_data("^EGX30")
with c2:
    st.metric("مؤشر EGX30", f"{egx30_p:,.2f}", f"{egx30_c:,.2f}")

st.success("✅ النظام شغال الآن! جرب تفتحه من موبايلك.")
