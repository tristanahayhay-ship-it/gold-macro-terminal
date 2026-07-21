import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN TERMINAL SCI-FI GÓC RỘNG TRÀN MÀN HÌNH
# ==============================================================================
st.set_page_config(
    page_title="Global Hologram Flow Terminal",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #020406; color: #dcdde1; }
    .terminal-card { background-color: #0a0e14; padding: 20px; border-radius: 8px; border: 1px solid #1c273c; margin-top: 15px; box-shadow: 0 0 15px rgba(28,39,60,0.3); }
    .status-badge { font-weight: bold; padding: 6px 12px; border-radius: 4px; font-size: 16px; box-shadow: 0 0 10px currentColor; }
    </style>
""", unsafe_allow_html=True)

st.title("🕸️ GLOBAL FINANCIAL HOLOGRAM TERMINAL (PRO v8.0)")
st.subheader("Mạng lưới Xung nhịp Dòng chảy Chằng chịt Toàn cầu - Thiết kế Đồ họa Cao cấp")
st.markdown("---")

# 2. SIDEBAR ĐIỀU KHIỂN ĐỘNG LỰC TOÀN CẦU
st.sidebar.header("🎛️ TỔNG TÀI KHOẢN VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "Chọn Trạng thái Chỉ số Dòng tiền:",
    ["Đồng USD giảm - Tổng lực ĐẦU TƯ TOÀN CẦU CHẰNG CHỊT (MÀU XANH NEON OUT)", 
     "Đồng USD tăng - Bán tháo rút dòng về Mỹ TRÚ ẨN (MÀU ĐỎ RUBY IN)"]
)

selected_agent = st.sidebar.radio(
    "Tiêu điểm Khối Thực thể chạy dây:",
    ["Tất cả chủ thể (Cá nhân & Tập đoàn)", "Chỉ hiện Nhà đầu tư Cá nhân (Retail)", "Chỉ hiện Khối Tập đoàn lớn (Corporate)"]
)

total_capital = st.sidebar.number_input("Tổng quy mô dòng vốn hệ thống vận chuyển (USD):", min_value=1000000, value=500000000, format="%d")

# Thiết lập hệ màu phối quang cao cấp (Neon Aesthetic)
if "MÀU XANH" in market_phase:
    flow_type, pulse_color, base_color, dash_pattern, badge_style, status_label = "INVESTMENT", "#00ff88", "rgba(0, 255, 136, 0.05)", "2 3 2 3", "background-color: rgba(0, 255, 136, 0.15); color: #00ff88;", "XUNG LỰC ĐẦU TƯ TOÀN CẦU (RISK-ON)"
else:
    flow_type, pulse_color, base_color, dash_pattern, badge_style, status_label = "SAFE_HAVEN", "#ff3838", "rgba(255, 56, 56, 0.05)", "6 3 6 3", "background-color: rgba(255, 56, 56, 0.15); color: #ff3838;", "KHỦNG HOẢNG THÁO CHẠY VỀ TRÚ ẨN (RISK-OFF)"

# 3. CƠ SỞ DỮ LIỆU ĐA LỚP TOÀN CẦU (GỘP 195 NƯỚC QUA CÁC TRỤC CHÍNH)
us_hq = {"name": "Mỹ (Trung tâm USD/Fed)", "lat": 38.9, "lon": -77.0}

macro_mesh = {
    "Việt Nam": {"lat_c1": 21.0, "lon_c1": 105.8, "lat_ag": 16.0, "lon_ag": 108.2, "lat_as": 10.7, "lon_as": 106.7, "name_as": "Sàn HOSE / Đất nền vùng ven"},
    "Trung Quốc": {"lat_c1": 39.9, "lon_c1": 116.4, "lat_ag": 31.2, "lon_ag": 121.4, "lat_as": 22.5, "lon_as": 114.0, "name_as": "Sàn Thâm Quyến / Thượng Hải"},
    "Nhật Bản": {"lat_c1": 35.6, "lon_c1": 139.6, "lat_ag": 34.6, "lon_ag": 135.5, "lat_as": 35.0, "lon_as": 136.0, "name_as": "Sàn Nikkei / Yên JPY"},
    "Đức": {"lat_c1": 52.5, "lon_c1": 13.4, "lat_ag": 50.1, "lon_ag": 8.6, "lat_as": 48.1, "lon_as": 11.5, "name_as": "Thị trường Frankfurt"},
    "Anh": {"lat_c1": 51.5, "lon_c1": -0.1, "lat_ag": 53.4, "lon_ag": -2.2, "lat_as": 55.9, "lon_as": -3.1, "name_as": "Sàn LSE / Bảng Anh"},
    "Singapore": {"lat_c1": 1.35, "lon_c1": 103.8, "lat_ag": 1.30, "lon_ag": 103.7, "lat_as": 1.40, "lon_as": 103.9, "name_as": "Trung tâm Tài chính Đông Nam Á"},
    "Thụy Sĩ": {"lat_c1": 46.9, "lon_c1": 7.4, "lat_ag": 47.3, "lon_ag": 8.5, "lat_as": 46.2, "lon_as": 6.1, "name_as": "Vàng & Franc Thụy Sĩ (CHF)"},
    "Úc": {"lat_c1": -35.2, "lon_c1": 149.1, "lat_ag": -33.8, "lon_ag": 151.2, "lat_as": -37.8, "lon_as": 144.9, "name_as": "Hàng hóa Quặng Sydney"}
}

# Tự động hóa sinh thêm 35 nút mạng lưới quốc gia ngẫu nhiên để tăng độ chằng chịt phủ kín bản đồ
for i in range(1, 36):
    macro_mesh[f"Trục Quốc gia {i}"] = {
        "lat_c1": 15.0 + (i * 0.9), "lon_c1": -50.0 + (i * 2.8),
        "lat_ag": 10.0 + (i * 0.9), "lon_ag": -55.0 + (i * 2.8),
        "lat_as": 5.0 + (i * 0.9), "lon_as": -60.0 + (i * 2.8),
        "name_as": f"Hạ tầng Tài sản nội bang {i}"
    }
# 4. ENGINE ĐỒ HỌA MẠNG LƯỚI MA TRẬN HOLOGRAM CAO CẤP
fig = go.Figure()

# Vẽ trung tâm nước Mỹ (Ngôi sao phát sáng đa tầng)
fig.add_trace(go.Scattergeo(
    lon = [us_hq["lon"]], lat = [us_hq["lat"]],
    text = f"⭐ {us_hq['name']}", mode = "markers",
    marker = dict(size=18, color="#f1c40f", symbol="star", line=dict(color="#fff", width=1.5), opacity=0.95)
))

# Vòng lặp liên kết mạng nhện xiên quốc gia và nội địa
for country, data in macro_mesh.items():
    # Vẽ điểm nút đầu não quốc gia (Màu ngọc lục bảo rực sáng)
    fig.add_trace(go.Scattergeo(lon=[data["lon_c1"]], lat=[data["lat_c1"]], text=f"🏛️ Thượng tầng: {country}", mode="markers", marker=dict(size=8, color="#00d2d3", symbol="square", opacity=0.8)))
    
    # Vẽ các nút Agent vi mô nội địa
    if "Tập đoàn" not in selected_agent:
        fig.add_trace(go.Scattergeo(lon=[data["lon_ag"]], lat=[data["lat_ag"]], text=f"👤 Cá nhân ({country})", mode="markers", marker=dict(size=6, color="#ff9f43", symbol="diamond")))
    if "Cá nhân" not in selected_agent:
        fig.add_trace(go.Scattergeo(lon=[data["lon_ag"]+0.3], lat=[data["lat_ag"]+0.3], text=f"🏢 Tập đoàn ({country})", mode="markers", marker=dict(size=6, color="#ea2027", symbol="triangle-up")))
        
    # Vẽ điểm nút tài sản đích
    fig.add_trace(go.Scattergeo(lon=[data["lon_as"]], lat=[data["lat_as"]], text=f"🎯 Đích: {data['name_as']}", mode="markers", marker=dict(size=7, color=pulse_color if flow_type=="INVESTMENT" else "#57606f", opacity=0.8)))

    # THUẬT TOÁN ĐA LỚP GIĂNG LƯỚI ĐƯỜNG CONG HOẠT HỌA PHÁT SÁNG "CHẠY CHẠY"
    # D1. Tuyến liên quốc gia kết nối với Mỹ (Đường chỉ mảnh + Đường mạch xung nhịp rực sáng)
    cross_lon = [us_hq["lon"], data["lon_c1"]] if flow_type == "INVESTMENT" else [data["lon_c1"], us_hq["lon"]]
    cross_lat = [us_hq["lat"], data["lat_c1"]] if flow_type == "INVESTMENT" else [data["lat_c1"], us_hq["lat"]]
    
    # Sợi quang nền mờ tinh tế
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=1, color=base_color), opacity=0.3, hoverinfo="none"))
    # Mạch xung động nhấp nháy chuyển động rực màu dạ quang
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=2.5, color=pulse_color, dash=dash_pattern), opacity=0.9, hoverinfo="none"))

    # D2. Tuyến nội địa phân rã đa cấp rẽ nhánh
    local_lon = [data["lon_c1"], data["lon_ag"], data["lon_as"]] if flow_type == "INVESTMENT" else [data["lon_as"], data["lon_ag"], data["lon_c1"]]
    local_lat = [data["lat_c1"], data["lat_ag"], data["lat_as"]] if flow_type == "INVESTMENT" else [data["lat_as"], data["lat_ag"], data["lat_c1"]]
    
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=1, color=base_color), opacity=0.3, hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=3, color=pulse_color, dash=dash_pattern), opacity=0.9, hoverinfo="none"))

# THIẾT LẬP LỚP NỀN HOLOGRAM 3D ĐỘC QUYỀN (PREMIUM DARK SCI-FI STYLING)
fig.update_layout(
    showlegend = False,
    height = 750, # Kéo giãn tối đa để tạo không gian bản đồ cực to và rộng
    margin = dict(l=0, r=0, t=10, b=0),
    paper_bgcolor = "rgba(0,0,0,0)", # Làm trong suốt nền bao quanh
    plot_bgcolor = "rgba(0,0,0,0)"
)

fig.update_geos(
    scope = "world",
    projection_type = "natural earth",
    showland = True, landcolor = "#10141d", # Màu đất liền kim loại tối cao cấp
    countrycolor = "#1c2a38", showcountries = True, # Đường viền quốc gia dạ quang xanh mờ
    countrywidth = 0.8,
    showocean = True, oceancolor = "#030508", # Đại dương đen huyền bí
    showlakes = False
)

# 5. ĐẨY BẢN ĐỒ LÊN VỊ TRÍ ĐỘC TÔN TO TOÀN MÀN HÌNH
st.plotly_chart(fig, use_container_width=True)

# 6. KHU VỰC THÔNG TIN TERMINAL DƯỚI CHÂN TRANG
col_text, col_stats = st.columns(2)

with col_text:
    st.markdown("### 🎚️ Trung tâm Điều phối Luồng Hệ thống")
    st.markdown(f"Trạng thái mạng lưới: <span class='status-badge' style='{badge_style}'>{status_label}</span>", unsafe_allow_html=True)
    st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Bản chất của mạng lưới dây chuyển động chằng chịt:")
    if flow_type == "INVESTMENT":
        st.write("🟢 **MẠCH XUNG XANH LÁ CHẠY TOẢ RA NGOÀI (Outflow):** Hệ thống vĩ mô nới lỏng toàn diện. Đồng USD suy yếu kích hoạt van giải ngân từ Mỹ phóng mạng nhện đường dây xanh đi khắp thế giới. Tại nội địa các nước, luồng tín dụng này kích hoạt nhịp chạy của khối Cá nhân và Doanh nghiệp lao vào nâng đỡ thanh khoản thị trường cổ phiếu, thúc đẩy làn sóng xây dựng nhà xưởng sản xuất.")
    else:
        st.write("🔴 **MẠCH XUNG ĐỎ RUBY CHẠY HÚT VÀO TRONG (Inflow):** Khủng hoảng thanh khoản kích hoạt. Toàn bộ các sợi dây kết nối tài sản rủi ro quốc tế bị thắt nút đóng băng. Hệ thống bản đồ phủ kín hàng loạt dải sáng màu đỏ rực chạy dồn dập cuộn ngược dòng, rút dòng vốn ngoại từ các quốc gia chảy xuyên biên giới quay thẳng về trục két sắt an toàn tại Mỹ.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_stats:
    st.markdown("### 🗜️ Tóm tắt Ma trận Vốn liên quốc gia (Top 5 Trục lớn)")
    matrix_rows = []
    top_countries = ["Việt Nam", "Trung Quốc", "Thụy Sĩ", "Nhật Bản", "Đức"]
    for country in top_countries:
        allocated_val = total_capital / len(macro_mesh)
        matrix_rows.append({"Trục kết nối vĩ mô": f"Mỹ ➔ {country}", "Tín hiệu chuyển động": "🟢 TỎA RA ĐẦU TƯ" if flow_type == "INVESTMENT" else "🔴 HÚT VỀ TRÚ ẨN", "Hạ tầng tiếp nhận tiêu biểu": macro_mesh[country]["name_as"], "Trạng thái hoạt họa": "Dải XANH phát sáng" if flow_type == "INVESTMENT" else "Dải ĐỎ dồn dập", "Dòng vốn ước tính (USD)": f"${allocated_val:,.0f} USD"})
    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
