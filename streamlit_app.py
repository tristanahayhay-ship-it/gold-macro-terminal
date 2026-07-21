import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Mô phỏng Vũ Trụ 4D")

st.title("🌌 Quả Cầu Trái Đất Nhìn Từ Không Gian Vũ Trụ")
st.write("Mô phỏng hiệu ứng bầu trời sao, khí quyển và dữ liệu năng lượng 4D.")

# 1. Tạo dữ liệu giả lập theo thời gian (4D) cho các quốc gia lớn
@st.cache_data
def generate_4d_data():
    countries = ['VNM', 'USA', 'CHN', 'RUS', 'BRA', 'AUS', 'IND', 'GBR', 'FRA', 'ZAF', 'CAN', 'JPN']
    lats = [14.0583, 37.0902, 35.8617, 61.5240, -14.2350, -25.2744, 20.5937, 55.3781, 46.2276, -30.5595, 56.1304, 36.2048]
    lons = [108.2772, -95.7129, 104.1954, 105.3188, -51.9253, 133.7751, 78.9629, -3.4360, 2.2137, 22.9375, -106.3468, 138.2529]
    names = ['Việt Nam', 'Mỹ', 'Trung Quốc', 'Nga', 'Brazil', 'Úc', 'Ấn Độ', 'Anh', 'Pháp', 'Nam Phi', 'Canada', 'Nhật Bản']
    
    data_list = []
    for year in range(2021, 2027):
        for i in range(len(countries)):
            value = np.random.randint(20, 100) + (year - 2021) * 12
            data_list.append({
                'Năm': year, 'Mã quốc gia': countries[i], 'Tên': names[i],
                'Vĩ độ': lats[i], 'Kinh độ': lons[i], 'Chỉ số phát sáng': value
            })
    return pd.DataFrame(data_list)

df_4d = generate_4d_data()

# Bộ lọc thời gian trực quan (Thanh trượt 4D)
selected_year = st.slider("📅 Trục thời gian vũ trụ (4D):", min_value=2021, max_value=2026, value=2026, step=1)
df_filtered = df_4d[df_4d['Năm'] == selected_year]

# 2. Khởi tạo biểu đồ đồ họa 3D
fig = go.Figure()

# --- TÍNH NĂNG MỚI 1: TẠO HIỆU ỨNG KHÍ QUYỂN PHÁT SÁNG BAO QUANH TRÁI ĐẤT ---
# Vẽ một đường viền tròn dạ quang (Cyan/Blue) bao quanh rìa quả địa cầu làm tầng khí quyển
theta = np.linspace(0, 2*np.pi, 100)
fig.add_trace(go.Scattergeo(
    lon = 100 * np.cos(theta), # Định vị vòng tròn bao quanh trục quả cầu
    lat = 40 * np.sin(theta),
    mode = 'lines',
    line = dict(width=3, color='rgba(0, 238, 255, 0.4)'), # Màu xanh khí quyển phát sáng nhẹ
    hoverinfo = 'none'
))

# 3. Thêm lớp dữ liệu các điểm hạt năng lượng rực rỡ (Dải màu Plasma từ Xanh - Tím - Vàng chanh)
fig.add_trace(go.Scattergeo(
    lon = df_filtered['Kinh độ'],
    lat = df_filtered['Vĩ độ'],
    text = df_filtered['Tên'] + "<br>Cường độ: " + df_filtered['Chỉ số phát sáng'].astype(str) + " GW",
    mode = 'markers',
    marker = dict(
        size = df_filtered['Chỉ số phát sáng'] / 3.2, 
        opacity = 0.9,
        reversescale = False,
        autocolorscale = False,
        symbol = 'circle',
        line = dict(width=1.5, color='rgba(255, 255, 255, 0.8)'),
        colorscale = 'Plasma', # Đổi sang hệ màu Plasma mang hơi hướng năng lượng vũ trụ
        cmin = df_4d['Chỉ số phát sáng'].min(),
        cmax = df_4d['Chỉ số phát sáng'].max(),
        color = df_filtered['Chỉ số phát sáng'],
        showscale = False
    )
))

# --- TÍNH NĂNG MỚI 2: MÔ PHỎNG NỀN KHÔNG GIAN VŨ TRỤ THỰC TẾ ---
fig.update_layout(
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.8,
        landcolor = '#0d1117',      # Màu lục địa đổi sang Đen Xám góc cạnh vệ tinh
        oceancolor = '#020408',     # Màu đại dương Đen Huyền Bí sâu thẳm
        countrycolor = '#1f2937',   # Biên giới các nước màu xám đen mờ
        lakecolor = '#020408',
        projection_type = 'orthographic', 
        # Cấu hình lưới Kinh - Vĩ độ mảnh phát sáng xanh mờ như màn hình rada vũ trụ
        lonaxis = dict(showgrid=True, gridcolor='rgba(0, 238, 255, 0.08)', gridwidth=0.5),
        lataxis = dict(showgrid=True, gridcolor='rgba(0, 238, 255, 0.08)', gridwidth=0.5)
    ),
    # Dùng ảnh nền mô phỏng các vì sao lấp lánh (Starfield) làm background bao quanh quả cầu
    images=[dict(
        source="https://unsplash.com", # Ảnh vũ trụ nhiều sao mịn nền tối
        xref="paper", yref="paper",
        x=0, y=1,
        sizex=1, sizey=1,
        xanchor="left", yanchor="top",
        sizing="stretch",
        opacity=0.6, # Độ mờ của nền sao để giữ bản đồ sắc nét
        layer="below" # Đẩy nền sao xuống dưới cùng bản đồ
    )],
    paper_bgcolor = '#020408', # Nền bao quanh tổng thể tiệp màu với không gian
    showlegend = False,
    margin = dict(l=0, r=0, t=0, b=0),
    height = 850
)

# Render đồ họa lên giao diện Streamlit
st.plotly_chart(fig, use_container_width=True)
