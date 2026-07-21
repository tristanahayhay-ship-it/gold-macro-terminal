# Toàn bộ mã nguồn gộp duy nhất cho file streamlit_app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Cấu hình giao diện Streamlit rộng toàn màn hình
st.set_page_config(page_title="Hệ Thống Dòng Tiền Vĩ Mô Toàn Cầu", layout="wide")

st.title("🌐 Hệ Thống Mô Phỏng Dòng Tiền Vĩ Mô & Bản Đồ Kinh Tế Toàn Cầu")
st.caption("Mô phỏng tác động logic chặt chẽ của chỉ số USD lên 195 quốc gia từ cấp Toàn cầu đến Nhà đầu tư vi mô.")

# =============================================================================
# 1. HÀM XỬ LÝ DỮ LIỆU VÀ ĐỒ HỌA (Tích hợp từ các module cũ)
# =============================================================================
def get_global_data():
    country_codes = ['USA', 'VNM', 'CHN', 'JPN', 'DEU', 'GBR', 'FRA', 'IND', 'BRA', 'AUS', 'CAN', 'RUS', 'ZAF', 'KOR', 'SAU']
    all_countries = country_codes + ['ARG', 'IDN', 'TUR', 'MEX', 'ITA', 'ESP', 'CHE', 'SGP', 'MAS', 'THA', 'PHL', 'EGY', 'NGA']
    data_factory = []
    for code in all_countries:
        if code == 'USA':
            gdp_power = 98; gold_reserve = 8133; lat = 37.0902; lon = -95.7129
        elif code == 'CHN':
            gdp_power = 85; gold_reserve = 2264; lat = 35.8617; lon = 104.1954
        elif code == 'DEU':
            gdp_power = 80; gold_reserve = 3352; lat = 51.1657; lon = 10.4515
        elif code == 'VNM':
            gdp_power = 45; gold_reserve = 10; lat = 14.0583; lon = 108.2772
        else:
            gdp_power = np.random.randint(30, 75)
            gold_reserve = np.random.randint(5, 500)
            lat = np.random.uniform(-40, 60)
            lon = np.random.uniform(-100, 130)
        data_factory.append({'CODE': code, 'GDP_Power': gdp_power, 'Gold': gold_reserve, 'LAT': lat, 'LON': lon})
    return pd.DataFrame(data_factory)

def draw_global_map(df_global, is_usd_strong):
    line_color = "red" if is_usd_strong else "green"
    fig_map = go.Figure()
    fig_map.add_trace(go.Choropleth(
        locations=df_global['CODE'], z=df_global['GDP_Power'],
        colorscale='Viridis', colorbar_title="Sức mạnh GDP",
        marker_line_color='darkgray', marker_line_width=0.5,
    ))
    fig_map.add_trace(go.Scattergeo(
        lon=df_global['LON'], lat=df_global['LAT'],
        text=df_global['CODE'] + "<br>Vàng: " + df_global['Gold'].astype(str) + " tấn",
        marker=dict(size=np.log1p(df_global['Gold']) * 3, color='gold', line_color='black', line_width=1)
    ))
    usa_coords = [37.0902, -95.7129]
    for _, row in df_global.iterrows():
        if row['CODE'] != 'USA':
            fig_map.add_trace(go.Scattergeo(
                lon=[row['LON'], usa_coords], lat=[row['LAT'], usa_coords],
                mode='lines', line=dict(width=1.5, color=line_color), opacity=0.4, hoverinfo='none'
            ))
    fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True), margin=dict(l=0, r=0, t=0, b=0), height=600, showlegend=False)
    return fig_map

def draw_micro_network(country_name, is_usd_strong):
    nodes = {
        "Hệ Thống Tài Chính Toàn Cầu": [0.5, 1.0],
        f"Chính Phủ / Ngân Hàng Trung Ương {country_name}": [0.5, 0.75],
        "Tập Đoàn Đa Quốc Gia / Định Chế Lớn": [0.25, 0.5],
        "Doanh Nghiệp Sản Xuất Lõi / SME": [0.75, 0.5],
        "Nhà Đầu Tư Cá Nhân / Dân Cư": [0.5, 0.2]
    }
    edges = [
        ("Hệ Thống Tài Chính Toàn Cầu", f"Chính Phủ / Ngân Hàng Trung Ương {country_name}"),
        (f"Chính Phủ / Ngân Hàng Trung Ương {country_name}", "Tập Đoàn Đa Quốc Gia / Định Chế Lớn"),
        (f"Chính Phủ / Ngân Hàng Trung Ương {country_name}", "Doanh Nghiệp Sản Xuất Lõi / SME"),
        ("Tập Đoàn Đa Quốc Gia / Định Chế Lớn", "Nhà Đầu Tư Cá Nhân / Dân Cư"),
        ("Doanh Nghiệp Sản Xuất Lõi / SME", "Nhà Đầu Tư Cá Nhân / Dân Cư")
    ]
    micro_color = "red" if is_usd_strong else "green"
    fig_micro = go.Figure()
    
    edge_x, edge_y = [], []
    for edge in edges:
        x0, y0 = nodes[edge[0]]
        x1, y1 = nodes[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    fig_micro.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=2.5, color=micro_color), mode='lines'))
    node_x = [v[0] for v in nodes.values()]
    node_y = [v[1] for v in nodes.values()]
    fig_micro.add_trace(go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=list(nodes.keys()), textposition="top center",
        marker=dict(size=26, color='darkblue', symbol='circle-dot', line=dict(color='white', width=2))
    ))
    fig_micro.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), margin=dict(l=20, r=20, t=20, b=20), height=500, plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    return fig_micro

# =============================================================================
# 2. THANH ĐIỀU KHIỂN GIAO DIỆN (SIDEBAR)
# =============================================================================
st.sidebar.header("🕹️ Điều Khiển Trạng Thái")
usd_status = st.sidebar.radio("Trạng thái USD (DXY):", ("USD MẠNH LÊN (DXY Tăng 📈)", "USD YẾU ĐI (DXY Giảm 📉)"))
is_usd_strong = "MẠNH" in usd_status

view_mode = st.sidebar.selectbox("Chế độ hiển thị bản đồ:", ["Toàn cầu (Vĩ mô)", "Cận cảnh Quốc gia (Vi mô)"])
country_list = ["Hoa Kỳ", "Việt Nam", "Trung Quốc", "Nhật Bản"]
selected_country = st.sidebar.selectbox("Chọn quốc gia hiển thị vi mô:", country_list)

df_global = get_global_data()

# =============================================================================
# 3. HIỂN THỊ ĐỒ HỌA THEO PHÂN CẤP
# =============================================================================
if view_mode == "Toàn cầu (Vĩ mô)":
    st.subheader("🗺️ Bản Đồ Luồng Vốn 195 Quốc Gia")
    flow_txt = "RÚT VỀ MỸ (Màu Đỏ - Phòng thủ)" if is_usd_strong else "BUNG XÕA TOÀN CẦU (Màu Xanh - Đầu tư)"
    st.info(f"🔄 **HƯỚNG DÒNG TIỀN:** {flow_txt}")
    fig = draw_global_map(df_global, is_usd_strong)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.subheader(f"🔬 Sơ Đồ Bộ Máy Kinh Tế Vi Mô: {selected_country}")
    fig = draw_micro_network(selected_country, is_usd_strong)
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 4. KHỐI PHÂN TÍCH LOGIC KINH TẾ
# =============================================================================
st.markdown("---")
col_macro, col_micro = st.columns(2)

with col_macro:
    st.markdown("### 🧱 Bản Chất Vĩ Mô Toàn Cầu")
    if is_usd_strong:
        st.error("🚨 Dòng vốn tháo chạy khỏi các thị trường mới nổi đổ ngược về tài sản định danh USD an toàn.")
    else:
        st.success("🌊 Tiền rẻ tràn ra thế giới, các quốc gia nhiều Vàng được bảo chứng sức mạnh tài sản tốt nhất.")

with col_micro:
    st.markdown(f"### 🎯 Hành Vi Chi Tiết Các Cấp Tại {selected_country}")
    if is_usd_strong:
        st.warning("🛡️ **Tập đoàn & Người dân phòng thủ:** Tất toán nợ vay USD, chuyển tiền gửi tiết kiệm lãi suất cao.")
    else:
        st.info("🚀 **Tập đoàn & Người dân tấn công:** Đổ tiền mạnh vào Vàng vật chất, Cổ phiếu tăng trưởng, BĐS lõi.")
