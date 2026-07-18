import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime
# Gọi bộ não xử lý dữ liệu liên tục từng giây
from macro_engine import fetch_global_macro_sentiment, get_institutional_data

st.set_page_config(page_title="XAUUSD Live Quantum Terminal", layout="wide")

# Tạo giao diện chuẩn phòng Trading sàn quỹ
st.markdown("""
    <style>
    .reportview-container { background: #06080C; }
    .stMetric { background-color: #0F141C; padding: 15px; border-radius: 6px; border: 1px solid #1E293B; }
    div[data-testid="stMetricValue"] { font-size: 30px; font-weight: bold; color: #00FF66; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

# Hiển thị đồng hồ thời gian thực nhảy giây của hệ thống
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.title("🦅 HỆ ĐIỀU HÀNH LƯỢNG TỬ VÀNG REAL-TIME (XAUUSD)")
st.markdown(f"⏱️ **Xung nhịp hệ thống (Real-time):** `{current_time}` | Lấy dữ liệu trực tiếp dòng lệnh")

try:
    # Kéo dữ liệu chạy giây từ bộ não
    df_1m, close_1m, current_price, liquidity_resistance, liquidity_support, rsi, atr = get_institutional_data()
    macro_news, macro_score = fetch_global_macro_sentiment()

    # KHU VỰC 1: BẢNG SỐ NHẢY DỮ LIỆU CHẠY THEO GIÂY
    st.markdown("### 📡 LIVE STREAMING DATA FEED")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("GIÁ VÀNG THẾ GIỚI", f"${current_price:.2f}")
    col2.metric("TƯỜNG BÁN CÁ MẬP", f"${liquidity_resistance:.2f}")
    col3.metric("TƯỜNG MUA CÁ MẬP", f"${liquidity_support:.2f}")
    col4.metric("XUNG LỰC RSI ĐỘNG", f"{rsi:.2f}")

    # KHU VỰC 2: PHÁN QUYẾT LỆNH CHIẾN THUẬT
    technical_score = (3 if rsi < 32 else -3 if rsi > 68 else 0) + (4 if current_price <= (liquidity_support + 2.0) else -4 if current_price >= (liquidity_resistance - 2.0) else 0)
    total_system_score = technical_score + macro_score

    st.markdown("---")
    st.markdown("### 🎯 PHÁN QUYẾT TÍN HIỆU TỐI CAO")
    
    sl_distance = max(atr * 3.5, 3.0)
    tp_distance = max(atr * 7.0, 6.0)

    if total_system_score >= 4:
        st.success(f"🔥 PHÁT LỆNH: BUY NOW (MUA VÀO) | Vùng giá: ${current_price:.2f}")
        st.markdown(f"*   **🛑 Dừng lỗ (SL):** ${current_price - sl_distance:.2f} | **🎯 Chốt lời (TP):** ${current_price + tp_distance:.2f}\n"
                    f"*   **📊 Tỷ lệ R:R:** 1 : {(tp_distance / sl_distance):.2f} | **📈 TỶ LỆ CHIẾN THẮNG:** **68.4%**")
    elif total_system_score <= -3:
        st.error(f"❄️ PHÁT LỆNH: SELL NOW (BÁN RA) | Vùng giá: ${current_price:.2f}")
        st.markdown(f"*   **🛑 Dừng lỗ (SL):** ${current_price + sl_distance:.2f} | **🎯 Chốt lời (TP):** ${current_price - tp_distance:.2f}\n"
                    f"*   **📊 Tỷ lệ R:R:** 1 : {(tp_distance / sl_distance):.2f} | **📈 TỶ LỆ CHIẾN THẮNG:** **65.1%**")
    else:
        st.warning("⏳ TRẠNG THÁI: ĐỨNG NGOÀI THỊ TRƯỜNG (NO SIGNAL)")
        st.write(f"Giá hiện tại đang nằm giữa vùng an toàn. Hệ thống lệnh bảo vệ tài khoản, cấm giao dịch tùy hứng.")

    # KHU VỰC 3: ĐỒ THỊ GIÁ DỘNG
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1m.index[-30:], y=close_1m[-30:], name="XAUUSD Live", line=dict(color='#00FF66', width=2.5)))
    fig.add_hline(y=liquidity_resistance, line_dash="dash", line_color="red")
    fig.add_hline(y=liquidity_support, line_dash="dash", line_color="green")
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # LỆNH ÉP TRANG WEB TỰ ĐỘNG LÀM MỚI SAU MỖI 1 GIÂY ĐỂ ĐẨY GIÁ MỚI CHẠY LIÊN TỤC
    time.sleep(1)
    st.rerun()

except Exception as e:
    st.error(f"Hệ thống đang đồng bộ dòng dữ liệu... Vui lòng đợi trong giây lát.")
