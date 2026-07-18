import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(page_title="XAUUSD AI Quantum Terminal", layout="wide")
st.title("🦅 HỆ THỐNG ĐIỀU HÀNH KỸ THUẬT QUANTUM XAUUSD")

@st.cache_data(ttl=5)
def get_advanced_data():
    df = yf.download(tickers="GC=F", period="5d", interval="1m")
    return df

try:
    df = get_advanced_data()
    # Tính toán toán học nâng cao trực tiếp trên mảng để tối ưu tốc độ dòng lệnh
    close = df['Close'].values.flatten()
    high = df['High'].values.flatten()
    low = df['Low'].values.flatten()
    current_price = float(close[-1])

    # 1. TÍNH TOÁN HỆ THỐNG CHỈ BÁO NÂNG CAO (MA Chéo, Bollinger Bands, MACD)
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['STD20'] = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['MA20'] + (df['STD20'] * 2)
    df['BB_lower'] = df['MA20'] - (df['STD20'] * 2)
    
    # Tính toán MACD thô
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Lấy các giá trị real-time mới nhất
    ma5 = float(df['MA5'].iloc[-1])
    ma20 = float(df['MA20'].iloc[-1])
    upper_bb = float(df['BB_upper'].iloc[-1])
    lower_bb = float(df['BB_lower'].iloc[-1])
    macd = float(df['MACD'].iloc[-1])
    signal = float(df['Signal_Line'].iloc[-1])

    # 2. ENGINE QUYẾT ĐỊNH LỆNH PHỨC HỢP (Multi-Indicator Scoring)
    # Chấm điểm dựa trên sự đồng thuận của nhiều chỉ báo tài chính
    buy_signals = 0
    sell_signals = 0

    if ma5 > ma20: buy_signals += 1 
    else: sell_signals += 1

    if current_price <= lower_bb: buy_signals += 2
    if current_price >= upper_bb: sell_signals += 2

    if macd > signal: buy_signals += 1
    else: sell_signals += 1

    # 3. GIAO DIỆN PHÂN TÍCH CHUYÊN SÂU
    st.markdown("### 📊 MA TRẬN DỮ LIỆU ĐA CHỈ BÁO")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("GIÁ HIỆN TẠI", f"${current_price:.2f}")
    c2.metric("DẢI TRÊN BB (CẢN ĐỈNH)", f"${upper_bb:.2f}")
    c3.metric("DẢI DƯỚI BB (CẢN ĐÁY)", f"${lower_bb:.2f}")
    c4.metric("XUNG LỰC MACD", f"{macd:.4f}", delta="Cắt lên (Tăng)" if macd > signal else "Cắt xuống (Giảm)")

    st.markdown("---")
    st.markdown("### 🎯 KẾT LUẬN CHIẾN LƯỢC TỐI CAO")

    # Đưa ra phán quyết dựa trên tổng điểm hệ thống
    if buy_signals >= 3:
        st.markdown("<h2 style='color: #2ECC71;'>🔥 KHUYẾN NGHỊ: BUY (MUA)</h2>", unsafe_allow_html=True)
        st.write(f"**📍 Điểm vào lệnh:** ${current_price:.2f} | **🛑 Cắt lỗ (SL):** ${current_price - 3.0:.2f} | **🎯 Chốt lời (TP):** ${upper_bb:.2f}")
        st.info(f"**🧠 Lý do hệ thống:** Sự đồng thuận từ {buy_signals} chỉ báo kỹ thuật dòng tiền. Giá chạm dải dưới Bollinger Bands kết hợp MACD hướng lên, xác suất đảo chiều tăng rất cao.")
    elif sell_signals >= 3:
        st.markdown("<h2 style='color: #E74C3C;'>❄️ KHUYẾN NGHỊ: SELL (BÁN)</h2>", unsafe_allow_html=True)
        st.write(f"**📍 Điểm vào lệnh:** ${current_price:.2f} | **🛑 Cắt lỗ (SL):** ${current_price + 3.0:.2f} | **🎯 Chốt lời (TP):** ${lower_bb:.2f}")
        st.info(f"**🧠 Lý do hệ thống:** Sự đồng thuận từ {sell_signals} chỉ báo kỹ thuật dòng tiền. Giá húc vào dải trên Bollinger Bands và quá tải lực mua, ưu tiên kích hoạt lệnh BÁN.")
    else:
        st.markdown("<h2 style='color: #F1C40F;'>⏳ TRẠNG THÁI: THEO DÕI (NO SIGNAL)</h2>", unsafe_allow_html=True)
        st.warning("Các chỉ báo kỹ thuật đang triệt tiêu lẫn nhau (Xung đột xu hướng). Thị trường rủi ro cao, hệ thống khuyến nghị không vào lệnh.")

    # 4. ĐỒ THỊ ĐA TẦNG CHUYÊN NGHIỆP
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index[-60:], y=close[-60:], name="XAUUSD Real-time", line=dict(color='#F1C40F', width=2)))
    fig.add_trace(go.Scatter(x=df.index[-60:], y=df['BB_upper'].iloc[-60:], name="BB Upper", line=dict(color='red', width=1, dash='dash')))
    fig.add_trace(go.Scatter(x=df.index[-60:], y=df['BB_lower'].iloc[-60:], name="BB Lower", line=dict(color='green', width=1, dash='dash')))
    fig.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Đang kết nối luồng thuật toán Quantum...")
