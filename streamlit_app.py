import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. CẤU HÌNH GIAO DIỆN TERMINAL TỐI (DARK-MODE)
st.set_page_config(
    page_title="Gold Macro Terminal Pro",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #07090e; color: #e1e6eb; }
    .terminal-card { background-color: #11141c; padding: 15px; border-radius: 8px; border: 1px solid #1f2633; margin-bottom: 12px; }
    .status-badge { font-weight: bold; padding: 4px 8px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("🕸️ GOLD MACRO-MICRO TERMINAL (COMPLETE EDITION)")
st.subheader("Hệ thống Định vị Mạng lưới Dòng chảy Tài chính 195 Quốc gia")
st.markdown("---")

# 2. BỘ ĐIỀU KHIỂN SIDEBAR TƯƠNG TÁC
st.sidebar.header("🎛️ BỘ ĐIỀU KHIỂN TRỤC VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "1. Chọn Trạng thái Chỉ số Dòng tiền:",
    ["Đồng USD giảm - Kích hoạt ĐẦU TƯ TOÀN CẦU (MÀU XANH CHẠY OUT)", 
     "Đồng USD tăng - Tháo chạy gom tài sản TRÚ ẨN (MÀU ĐỎ CHẠY IN)"]
)

base_countries = ["Việt Nam", "Mỹ (United States)", "Thụy Sĩ (Switzerland)", "Nhật Bản", "Trung Quốc", "Đức", "Anh", "Singapore"]
all_195_countries = base_countries + [f"Quốc gia mẫu thứ {i}" for i in range(9, 196)]

selected_country = st.sidebar.selectbox("2. Chọn Quốc gia để ZOOM SÂU nội địa:", all_195_countries)
selected_agent = st.sidebar.radio("3. Tiêu điểm Chủ thể Vi mô (Agent-Layer):", ["Tất cả chủ thể cùng chạy", "Nhà đầu tư Cá nhân (Retail)", "Khối Tập đoàn lớn (Corporate)"])
total_capital = st.sidebar.number_input("4. Quy mô dòng vốn giả lập (USD):", min_value=1000000, value=100000000, step=1000000, format="%d")

# 3. THUẬT TOÁN ĐIỀU KHIỂN HOẠT HỌA "CHẠY CHẠY" & MÀU SẮC
if "MÀU XANH" in market_phase:
    flow_type = "INVESTMENT"
    pulse_color = "#2ecc71"
    base_color = "rgba(46, 204, 113, 0.15)"
    dash_pattern = "4 4 4 4"
    badge_style = "background-color: rgba(46, 204, 113, 0.2); color: #2ecc71;"
    status_label = "MỞ RỘNG VỐN ĐẦU TƯ (RISK-ON)"
else:
    flow_type = "SAFE_HAVEN"
    pulse_color = "#e74c3c"
    base_color = "rgba(231, 76, 60, 0.15)"
    dash_pattern = "8 4 8 4"
    badge_style = "background-color: rgba(231, 76, 60, 0.2); color: #e74c3c;"
    status_label = "THÁO VỐN PHÒNG THỦ (RISK-OFF)"
# 4. CƠ SỞ DỮ LIỆU ĐỘNG PHÂN RÃ THEO CHỦ THỂ & TÀI SẢN NỘI ĐỊA
if selected_country == "Việt Nam":
    geo_scope = "asia"
    center_lat, center_lon = 15.8, 107.5
    level_1 = {"name": "Ngân hàng Nhà nước (SBV) & Bộ Tài chính Việt Nam", "lat": 21.0285, "lon": 105.8342}
    agents_data = {
        "Nhà đầu tư Cá nhân (Retail)": {"name": "Hộ gia đình & Cá nhân đầu tư VN", "lat": 16.0470, "lon": 108.2205},
        "Khối Tập đoàn lớn (Corporate)": {"name": "Tập đoàn kinh tế & Doanh nghiệp nội địa", "lat": 10.7769, "lon": 106.7018}
    }
    assets_data = {
        "Cổ phiếu Tăng trưởng": {"name": "Sàn HOSE (Cổ phiếu Tăng trưởng)", "lat": 10.8231, "lon": 106.6297, "type": "INVESTMENT"},
        "Bất động sản Đầu cơ": {"name": "Đất nền vùng ven & Dự án Đô thị", "lat": 11.5424, "lon": 106.9407, "type": "INVESTMENT"},
        "Thị trường Crypto": {"name": "Sàn Tài sản số (Crypto Exchange)", "lat": 10.7626, "lon": 106.6602, "type": "INVESTMENT"},
        "Vàng miếng & Nhẫn": {"name": "Đại lý Vàng vật chất (SJC/Nhẫn 9999)", "lat": 21.0333, "lon": 105.8500, "type": "SAFE_HAVEN"},
        "Tiền mặt & Tiết kiệm": {"name": "H型thống Ngân hàng Thương mại (Tiết kiệm VND)", "lat": 21.0167, "lon": 105.8167, "type": "SAFE_HAVEN"},
        "Trái phiếu Chính phủ": {"name": "Sàn Giao dịch Trái phiếu Kho bạc Nhà nước", "lat": 21.0245, "lon": 105.8412, "type": "SAFE_HAVEN"}
    }
elif selected_country == "Mỹ (United States)":
    geo_scope = "north america"
    center_lat, center_lon = 37.0, -95.7
    level_1 = {"name": "Fed (Cục Dự trữ Liên bang) & US Treasury", "lat": 38.9072, "lon": -77.0369}
    agents_data = {
        "Nhà đầu tư Cá nhân (Retail)": {"name": "Cộng đồng nhỏ lẻ Robinhood Traders", "lat": 41.8781, "lon": -87.6298},
        "Khối Tập đoàn lớn (Corporate)": {"name": "Các tập đoàn S&P 500 & Định chế tài chính", "lat": 34.0522, "lon": -118.2437}
    }
    assets_data = {
        "Cổ phiếu Tăng trưởng": {"name": "Sàn NYSE / NASDAQ (Cổ phiếu Công nghệ)", "lat": 40.7128, "lon": -74.0060, "type": "INVESTMENT"},
        "Bất động sản Đầu cơ": {"name": "BĐS Thương mại (US Commercial REITs)", "lat": 32.7767, "lon": -96.7970, "type": "INVESTMENT"},
        "Thị trường Crypto": {"name": "Quỹ ETF Bitcoin & Coinbase Pro", "lat": 37.7749, "lon": -122.4194, "type": "INVESTMENT"},
        "Vàng miếng & Nhẫn": {"name": "Quỹ Tín thác Vàng quốc tế (GLD ETF)", "lat": 42.3601, "lon": -71.0589, "type": "SAFE_HAVEN"},
        "Tiền mặt & Tiết kiệm": {"name": "Tài khoản Tiền gửi Đô la Mỹ (USD Cash)", "lat": 39.9526, "lon": -75.1652, "type": "SAFE_HAVEN"},
        "Trái phiếu Chính phủ": {"name": "Két an toàn Trái phiếu Chính phủ Mỹ (US Treasuries)", "lat": 38.8951, "lon": -77.0364, "type": "SAFE_HAVEN"}
    }
else:
    geo_scope = "world"
    center_lat, center_lon = 20.0, 0.0
    level_1 = {"name": f"Hội đồng Vĩ mô Thượng tầng {selected_country}", "lat": 20.0, "lon": 0.0}
    agents_data = {
        "Nhà đầu tư Cá nhân (Retail)": {"name": f"Khối Cá nhân {selected_country}", "lat": 15.0, "lon": -10.0},
        "Khối Tập đoàn lớn (Corporate)": {"name": f"Khối Doanh nghiệp {selected_country}", "lat": 10.0, "lon": 10.0}
    }
    assets_data = {
        "Cổ phiếu Tăng trưởng": {"name": f"Thị trường tài sản {selected_country}", "lat": 5.0, "lon": 5.0, "type": "INVESTMENT"},
        "Bất động sản Đầu cơ": {"name": f"BĐS Địa phương {selected_country}", "lat": 5.0, "lon": -5.0, "type": "INVESTMENT"},
        "Thị trường Crypto": {"name": "Ví lạnh lưu trữ Crypto kỹ thuật số", "lat": 0.0, "lon": 0.0, "type": "INVESTMENT"},
        "Vàng miếng & Nhẫn": {"name": f"Kho dự trữ Vàng {selected_country}", "lat": 25.0, "lon": 5.0, "type": "SAFE_HAVEN"},
        "Tiền mặt & Tiết kiệm": {"name": f"Ngân hàng nội tệ {selected_country}", "lat": 25.0, "lon": -5.0, "type": "SAFE_HAVEN"},
        "Trái phiếu Chính phủ": {"name": f"Trái phiếu nội bang {selected_country}", "lat": 30.0, "lon": 0.0, "type": "SAFE_HAVEN"}
    }

# 5. ĐỒ HỌA MẠNG LƯỚI BẢN ĐỒ THỜI GIAN THỰC (MAP ENGINE)
fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon = [level_1["lon"]], lat = [level_1["lat"]],
    text = f"🏛️ CẤP 1: {level_1['name']}", mode = "markers+text", textposition = "top center",
    marker = dict(size=14, color="#1abc9c", symbol="square", line=dict(color="#fff", width=1.5))
))

active_agents = list(agents_data.keys()) if selected_agent == "Tất cả chủ thể cùng chạy" else [selected_agent]

for agent_key in active_agents:
    agent = agents_data[agent_key]
    fig.add_trace(go.Scattergeo(
        lon = [agent["lon"]], lat = [agent["lat"]],
        text = f"👤 CẤP 2: {agent['name']}", mode = "markers+text", textposition = "bottom center",
        marker = dict(size=12, color="#f39c12", symbol="diamond", line=dict(color="#fff", width=1))
    ))

for asset_key, asset in assets_data.items():
    is_active = (flow_type == asset["type"])
    node_size = 11 if is_active else 6
    node_col = pulse_color if is_active else "#57606f"
    fig.add_trace(go.Scattergeo(
        lon = [asset["lon"]], lat = [asset["lat"]],
        text = f"🎯 CẤP 3: {asset['name']}", mode = "markers+text", textposition = "top right",
        marker = dict(size=node_size, color=node_col, symbol="circle", line=dict(color="#fff", width=0.5))
    ))

for agent_key in active_agents:
    agent = agents_data[agent_key]
    l1_l2_lon = [level_1["lon"], agent["lon"]] if flow_type == "INVESTMENT" else [agent["lon"], level_1["lon"]]
    l1_l2_lat = [level_1["lat"], agent["lat"]] if flow_type == "INVESTMENT" else [agent["lat"], level_1["lat"]]
    
    fig.add_trace(go.Scattergeo(lon=l1_l2_lon, lat=l1_l2_lat, mode="lines", line=dict(width=1, color=base_color), hoverinfo="none"))
    fig.add_trace(go.Scattergeo(lon=l1_l2_lon, lat=l1_l2_lat, mode="lines", line=dict(width=2.5, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

    for asset_key, asset in assets_data.items():
        if asset["type"] == flow_type:
            path_lon = [agent["lon"], asset["lon"]] if flow_type == "INVESTMENT" else [asset["lon"], agent["lon"]]
            path_lat = [agent["lat"], asset["lat"]] if flow_type == "INVESTMENT" else [agent["lat"], asset["lat"]]
            fig.add_trace(go.Scattergeo(lon=path_lon, lat=path_lat, mode="lines", line=dict(width=1.5, color=base_color), hoverinfo="none"))
            fig.add_trace(go.Scattergeo(lon=path_lon, lat=path_lat, mode="lines", line=dict(width=3.5, color=pulse_color, dash=dash_pattern), hoverinfo="none"))

fig.update_layout(showlegend = False, height = 600, margin = dict(l=0, r=0, t=0, b=0))

fig.update_geos(
    scope = geo_scope, showland = True, landcolor = "#0f131a",
    countrycolor = "#232b38", showcountries = True, showocean = True, oceancolor = "#05070a",
    projection_type = "mercator" if geo_scope != "world" else "natural earth"
)
# 6. HIỂN THỊ BỐ CỤC CHUYÊN NGHIỆP TRÊN WEB DASHBOARD
col_map_layer, col_terminal_panel = st.columns(2)

with col_map_layer:
    st.plotly_chart(fig, use_container_width=True)

with col_terminal_panel:
    st.markdown("### 🎚️ Trung tâm Phân tích Luồng tín hiệu")
    st.markdown(f"Hệ thống: <span class='status-badge' style='{badge_style}'>{status_label}</span>", unsafe_allow_html=True)
    st.write(f"Tọa độ mục tiêu: **{selected_country.upper()}**")
    
    st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Cơ chế hoạt họa nhịp dây:")
    if flow_type == "INVESTMENT":
        st.write("🟢 **Đường chỉ màu XANH LÁ liền mạch đang CHẠY RA NGOÀI (Outflow):** Thể hiện trạng thái USD giảm nhiệt, lãi suất nới lỏng. Dòng tiền từ đầu não Thượng tầng bắn luồng xung lực xuống các Chủ thể Vi mô. Từ đây, dòng tiền giải ngân của Cá nhân và Tập đoàn tạo thành các dải hạt sáng chạy tốc độ cao đổ thẳng vào các tọa độ Sàn chứng khoán HOSE, sàn Crypto và gom mua Đất nền vùng ven để đầu tư sinh lời.")
    else:
        st.write("🔴 **Đường chỉ màu ĐỎ đứt đoạn đang CUỘN NGƯỢC VÀO TRONG (Inflow):** Thể hiện trạng thái USD tăng mạnh hoặc rủi ro vĩ mô xuất hiện. Trục tài sản rủi ro bị đóng băng. Bạn nhìn thấy rõ các hạt sáng màu đỏ đang chạy co cụm dồn dập kéo ngược dòng từ các tài sản rủi ro về két sắt của Cá nhân và Tập đoàn, sau đó truyền tín hiệu phòng thủ thủ thế thẳng vào Hệ thống đại lý Vàng miếng SJC và tài khoản Tiết kiệm ngân hàng.")
    st.markdown("</div>", unsafe_allow_html=True)

# 7. MA TRẬN ĐỊNH LƯỢNG PHÂN PHỐI DÒNG VỐN
st.markdown("---")
st.markdown("### 🗜️ Ma trận Phân tách chi tiết dòng tiền kết nối vi mô từ Chủ thể đến Tài sản Đích")

active_assets_list = [asset for asset in assets_data.values() if asset["type"] == flow_type]
shares_allocation = [0.50, 0.30, 0.20]

matrix_rows = []
for agent_key in active_agents:
    agent_name = agents_data[agent_key]["name"]
    for asset, pct in zip(active_assets_list, shares_allocation):
        allocated_val = total_capital * pct
        matrix_rows.append({
            "Quốc gia": selected_country,
            "Chủ thể khởi nguồn (Cấp 2)": agent_name,
            "Tín hiệu đường dây": "🟢 CHẠY RA ĐẦU TƯ" if flow_type == "INVESTMENT" else "🔴 RÚT VỀ TRÚ ẨN",
            "Hạ tầng tài sản đích (Cấp 3)": asset["name"],
            "Tỷ lệ xung dòng": f"{pct*100:.0f}%",
            "Quy đổi dòng vốn phân bổ": f"${allocated_val:,.0f} USD"
        })

df_terminal_matrix = pd.DataFrame(matrix_rows)
st.dataframe(df_terminal_matrix, use_container_width=True, hide_index=True)
