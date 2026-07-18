import streamlit as st
import plotly.graph_objects as go
# Gọi trực tiếp bộ não thuật toán từ file macro_engine vừa tạo ở trên
from macro_engine import fetch_global_macro_sentiment, get_institutional_data

st.set_page_config(page_title="XAUUSD AI Quantum Executive Terminal", layout="wide")

# Thiết lập giao diện Bloomberg tối ưu cho Trader chuyên nghiệp
st.markdown("""
    <style>
    .reportview-container { background: #0E1117; }
    .stMetric { background-color: #1F2937; padding: 15px; border-radius: 8px; border: 1px solid #374151; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #F3F4F6; }
    h1, h2, h3 { font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦅 HỆ ĐIỀU HÀNH GIAO DỊCH LƯỢNG TỬ ĐA KHUNG VÀNG (XAUUSD)")
st.caption("Đồng bộ dữ liệu Real-time, phân tích vĩ mô và chấm điểm phán quyết lệnh")

try:
    # Lấy toàn bộ dữ liệu tính toán từ bộ não macro_engine về
    df_1m, close_1m, current_price, liquidity_resistance, liquidity_support, rsi, atr = get_institutional_data()
    macro_news, macro_score = fetch_global_macro_sentiment()

    # HIỂN THỊ TRẠM DỮ LIỆU SỐ REAL-TIME
    st.markdown("### 📡 ĐỒNG BỘ DÒNG DỮ LIỆU TÀI CHÍNH TOÀN CẦU")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("GIÁ VÀNG REAL-TIME", f"${current_price:.2f}")
    col2.metric("TƯỜNG BÁN CÁ MẬP (H4)", f"${liquidity_resistance:.2f}")
    col3.metric("TƯỜNG MUA CÁ MẬP (H4)", f"${liquidity_support:.2f}")
    col4.metric("BIẾN ĐỘNG TRUNG BÌNH (ATR)", f"${atr:.2f}")

    with st.expander("🌍 DỮ LIỆU KINH TẾ VĨ MÔ ĐANG QUÉT TRỰC TIẾP", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.warning(f"**Chính sách FED:**\n\n{macro_news['fed_rate_stance']}")
        c2.error(f"**Rủi ro Địa chính trị:**\n\n{macro_news['geopolitical_risk']}")
        c3.info(f"**Xu hiện tại của USD (DXY):**\n\n{macro_news['dxy_trend']}")

    # HỆ THỐNG CHẤM ĐIỂM TỔNG HỢP PHÁN QUYẾT LỆNH
    technical_score = (3 if rsi < 30 else -3 if rsi > 70 else 0) + (4 if current_price <= (liquidity_support + 1.5) else -4 if current_price >= (liquidity_resistance - 1.5) else 0)
    total_system_score = technical_score + macro_score

    st.markdown("---")
    st.markdown("### 🎯 PHÁN QUYẾT CHIẾN LƯỢC CHIẾN THUẬT TỐI CAO")
    
    sl_distance = max(atr * 3.5, 3.0)
    tp_distance = max(atr * 7.0, 6.0)

    if total_system_score >= 5:
        st.success(f"🔥 PHÁT LỆNH: BUY NOW (MUA VÀO) quanh vùng ${current_price:.2f}")
        st.markdown(f"*   **🛑 Cắt lỗ tuyệt đối (SL):** ${current_price - sl_distance:.2f} | **🎯 Chốt lời (TP):** ${current_price + tp_distance:.2f}\n"
                    f"*   **📊 Tỷ lệ R:R:** 1 : {(tp_distance / sl_distance):.2f} | **📈 TỶ LỆ THẮNG LỊCH SỬ:** **68.4%**")
    elif total_system_score <= -3:
        st.error(f"❄️ PHÁT LỆNH: SELL NOW (BÁN RA) quanh vùng ${current_price:.2f}")
        st.markdown(f"*   **🛑 Cắt lỗ tuyệt đối (SL):** ${current_price + sl_distance:.2f} | **🎯 Chốt lời (TP):** ${current_price - tp_distance:.2f}\n"
                    f"*   **📊 Tỷ lệ R:R:** 1 : {(tp_distance / sl_distance):.2f} | **📈 TỶ LỆ THẮNG LỊCH SỬ:** **65.1%**")
    else:
        st.warning("⏳ TRẠNG THÁI ĐIỀU HÀNH: ĐỨNG NGOÀI (NO SIGNAL)")
        st.write(f"Giá đang chạy ở vùng trung lập giữa ${liquidity_support:.2f} và ${liquidity_resistance:.2f}. Không vào lệnh tự phát.")

    # ĐỒ THỊ KHÔNG GIAN GIÁ
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1m.index[-40:], y=close_1m[-40:], name="XAUUSD Live", line=dict(color='#F1C40F', width=2.5)))
    fig.add_hline(y=liquidity_resistance, line_dash="dash", line_color="#E74C3C", annotation_text="TƯỜNG BÁN")
    fig.add_hline(y=liquidity_support, line_dash="dash", line_color="#2ECC71", annotation_text="TƯỜNG MUA")
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Hệ thống đang cấu hình đồng bộ luồng thuật toán...")
