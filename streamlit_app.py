import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN TERMINAL TỐI GÓC RỘNG TRÊN CÙNG (SUPER FULL-WIDTH LAYOUT)
# ==============================================================================
st.set_page_config(
    page_title="Global Mesh Macro Terminal",
    page_icon="🕸️",
    layout="wide", # Kích hoạt chế độ tràn màn hình góc rộng
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e1e6eb; }
    .terminal-card { background-color: #0d1117; padding: 20px; border-radius: 8px; border: 1px solid #1f2633; margin-top: 15px; }
    .status-badge { font-weight: bold; padding: 6px 12px; border-radius: 4px; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

st.title("🕸️ GLOBAL FINANCIAL MESH TERMINAL (MEGA-VIEW)")
st.subheader("Mạng lưới Xung nhịp Dòng chảy Chằng chịt Toàn cầu - Tương quan 195 Quốc gia")
st.markdown("---")

# 2. SIDEBAR ĐIỀU KHIỂN ĐỘNG LỰC TOÀN CẦU
st.sidebar.header("🎛️ TỔNG TÀI KHOẢN VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "Chọn Trạng thái Chỉ số Dòng tiền:",
    ["Đồng USD giảm - Tổng lực ĐẦU TƯ TOÀN CẦU CHẰNG CHỊT (MÀU XANH CHẠY OUT)", 
     "Đồng USD tăng - Bán tháo rút dòng về Mỹ TRÚ ẨN (MÀU ĐỎ CHẠY IN)"]
)

selected_agent = st.sidebar.radio(
    "Tiêu điểm Khối Thực thể chạy dây:",
    ["Tất cả chủ thể (Cá nhân & Tập đoàn)", "Chỉ hiện Nhà đầu tư Cá nhân (Retail)", "Chỉ hiện Khối Tập đoàn lớn (Corporate)"]
)

total_capital = st.sidebar.number_input("Tổng quy mô dòng vốn hệ thống vận chuyển (USD):", min_value=1000000, value=500000000, format="%d")

# Thiết lập xung nhịp hoạt họa chạy dòng tiền
if "MÀU XANH" in market_phase:
    flow_type, pulse_color, base_color, dash_pattern, badge_style, status_label = "INVESTMENT", "#2ecc71", "rgba(46, 204, 113, 0.08)", "4 4 4 4", "background-color: rgba(46, 204, 113, 0.2); color: #2ecc71;", "HỆ THỐNG XUNG LỰC ĐẦU TƯ TỔNG LỰC (RISK-ON)"
else:
    flow_type, pulse_color, base_color, dash_pattern, badge_style, status_label = "SAFE_HAVEN", "#e74c3c", "rgba(231, 76, 60, 0.08)", "8 4 8 4", "background-color: rgba(231, 76, 60, 0.2); color: #e74c3c;", "HỆ THỐNG KHỦNG HOẢNG THÁO CHẠY VỀ MỸ (RISK-OFF)"

# 3. SƠ SỞ DỮ LIỆU ĐA LỚP TOÀN CẦU (GỘP ĐỒNG THỜI TOÀN BỘ CÁC TRỤC QUỐC GIA LỚN)
us_hq = {"name": "Mỹ (Trung tâm USD/Fed/Treasury)", "lat": 38.9072, "lon": -77.0369}

macro_mesh = {
    "Việt Nam": {"lat_c1": 21.0, "lon_c1": 105.8, "lat_ag": 14.0, "lon_ag": 108.0, "lat_as": 10.7, "lon_as": 106.7, "name_as": "Sàn HOSE / BĐS Vùng ven"},
    "Trung Quốc": {"lat_c1": 39.9, "lon_c1": 116.4, "lat_ag": 31.2, "lon_ag": 121.4, "lat_as": 22.5, "lon_as": 114.0, "name_as": "Sàn Thâm Quyến / Thượng Hải"},
    "Nhật Bản": {"lat_c1": 35.6, "lon_c1": 139.6, "lat_ag": 34.6, "lon_ag": 135.5, "lat_as": 35.0, "lon_as": 136.0, "name_as": "Sàn Nikkei / Trái phiếu Yên JPY"},
    "Đức": {"lat_c1": 52.5, "lon_c1": 13.4, "lat_ag": 50.1, "lon_ag": 8.6, "lat_as": 48.1, "lon_as": 11.5, "name_as": "Thị trường Công nghiệp Frankfurt"},
    "Anh": {"lat_c1": 51.5, "lon_c1": -0.1, "lat_ag": 53.4, "lon_ag": -2.2, "lat_as": 55.9, "lon_as": -3.1, "name_as": "Sàn LSE / Công cụ nợ Bảng Anh"},
    "Singapore": {"lat_c1": 1.35, "lon_c1": 103.8, "lat_ag": 1.30, "lon_ag": 103.7, "lat_as": 1.40, "lon_as": 103.9, "name_as": "Trung tâm Tài chính Đông Nam Á"},
    "Thụy Sĩ": {"lat_c1": 46.9, "lon_c1": 7.4, "lat_ag": 47.3, "lon_ag": 8.5, "lat_as": 46.2, "lon_as": 6.1, "name_as": "Két sắt Vàng & Franc Thụy Sĩ (CHF)"},
    "Úc": {"lat_c1": -35.2, "lon_c1": 149.1, "lat_ag": -33.8, "lon_ag": 151.2, "lat_as": -37.8, "lon_as": 144.9, "name_as": "Thị trường Hàng hóa Quặng Sydney"}
}

# Tự động hóa sinh thêm 30 nút mạng lưới đại diện cho các quốc gia còn lại để tăng độ chằng chịt
for i in range(1, 31):
    macro_mesh[f"Quốc gia Mẫu {i}"] = {
        "lat_c1": 20.0 + (i * 0.8), "lon_c1": -40.0 + (i * 2.5),
        "lat_ag": 15.0 + (i * 0.8), "lon_ag": -45.0 + (i * 2.5),
        "lat_as": 10.0 + (i * 0.8), "lon_as": -50.0 + (i * 2.5),
        "name_as": f"Hạ tầng Tài sản nội bang {i}"
    }
# 4. ENGINE ĐỒ HỌA MẠNG LƯỚI MA TRẬN CHẰNG CHỊT TOÀN CẦU
fig = go.Figure()

# Vẽ điểm nút Thượng tầng Mỹ (Trung tâm hấp thụ USD tối cao)
fig.add_trace(go.Scattergeo(
    lon = [us_hq["lon"]], lat = [us_hq["lat"]],
    text = f"⭐ {us_hq['name']}", mode = "markers+text", textposition = "top center",
    marker = dict(size=16, color="#f39c12", symbol="star", line=dict(color="#fff", width=2))
))

for country, data in macro_mesh.items():
    fig.add_trace(go.Scattergeo(lon=[data["lon_c1"]], lat=[data["lat_c1"]], text=f"🏛️ {country}", mode="markers", marker=dict(size=9, color="#1abc9c", symbol="square")))
    
    if "Tập đoàn" not in selected_agent:
        fig.add_trace(go.Scattergeo(lon=[data["lon_ag"]], lat=[data["lat_ag"]], text=f"👤 Cá nhân ({country})", mode="markers", marker=dict(size=7, color="#f1c40f", symbol="diamond")))
    if "Cá nhân" not in selected_agent:
        fig.add_trace(go.Scattergeo(lon=[data["lon_ag"]+0.2], lat=[data["lat_ag"]+0.2], text=f"🏢 Tập đoàn ({country})", mode="markers", marker=dict(size=7, color="#e67e22", symbol="triangle-up")))
        
    fig.add_trace(go.Scattergeo(lon=[data["lon_as"]], lat=[data["lat_as"]], text=f"🎯 {data['name_as']}", mode="markers", marker=dict(size=8, color=pulse_color if flow_type=="INVESTMENT" else "#7f8c8d")))

    # THUẬT TOÁN ĐA LỚP GIĂNG LƯỚI ĐƯỜNG DÂY CHẰNG CHỊT NHẤP NHÁY "CHẠY CHẠY"
    cross_lon = [us_hq["lon"], data["lon_c1"]] if flow_type == "INVESTMENT" else [data["lon_c1"], us_hq["lon"]]
    cross_lat = [us_hq["lat"], data["lat_c1"]] if flow_type == "INVESTMENT" else [data["lat_c1"], us_hq["lat"]]
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=1, color=base_color), hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=2.5, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

    local_lon = [data["lon_c1"], data["lon_ag"], data["lon_as"]] if flow_type == "INVESTMENT" else [data["lon_as"], data["lon_ag"], data["lon_c1"]]
    local_lat = [data["lat_c1"], data["lat_ag"], data["lat_as"]] if flow_type == "INVESTMENT" else [data["lat_as"], data["lat_ag"], data["lat_c1"]]
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=1, color=base_color), hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=3, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

# Thiết lập Bản đồ phẳng góc rộng phóng to kích thước tối đa toàn cầu (Mega-view Layout)
fig.update_layout(showlegend = False, height = 700, margin = dict(l=0, r=0, t=10, b=0))
fig.update_geos(scope = "world", projection_type = "natural earth", showland = True, landcolor = "#090c10", countrycolor = "#1f242e", showcountries = True, showocean = True, oceancolor = "#040508")

# 5. HIỂN THỊ BIỂU ĐỒ BẢN ĐỒ TO TRÊN CÙNG TRÀN MÀN HÌNH
st.plotly_chart(fig, use_container_width=True)

# 6. KHU VỰC THÔNG TIN TERMINAL VÀ MA TRẬN ĐỊNH LƯỢNG Ở PHÍA DƯỚI
col_text, col_stats = st.columns(2)

with col_text:
    st.markdown("### 🎚️ Trung tâm Phân tích Luồng Hệ thống")
    st.markdown(f"Trạng thái mạng lưới: <span class='status-badge' style='{badge_style}'>{status_label}</span>", unsafe_allow_html=True)
    st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Bản chất của mạng lưới dây chuyển động chằng chịt:")
    if flow_type == "INVESTMENT":
        st.write("🟢 **MÀU XANH LÁ CHẠY TOẢ RA NGOÀI (Outflow):** Chỉ số sức mạnh USD giảm nhiệt, chiếc van tiền từ nước Mỹ mở ra. Bạn nhìn thấy rõ hàng trăm sợi cáp quang đang nhấp nháy các hạt bụi sáng chạy bắn liên tục từ Mỹ phóng ra 195 quốc gia. Tại nội địa từng nước, dòng vốn ngoại này tiếp tục rẽ nhánh thành các đường dây vi mô chạy luồn lách xuống các tài khoản của Cá nhân và Tập đoàn, đẩy mạnh sản xuất và thổi bùng thanh khoản các sàn chứng khoán (HOSE, Thâm Quyến, Frankfurt) và bất động sản.")
    else:
        st.write("🔴 **MÀU ĐỎ CHẠY CUỘN VÀO TRONG (Inflow):** Rủi ro hệ thống bùng nổ, lực hút của nước Mỹ kích hoạt. Toàn bộ các trục tài sản rủi ro quốc tế lập tức bị ngắt kết nối. Mạng lưới bản đồ bị bao phủ bởi hàng trăm đường chỉ đỏ chạy giật nhịp cuộn dồn dập ngược từ các quốc gia đổ thẳng về trung tâm nước Mỹ. Nhà đầu tư toàn cầu bán tháo tài sản nội địa, chuyển hóa dòng tiền chạy xuyên biên giới để tháo chạy vào kho dự trữ Vàng và Trái phiếu chính phủ Mỹ.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_stats:
    st.markdown("### 🗜️ Tóm tắt Ma trận Điều phối Vốn liên quốc gia (Top 5 Trục lớn)")
    matrix_rows = []
    top_countries = ["Việt Nam", "Trung Quốc", "Thụy Sĩ", "Nhật Bản", "Đức"]
    for country in top_countries:
        allocated_val = total_capital / len(macro_mesh)
        matrix_rows.append({"Trục kết nối vĩ mô": f"Mỹ ➔ {country}", "Tín hiệu chuyển động": "🟢 TỎA RA ĐẦU TƯ" if flow_type == "INVESTMENT" else "🔴 HÚT VỀ TRÚ ẨN", "Hạ tầng tiếp nhận tiêu biểu": macro_mesh[country]["name_as"], "Trạng thái hoạt họa": "Dải XANH chạy Out" if flow_type == "INVESTMENT" else "Dải ĐỎ chạy In", "Dòng vốn ước tính (USD)": f"${allocated_val:,.0f} USD"})
    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
