import streamlit as st
from macro_engine import evaluate_d1_quantum_signal

# 1. CẤU HÌNH TRANG WEB TOÀN CỤC
st.set_page_config(page_title="XAUUSD D1 Macro Executive Terminal", layout="wide")

# 2. BỘ MÃ HÓA CSS TỐI ƯU HIỂN THỊ (SỬA LỖI CHỮ MỜ)
st.markdown("""
    <style>
    /* Nền tối Bloomberg Terminal */
    .stApp { background-color: #04060A !important; }
    .stSelectbox, .stNumberInput { background-color: #0E121A !important; }
    
    /* Ép tất cả các văn bản lên màu trắng rõ nét, độ tương phản cao */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div, span, li { 
        color: #FFFFFF !important; 
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Làm nổi bật nhãn tiêu đề của các ô nhập liệu */
    div[data-testid="stWidgetLabel"] p {
        font-size: 16px !important;
        font-weight: bold !important;
        color: #00FF66 !important; /* Màu xanh neon chuyên nghiệp */
    }
    
    /* Tăng cỡ chữ trong hộp chọn */
    div[data-baseweb="select"] span {
        font-size: 15px !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. TIÊU ĐỀ TRẠM ĐIỀU HÀNH
st.title("🏛️ TRẠM ĐIỀU HÀNH THẨM ĐỊNH LƯỢNG TỬ KHUNG NGÀY D1 (XAUUSD)")
st.caption("Hệ thống phân tích ma trận dữ liệu đóng nến Ngày - Chuyên đánh sóng dài hạn (Swing Trading)")
st.markdown("---")

# 4. KHU VỰC NHẬP DỮ LIỆU ĐÓNG NẾN NGÀY D1
st.markdown("### 📥 DỮ LIỆU ĐÓNG NẾN NGÀY D1 THỰC TẾ (QUAN SÁT MỖI NGÀY 1 LẦN LÚC 4H-5H SÁNG)")
col1, col2 = st.columns(2)

with col1:
    user_rsi = st.number_input("1. Chỉ số RSI trên khung D1 hiện tại (0 - 100):", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    user_trend = st.selectbox("2. Cấu trúc xu hướng chủ đạo trên khung D1:", ["Xu hướng Tăng dài hạn (Bullish)", "Xu hướng Giảm dài hạn (Bearish)", "Xu hướng Đi ngang / Không rõ ràng (Sideway)"])
    user_price_action = st.selectbox("3. Tín hiệu đóng nến Ngày D1 vừa qua (Price Action):", ["Nến D1 Đảo chiều Tăng mạnh (Pinbar rút râu dài / Engulfing xanh ôm trọn)", "Nến D1 Đảo chiều Giảm mạnh (Pinbar từ chối đỉnh / Engulfing đỏ nuốt chửng)", "Nến Doji / Nến thân nhỏ biến động hẹp"])

with col2:
    user_liquidity = st.selectbox("4. Vị trí giá D1 so với vùng Cản lớn (D1/W1):", ["Chạm Vùng Hỗ trợ D1 / Order Block Tăng tuần", "Chạm Vùng Kháng cự D1 / Order Block Giảm tuần", "Nằm lơ lửng giữa các vùng cản lớn"])
    user_fed = st.selectbox("5. Định hướng chính sách tiền tệ dài hạn của FED:", ["Nới lỏng (Cắt giảm lãi suất / Bơm tiền / USD suy yếu)", "Thắt chặt (Tăng lãi suất / Giữ lãi suất cao / USD mạnh)", "Trung lập (FED chờ đợi thêm số liệu lạm phát)"])

st.markdown("---")

# 5. KHU VỰC SỬ LÝ VÀ PHÁN QUYẾT CHIẾN LƯỢC TỐI CAO
st.markdown("### 🎯 PHÁN QUYẾT CHIẾN LƯỢC TOÀN CỤC KHUNG NGÀY D1")

if st.button("🚀 KÍCH HOẠT THẨM ĐỊNH TOÀN DIỆN KHUNG NGÀY", use_container_width=True):
    # Gọi bộ não đa tầng xử lý từ file macro_engine.py
    decision, logic_reasons, winrate = evaluate_d1_quantum_signal(user_rsi, user_trend, user_fed, user_liquidity, user_price_action)
    
    if "BUY" in decision:
        st.markdown(f"<div style='background-color: #112A11; padding: 25px; border-radius: 8px; border-left: 8px solid #2ECC71;'>"
                    f"<h2 style='color: #2ECC71 !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Xác suất thành công của sóng ngày: <span style='color: #2ECC71; font-weight: bold;'>{winrate}%</span>", unsafe_allow_html=True)
        st.info("💡 **Chiến lược Quản trị vốn Swing D1:** Kích hoạt vị thế MUA và xác định giữ lệnh từ vài ngày đến vài tuần. Điểm dừng lỗ (SL) phải đặt an toàn dưới đáy nến D1 đảo chiều (Thường cách điểm vào lệnh từ 15 - 25 USD tùy biến động ATR ngày). Mục tiêu chốt lời (TP) hướng tới vùng kháng cự đỉnh D1 tiếp theo.")
        
    elif "SELL" in decision:
        st.markdown(f"<div style='background-color: #2A1111; padding: 25px; border-radius: 8px; border-left: 8px solid #E74C3C;'>"
                    f"<h2 style='color: #E74C3C !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"### 📊 Xác suất thành công của sóng ngày: <span style='color: #E74C3C; font-weight: bold;'>{winrate}%</span>", unsafe_allow_html=True)
        st.error("💡 **Chiến lược Quản trị vốn Swing D1:** Kích hoạt vị thế BÁN và giữ vị thế dài hạn. Điểm dừng lỗ (SL) đặt trên đỉnh nến D1 xác nhận (Cách điểm vào lệnh từ 15 - 25 USD). Mục tiêu chốt lời (TP) hướng tới dải hỗ trợ đáy D1 tiếp theo.")
        
    else:
        st.markdown(f"<div style='background-color: #1A1A0A; padding: 25px; border-radius: 8px; border-left: 8px solid #F1C40F;'>"
                    f"<h2 style='color: #F1C40F !important; margin: 0; text-align: center; font-weight: bold;'>🎯 {decision}</h2>"
                    f"</div>", unsafe_allow_html=True)
        st.warning("⚠️ **Hành động phòng thủ vốn:** ĐỨNG NGOÀI THỊ TRƯỜNG. Khung D1 chưa cho thấy sự đồng thuận tuyệt đối giữa Vĩ mô và Hành động giá Kỹ thuật. Tuyệt đối không mạo hiểm vốn dài hạn khi thị trường mập mờ.")

    # 6. HIỂN THỊ LUẬN ĐIỂM CHI TIẾT
    if logic_reasons:
        st.markdown("#### 🧠 Các luận điểm hội tụ dòng tiền lớn:")
        for r in logic_reasons:
            st.write(f"📈 {r}")
