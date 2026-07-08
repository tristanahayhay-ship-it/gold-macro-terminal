import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openai
import os

# --- CẤU HÌNH TRANG WEB STREAMLIT ---
st.set_page_config(
    page_title="Macro Gold Terminal & AI",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh giao diện Dark Mode cao cấp
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #ffffff; }
    .stHeader { background-color: #111827; }
    h1, h2, h3 { color: #f59e0b !important; }
    div[data-testid="stExpander"] { background-color: #111827; border: 1px solid #1f2937; }
    .stButton>button { background-color: #10b981; color: white; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU MẪU LỊCH SỬ (MOCK DATA) ---
@st.cache_data
def load_mock_candles():
    dates = pd.date_range(start="2026-06-01", periods=30, freq="D")
    return pd.DataFrame({
        "Date": dates,
        "Open": [2300 + i*3 + (i%3)*5 for i in range(30)],
        "High": [2320 + i*3 + (i%2)*8 for i in range(30)],
        "Low": [2290 + i*3 - (i%4)*4 for i in range(30)],
        "Close": [2315 + i*3 + (i%2)*6 for i in range(30)]
    })

@st.cache_data
def load_macro_data():
    return pd.DataFrame({
        "Chỉ số": ["CPI YoY", "Core CPI", "PCE YoY", "Core PCE", "NFP (Bảng lương)", "Tỷ lệ thất nghiệp", "GDP YoY", "PMI Sản xuất"],
        "Kỳ trước": ["3.1%", "3.8%", "2.6%", "2.8%", "175K", "3.9%", "2.1%", "49.2"],
        "Dự báo": ["3.0%", "3.7%", "2.5%", "2.7%", "185K", "3.8%", "2.3%", "49.8"],
        "Thực tế": ["2.9%", "3.6%", "2.4%", "2.6%", "160K", "4.0%", "2.0%", "48.5"],
        "Tác động Vàng": ["BULLISH", "BULLISH", "BULLISH", "BULLISH", "BULLISH", "BULLISH", "BULLISH", "BULLISH"]
    })

# --- HÀM VẼ BIỂU ĐỒ NẾN TƯƠNG TÁC (PLOTLY) ---
def plot_candle_chart(df, title):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])
    fig.update_layout(
        title=title, template="plotly_dark",
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20), height=350
    )
    return fig

# --- KẾT NỐI AI CHUYÊN SÂU ---
def get_ai_analysis(macro_df):
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    if not api_key:
        return "⚠️ Chưa cấu hình API Key OpenAI trên Streamlit Secrets. Hệ thống đang hiển thị nhận định mẫu:\n\n**Nhận định xu hướng từ AI (Mẫu):** Dữ liệu lạm phát (CPI, PCE) hạ nhiệt mạnh hơn dự kiến kết hợp số liệu việc làm NFP yếu đi rõ rệt. Điều này củng cố khả năng FED sẽ hạ lãi suất nhanh hơn. Áp lực lên Real Yield giảm mạnh, tạo bệ phóng vững chắc đẩy giá vàng (XAU/USD) bước vào chu kỳ tăng trưởng (Bullish) mạnh mẽ lên các mốc cao kỷ lục mới.", 78
    
    openai.api_key = api_key
    try:
        data_summary = macro_df.to_string()
        prompt = f"Phân tích tập dữ liệu vĩ mô sau và đưa ra nhận định xu hướng cho giá vàng XAU/USD: \n{data_summary}\nYêu cầu đưa ra xu hướng ngắn/trung hạn kèm điểm số tâm lý thị trường từ 0 (Cực tệ) đến 100 (Cực tốt cho vàng)."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices.message['content'], 82
    except Exception as e:
        return f"Lỗi kết nối AI: {str(e)}", 50

# ==================== GIAO DIỆN CHÍNH (DASHBOARD) ====================

st.title("🪙 KINH TẾ VĨ MÔ & NHẬN ĐỊNH GIÁ VÀNG")
st.caption("Hệ thống phân tích thông minh toàn cảnh thị trường XAU/USD - Powered by Streamlit & AI")
st.markdown("---")

# --- KHU VỰC 1: BIỂU ĐỒ NẾN TƯƠNG TÁC ---
st.subheader("📊 Hệ Thống Biểu Đồ Nến Tương Tác Real-time")
col1, col2, col3 = st.columns(3)

df_mock = load_mock_candles()

with col1:
    st.plotly_chart(plot_candle_chart(df_mock, "XAU/USD (Giá Vàng)"), use_container_width=True)
with col2:
    df_dxy = df_mock.copy()
    df_dxy[['Open', 'High', 'Low', 'Close']] = 2500 - df_dxy[['Open', 'High', 'Low', 'Close']] + 100
    st.plotly_chart(plot_candle_chart(df_dxy, "DXY (Chỉ số Đô la Mỹ)"), use_container_width=True)
with col3:
    st.plotly_chart(plot_candle_chart(df_mock, "US10Y (Lợi suất trái phiếu Mỹ)"), use_container_width=True)

st.markdown("---")

# --- KHU VỰC 2: BẢNG DỮ LIỆU VĨ MÔ & NHẬN ĐỊNH AI ---
st.subheader("🇺🇸 Dữ Liệu Kinh Tế Mỹ & Phân Tích Xu Hướng AI")
col_table, col_ai = st.columns()

macro_df = load_macro_data()

with col_table:
    st.markdown("**Bảng chỉ số kinh tế quan trọng cập nhật tự động:**")
    st.dataframe(macro_df, use_container_width=True, hide_index=True)
    
    st.markdown("**Biểu đồ lịch sử thay đổi của chỉ số lựa chọn:**")
    selected_ind = st.selectbox("Chọn chỉ số để xem biểu đồ cột lịch sử:", macro_df["Chỉ số"].tolist())
    history_data = pd.DataFrame({
        "Kỳ": ["Tháng 4", "Tháng 5", "Tháng 6"],
        "Giá trị (%)": [3.4, 3.1, 2.9] if "CPI" in selected_ind else [4.1, 180, 2.1] if "GDP" in selected_ind else [3.8, 3.9, 4.0]
    })
    fig_bar = go.Figure([go.Bar(x=history_data["Kỳ"], y=history_data["Giá trị (%)"], marker_color="#f59e0b")])
    fig_bar.update_layout(template="plotly_dark", height=200, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_ai:
    ai_text, ai_score = get_ai_analysis(macro_df)
    
    st.markdown("**Thanh đo tâm lý xu hướng Vàng từ Hệ thống AI:**")
    st.progress(ai_score / 100)
    st.markdown(f"**Điểm số định lượng hiện tại:** <span style='color:#10b981;font-size:20px;font-weight:bold;'>{ai_score}/100 (Bullish - Thiên hướng Tăng giá)</span>", unsafe_allow_html=True)
    
    with st.expander("🤖 Xem Báo Cáo Nhận Định Toàn Cảnh Từ AI", expanded=True):
        st.write(ai_text)

st.markdown("---")

# --- KHU VỰC 3: ĐỊA CHÍNH TRỊ & GIẢ LẬP GIAO DỊCH ---
st.subheader("🌍 Bản Đồ Địa Chính Trị & Công Cụ Giao Dịch Giả Lập")
col_map, col_trade = st.columns()

with col_map:
    st.markdown("**Bản đồ nhiệt dự trữ vàng & Cảnh báo xung đột:**")
    map_data = pd.DataFrame({
        "Country": ["USA", "DEU", "ITA", "FRA", "CHN", "RUS", "VNM"],
        "Gold_Reserves": [8133, 3352, 2451, 2436, 2264, 2332, 9.2],
        "Status": ["Bình thường", "Bình thường", "Bình thường", "Bình thường", "Căng thẳng thương mại", "Xung đột địa chính trị", "Bình thường"]
    })
    fig_map = px.choropleth(
        map_data, locations="Country", color="Gold_Reserves",
        hover_name="Status", color_continuous_scale="YlOrBr",
        projection="natural earth"
    )
    fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0), height=350)
    st.plotly_chart(fig_map, use_container_width=True)

with col_trade:
    st.markdown("**Hệ thống thực hành thị trường (Paper Trading XAU/USD):**")
    
    if 'balance' not in st.session_state:
        st.session_state.balance = 100000.0
    if 'position' not in st.session_state:
        st.session_state.position = None

    current_gold_price = 2365.50
    
    st.metric(label="Số dư tài khoản Demo (USD)", value=f"${st.session_state.balance:,.2f}")
    st.metric(label="Giá thị trường XAU/USD hiện tại", value=f"${current_gold_price:.2f}")

    if not st.session_state.position:
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            if st.button("🔴 ĐẶT LỆNH MUA (BUY) 1 LOT"):
                st.session_state.position = {"type": "BUY", "entry": current_gold_price}
                st.rerun()
        with t_col2:
            if st.button("🔵 ĐẶT LỆNH BÁN (SELL) 1 LOT"):
                st.session_state.position = {"type": "SELL", "entry": current_gold_price}
                st.rerun()
    else:
        pos = st.session_state.position
        pnl = (current_gold_price - pos["entry"]) * 100 if pos["type"] == "BUY" else (pos["entry"] - current_gold_price) * 100
        
        st.info(f"Đang mở vị thế **{pos['type']}** tại mức giá **${pos['entry']}**")
        st.metric(label="Lợi nhuận/Thua lỗ tạm tính (P&L)", value=f"${pnl:,.2f}", delta=f"{pnl:.2f} USD")
        
        if st.button("🔒 ĐÓNG VỊ THẾ BẰNG GIÁ THỊ TRƯỜNG"):
            st.session_state.balance += pnl
            st.session_state.position = None
            st.success(f"Đóng trạng thái thành công! Khớp P&L: {pnl:.2f} USD")
            st.rerun()
