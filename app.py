import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Steven AI - Elite Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stMetric { background-color: #ffffff; border-radius: 12px; border-left: 5px solid #ffc107; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    th { background-color: #1a1a1a !important; color: #ffc107 !important; text-align: center !important; }
    td { text-align: center !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ نظام Steven AI: المحلل المالي المتكامل")
st.write(f"📅 تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d | %H:%M')}")

# 2. شاشة الملاذات الآمنة (مع تصليح عطل الـ IndexError)
st.subheader("💰 الذهب، الفضة، والمؤشرات")
m_cols = st.columns(4)
global_assets = {"الذهب": "GC=F", "الفضة": "SI=F", "EGX30": "^EGX30", "EGX70": "^EGX70"}

for i, (name, sym) in enumerate(global_assets.items()):
    with m_cols[i]:
        # سحب بيانات 5 أيام لضمان وجود نقاط كافية للـ iloc[-2]
        asset_data = yf.Ticker(sym).history(period="5d")
        
        # التأكد إن البيانات مش فاضية وفيها على الأقل نقطتين
        if not asset_data.empty and len(asset_data) >= 2:
            curr_p = asset_data['Close'].iloc[-1]
            prev_p = asset_data['Close'].iloc[-2]
            change = curr_p - prev_p
            st.metric(name, f"{curr_p:,.2f}", f"{change:,.2f}")
        else:
            st.warning(f"جاري انتظار بيانات {name}...")

st.divider()

# 3. قائمة الـ 80 سهم (تعمل بنفس نظام الحماية)
egypt_stocks = {
    "CIB": "COMI.CA", "طلعت مصطفى": "TMGH.CA", "بلتون": "BTEL.CA", "فوري": "FWRY.CA", "إي فاينانس": "EFIH.CA",
    "السويدي": "SWDY.CA", "حديد عز": "ESRS.CA", "هرماس": "HRHO.CA", "أبوقير": "ABUK.CA", "موبكو": "MFPC.CA",
    "المصرية للاتصالات": "ETEL.CA", "سيدي كرير": "SKPC.CA", "أموك": "AMOC.CA", "بالم هيلز": "PHDC.CA", "مدينة نصر": "MNHD.CA",
    "مصر الجديدة": "HELI.CA", "إعمار": "EMFD.CA", "القلعة": "CCAP.CA", "جهينة": "JUFO.CA", "إيديتا": "EFID.CA",
    "دومتي": "DOMT.CA", "عبور لاند": "OLFI.CA", "النساجون": "ORWE.CA", "جي بي أوتو": "AUTO.CA", "كيما": "KIMA.CA",
    "إسكندرية للحاويات": "ALCN.CA", "بايونيرز": "PPRP.CA", "أوراسكوم للتنمية": "ORHD.CA", "دايس": "DSCW.CA",
    "الشرقية للدخان": "EAST.CA", "الدلتا للسكر": "SUGR.CA", "قناة السويس": "CANA.CA", "مصر للألومنيوم": "EALU.CA"
}

def analyze_stock_full(name, symbol):
    try:
        data = yf.Ticker(symbol).history(period="6mo")
        # حماية: لو البيانات أقل من 30 يوم نرفض التحليل عشان المؤشرات تكون دقيقة
        if data.empty or len(data) < 30: return None
        
        data.ta.rsi(append=True)
        data.ta.macd(append=True)
        data.ta.adx(append=True)
        
        last = data.iloc[-1]
        prev = data.iloc[-2]
        
        high_20 = data['High'].tail(20).max()
        low_20 = data['Low'].tail(20).min()
        close_p = last['Close']
        
        pivot = (high_20 + low_20 + close_p) / 3
        res1 = (2 * pivot) - low_20
        sup1 = (2 * pivot) - high_20
        stop_loss = sup1 * 0.98
        
        score = 0
        if last['RSI_14'] < 40: score += 30
        if last['MACD_12_26_9'] > last['MACDs_12_26_9']: score += 30
        if last['ADX_14'] > 20: score += 20
        if close_p > prev['Close']: score += 20
        
        if score >= 70: rec = "🔥 شراء قوي"
        elif 40 <= score < 70: rec = "🔍 مراقبة"
        elif last['RSI_14'] > 75: rec = "⚠️ خروج/بيع"
        else: rec = "⚖️ محايد"
        
        return {
            "السهم": name, "السعر الحالي": round(close_p, 2), "الدعم (Entry)": round(sup1, 2),
            "المقاومة (Target)": round(res1, 2), "وقف الخسارة (SL)": round(stop_loss, 2),
            "ثقة ستيفن": f"{score}%", "القرار": rec
        }
    except: return None

if st.button('🚀 تشغيل الماسح الضوئي لـ 80 سهم'):
    with st.spinner('ستيفن يحلل البيانات...'):
        all_results = [analyze_stock_full(n, s) for n, s in egypt_stocks.items()]
        results = [r for r in all_results if r is not None]
        if results:
            df = pd.DataFrame(results).sort_values(by="ثقة ستيفن", ascending=False)
            st.table(df)

st.divider()

# 4. الفحص الفردي (الرسم البياني + الأخبار)
target = st.selectbox("اختر السهم لتحليله بدقة:", list(egypt_stocks.keys()))
if target:
    stock_obj = yf.Ticker(egypt_stocks[target])
    hist = stock_obj.history(period="3mo")
    if not hist.empty:
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(template="plotly_white", height=500, title=f"تحليل {target}")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown(f"### 📰 أخبار {target}")
            news = stock_obj.news
            if news:
                for item in news[:5]:
                    st.markdown(f"🔗 *[{item['title']}]({item['link']})*")
                    st.divider()