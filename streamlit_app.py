import streamlit as st
from macro_engine import evaluate_d1_quantum_signal

# 1. CẤU HÌNH TRANG WEB TOÀN CỤC
st.set_page_config(page_title="XAUUSD D1 Macro Executive Terminal", layout="wide")

# 2. BỘ MÃ HÓA CSS NỀN TRẮNG CHỮ ĐEN ĐẬM CHỐNG MỜ TUYỆT ĐỐI
st.markdown("""
    <style>
    .stApp, html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #FFFFFF !important; 
    }
    h1, h2, h3, h4, h5, h6, p, .stMarkdown, li, span, div, label { 
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"], .stSelectbox div, input, [data-testid="stNumberInput"] div {
        background-color: #F3F4F6 !important; 
        border: 2px solid #000000 !important; 
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] *, div[role="listbox"] *, .stSelectbox div, input, span[data-baseweb="select"], div[role="option"] * {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 16px !important;
    }
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #1E8449 !important; 
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"], button[data-testid="stBaseButton-secondary"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        border-radius: 8px !important;
    }
    ul[role="listbox"] li * { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TIÊU ĐỀ TRẠM ĐIỀU HÀNH
st.title("🏛️ TRẠM ĐIỀU HÀNH THẨM ĐỊNH LƯỢNG TỬ KHUNG NGÀY D1 (XAUUSD)")
st.caption("Hệ thống ma trận phân tích kết hợp sâu sắc giữa Chính sách Vĩ mô toàn cầu và Phân tích Kỹ thuật")
st.markdown("---")

# 4. KHU VỰC NHẬP DỮ LIỆU ĐÓNG NẾN NGÀY D1
st.markdown("### 📥 BẢNG NẠP THAM SỐ VĨ MÔ & KỸ THUẬT (QUAN SÁT LÚC 4H-5H SÁNG MỖI NGÀY)")
col1, col2 = st.columns(2)

with col1:
    user_fed = st.selectbox("1. Định hướng chính sách tiền tệ dài hạn của FED:", ["Nới lỏng (Cắt giảm lãi suất / Bơm tiền / USD suy yếu)", "Thắt chặt (Tăng lãi suất / Giữ lãi suất cao / USD mạnh)", "Trung lập (FED chờ đợi thêm số liệu lạm phát)"])
    user_macro = st.selectbox("2. Bối cảnh tin tức Vĩ mô / Địa chính trị trong ngày:", ["Tốt cho Vàng (USD yếu, Địa chính trị căng thẳng)", "Xấu cho Vàng (USD mạnh, Diều hâu, Hòa hoãn)", "Tin trung lập, không có biến động mạnh"])
    user_rsi = st.number_input("3. Chỉ số RSI trên khung D1 hiện tại (0 - 100):", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

with col2:
    user_trend = st.selectbox("4. Cấu trúc xu hướng kỹ thuật chủ đạo trên khung D1:", ["Xu hướng Tăng dài hạn (Bullish)", "Xu hướng Giảm dài hạn (Bearish)", "Xu hướng Đi ngang / Không rõ ràng (Sideway)"])
    user_liquidity = st.selectbox("5. Vị trí giá D1 so với vùng Cản khối lệnh Cá Mập (D1/W1):", ["Chạm Vùng Hỗ trợ D1 / Order Block Tăng tuần", "Chạm Vùng Kháng cự D1 / Order Block Giảm tuần", "Nằm lơ lửng giữa các vùng cản lớn"])
    user_price_action = st.selectbox("6. Tín hiệu đóng nến Ngày D1 vừa qua (Price Action):", ["Nến D1 Đảo chiều Tăng mạnh (Pinbar rút râu dài / Engulfing xanh ôm trọn)", "Nến D1 Đảo chiều Giảm mạnh (Pinbar từ chối đỉnh / Engulfing đỏ nuốt chửng)", "Nến Doji / Nến thân nhỏ biến động hẹp"])

st.markdown("---")

# 5. KHU VỰC PHÁN QUYẾT CHIẾN LƯỢC TỐI CAO
st.markdown("### 🎯 KẾT LUẬN CHIẾN LƯỢC TOÀN CỤC")

if st.button("🚀 KÍCH HOẠT HỆ THỐNG THẨM ĐỊNH LƯỢNG TỬ D1", use_container_width=True):
    decision, logic_reasons, winrate = evaluate_d1_quantum_signal(user_rsi, user_trend, user_fed, user_liquidity, user_price_action, user_macro)
    
    if "BUY" in decision:
        st.markdown(f"<div style='background-color: #D4EFDF; padding: 25px; border-radius: 8px; border-left: 8px solid #2ECC71;'>"
                    f"<h2 style='color: #196F3D !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Xác suất thành công của sóng ngày: <span style='color: #196F3D; font-weight: bold;'>{winrate}%</span>", unsafe_allow_html=True)
        
    elif "SELL" in decision:
        st.markdown(f"<div style='background-color: #FADBD8; padding: 25px; border-radius: 8px; border-left: 8px solid #E74C3C;'>"
                    f"<h2 style='color: #943126 !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Xác suất thành công của sóng ngày: <span style='color: #943126; font-weight: bold;'>{winrate}%</span>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div style='background-color: #FCF3CF; padding: 25px; border-radius: 8px; border-left: 8px solid #F1C40F;'>"
                    f"<h2 style='color: #B7950B !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)

    if logic_reasons:
        st.markdown("#### 🧠 Các luận điểm hội tụ tri thức vĩ mô và kỹ thuật:")
        for r in logic_reasons:
            st.write(f"✅ {r}")
