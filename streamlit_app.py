import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN TERMINAL PHẲNG (FLAT FLAT DESIGN)
# ==============================================================================
st.set_page_config(
    page_title="Global Flat Map Terminal",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #eef2f5; color: #1e272e; }
    .terminal-card { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #dcdde1; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .status-badge { font-weight: bold; padding: 6px 12px; border-radius: 4px; font-size: 16px; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ GLOBAL FINANCIAL FLAT TERMINAL (VIETNAM STYLE)")
st.subheader("Mạng lưới Dòng chảy: Hệ thống khóa dịch chuyển dọc (Chỉ cuộn ngang & Zoom)")
st.markdown("---")

# 2. SIDEBAR ĐIỀU KHIỂN DÒNG VỐN
st.sidebar.header("🎛️ TỔNG TÀI KHOẢN VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "Chọn Trạng thái Chỉ số Dòng tiền:",
    ["Đồng USD giảm - Tổng lực ĐẦU TƯ TOÀN CẦU CHẰNG CHỊT (MÀU XANH OUT)", 
     "Đồng USD tăng - Bán tháo rút dòng về Mỹ TRÚ ẨN (MÀU ĐỎ IN)"]
)

selected_agent = st.sidebar.radio(
    "Tiêu điểm Khối Thực thể chạy dây:",
    ["Tất cả chủ thể (Cá nhân & Tập đoàn)", "Chỉ hiện Nhà đầu tư Cá nhân (Retail)", "Chỉ hiện Khối Tập đoàn lớn (Corporate)"]
)

total_capital = st.sidebar.number_input("Tổng quy mô dòng vốn hệ thống vận chuyển (USD):", min_value=1000000, value=500000000, format="%d")

# Phối màu đường chỉ chuyển động tương phản trên nền bản đồ Đỏ - Vàng
if "MÀU XANH" in market_phase:
    flow_type, pulse_color, base_color, dash_pattern, badge_bg, status_label = "INVESTMENT", "#00b894", "rgba(0, 184, 148, 0.15)", "4 4 4 4", "#00b894", "XUNG LỰC ĐẦU TƯ TOÀN CẦU (RISK-ON)"
else:
    flow_type, pulse_color, base_color, dash_pattern, badge_bg, status_label = "SAFE_HAVEN", "#d63031", "rgba(214, 48, 49, 0.15)", "8 4 8 4", "#d63031", "KHỦNG HOẢNG THÁO CHẠY VỀ TRÚ ẨN (RISK-OFF)"

# 3. CƠ SỞ DỮ LIỆU TOÀN CẦU VỚI VIỆT NAM LÀM TÂM ĐIỂM ĐỊA LÝ
us_hq = {"name": "Mỹ (Trung tâm USD/Fed)", "lat": 38.9, "lon": -77.0}

macro_mesh = {
    "Việt Nam": {"lat_c1": 21.0, "lon_c1": 105.8, "lat_ag": 16.0, "lon_ag": 108.2, "lat_as": 10.7, "lon_as": 106.7, "name_as": "Sàn HOSE / Đất nền vùng ven", "intensity": 95},
    "Trung Quốc": {"lat_c1": 39.9, "lon_c1": 116.4, "lat_ag": 31.2, "lon_ag": 121.4, "lat_as": 22.5, "lon_as": 114.0, "name_as": "Sàn Thâm Quyến / Thượng Hải", "intensity": 80},
    "Nhật Bản": {"lat_c1": 35.6, "lon_c1": 139.6, "lat_ag": 34.6, "lon_ag": 135.5, "lat_as": 35.0, "lon_as": 136.0, "name_as": "Sàn Nikkei / Yên JPY", "intensity": 75},
    "Đức": {"lat_c1": 52.5, "lon_c1": 13.4, "lat_ag": 50.1, "lon_ag": 8.6, "lat_as": 48.1, "lon_as": 11.5, "name_as": "Thị trường Frankfurt", "intensity": 70},
    "Anh": {"lat_c1": 51.5, "lon_c1": -0.1, "lat_ag": 53.4, "lon_ag": -2.2, "lat_as": 55.9, "lon_as": -3.1, "name_as": "Sàn LSE / Bảng Anh", "intensity": 65},
    "Singapore": {"lat_c1": 1.35, "lon_c1": 103.8, "lat_ag": 1.30, "lon_ag": 103.7, "lat_as": 1.40, "lon_as": 103.9, "name_as": "Trung tâm Tài chính ĐNA", "intensity": 85},
    "Thụy Sĩ": {"lat_c1": 46.9, "lon_c1": 7.4, "lat_ag": 47.3, "lon_ag": 8.5, "lat_as": 46.2, "lon_as": 6.1, "name_as": "Vàng & Franc Thụy Sĩ", "intensity": 90}
}
# 4. ENGINE DỰNG BẢN ĐỒ PHẲNG ĐỎ VÀNG THEO YÊU CẦU ẢNH MẪU
fig = go.Figure()

# Tạo bản đồ nền phẳng màu Đỏ - Cam - Vàng theo phong cách ảnh mẫu
all_countries_sample = ["VNM", "USA", "CHN", "JPN", "DEU", "GBR", "SGP", "CHE"]
intensities_sample = [95, 40, 80, 75, 70, 65, 85, 90]

fig.add_trace(go.Choropleth(
    locations = all_countries_sample,
    z = intensities_sample,
    locationmode = "ISO-3",
    colorscale = [
        [0.0, "#d63031"],  # Đỏ rực phẳng (Lớp nền chính của ảnh)
        [0.5, "#e17055"],  # Cam đất (Vùng chuyển tiếp địa hình)
        [1.0, "#fdcb6e"]   # Vàng tươi rực rỡ (Vùng mật độ cao)
    ],
    showscale = False,
    hoverinfo = "none",
    marker_line_color = "rgba(255,255,255,0.2)"
))

# Vẽ điểm nút gốc nước Mỹ
fig.add_trace(go.Scattergeo(
    lon = [us_hq["lon"]], lat = [us_hq["lat"]],
    text = f"⭐ {us_hq['name']}", mode = "markers",
    marker = dict(size=14, color="#ffffff", symbol="star", line=dict(color="#2d3436", width=2))
))

# Vẽ các đường chỉ chạy dây và các điểm nút mạng lưới chằng chịt
for country, data in macro_mesh.items():
    fig.add_trace(go.Scattergeo(lon=[data["lon_c1"]], lat=[data["lat_c1"]], text=f"🏛️ {country}", mode="markers", marker=dict(size=8, color="#2d3436", symbol="square")))
    fig.add_trace(go.Scattergeo(lon=[data["lon_as"]], lat=[data["lat_as"]], text=f"🎯 {data['name_as']}", mode="markers", marker=dict(size=8, color="#ffffff", line=dict(color="#2d3436", width=1.5))))

    # Đường kết nối liên quốc gia
    cross_lon = [us_hq["lon"], data["lon_c1"]] if flow_type == "INVESTMENT" else [data["lon_c1"], us_hq["lon"]]
    cross_lat = [us_hq["lat"], data["lat_c1"]] if flow_type == "INVESTMENT" else [data["lat_c1"], us_hq["lat"]]
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=1, color=base_color), hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=cross_lon, lat=cross_lat, mode="lines", line=dict(width=3, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

    # Đường dây phân rã nội địa
    local_lon = [data["lon_c1"], data["lon_ag"], data["lon_as"]] if flow_type == "INVESTMENT" else [data["lon_as"], data["lon_ag"], data["lon_c1"]]
    local_lat = [data["lat_c1"], data["lat_ag"], data["lat_as"]] if flow_type == "INVESTMENT" else [data["lat_as"], data["lat_ag"], data["lat_c1"]]
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=1, color=base_color), hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=local_lon, lat=local_lat, mode="lines", line=dict(width=3.5, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

# ĐÃ NÂNG CẤP TIÊU CHÍ: Khóa trục dọc, chỉ cho cuộn ngang và phóng to thu nhỏ
fig.update_layout(
    showlegend = False,
    height = 700,
    margin = dict(l=0, r=0, t=10, b=0),
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor = "rgba(0,0,0,0)",
    dragmode = "pan" # Ép buộc chế độ chuột luôn kéo trượt (Pan) thay vì quét hộp chọn
)

fig.update_geos(
    scope = "world",
    projection_type = "natural earth", # Phép chiếu phẳng 2D chuẩn quốc tế
    showland = True, landcolor = "#dfe6e9",
    showocean = True, oceancolor = "#f5f6fa",
    showcountries = True, countrycolor = "#ffffff",
    # Tham số cốt lõi khóa trục dọc: Cố định giới hạn vĩ độ (Latitude) để không dịch lên xuống
    lataxis = dict(range=[-50, 70], showgrid=False),
    # Giữ nguyên trục kinh độ tự do để người dùng cuộn ngang thoải mái quanh trái đất
    lonaxis = dict(showgrid=False)
)

# 5. HIỂN THỊ BẢN ĐỒ GÓC RỘNG TO LÊN TRÊN CÙNG MÀN HÌNH
st.plotly_chart(fig, use_container_width=True)

# 6. KHU VỰC THÔNG TIN TERMINAL PHÍA DƯỚI
col_text, col_stats = st.columns(2)

with col_text:
    st.markdown("### 🎚️ Trung tâm Phân tích Luồng Tín hiệu")
    st.markdown(f"Trạng thái mạng lưới: <span class='status-badge' style='background-color: {badge_bg};'>{status_label}</span>", unsafe_allow_html=True)
    st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Cơ chế hoạt họa nhịp dây trên nền phẳng:")
    if flow_type == "INVESTMENT":
        st.write("🟢 **MÀU XANH LÁ CHẠY TOẢ RA NGOÀI (Outflow):** Chỉ số sức mạnh USD suy yếu. Dòng tiền từ nước Mỹ bắn các luồng hạt sáng chạy liên tục ra các quốc gia có mô hình bản đồ Đỏ - Vàng để gom mua cổ phiếu, tiền kỹ thuật số và đẩy mạnh giải ngân sản xuất.")
    else:
        st.write("🔴 **MÀU ĐỎ CHẠY CUỘN VÀO TRONG (Inflow):** Khủng hoảng tài chính kích hoạt. Toàn bộ các sợi dây rủi ro bị đóng băng. Tiền tệ từ các hạ tầng tài sản nội địa chạy dồn dập ngược dòng theo dải xung đỏ, xuyên biên giới để rút vốn an toàn về nước Mỹ.")
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
