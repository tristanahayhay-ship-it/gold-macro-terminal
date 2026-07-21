import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Bản Đồ Thế Giới 4D")

st.title("🌐 Quả Cầu Thế Giới 4D Tương Tác Cao Cấp")
st.write("Di chuột để xoay 3D, phóng to thu nhỏ và kéo thanh trượt bên dưới để thay đổi thời gian (Trục 4D).")

# 1. Tạo dữ liệu giả lập theo thời gian (4D) cho các quốc gia lớn
@st.cache_data
def generate_4d_data():
    countries = ['VNM', 'USA', 'CHN', 'RUS', 'BRA', 'AUS', 'IND', 'GBR', 'FRA', 'ZAF', 'CAN', 'JPN']
    lats = [14.0583, 37.0902, 35.8617, 61.5240, -14.2350, -25.2744, 20.5937, 55.3781, 46.2276, -30.5595, 56.1304, 36.2048]
    lons = [108.2772, -95.7129, 104.1954, 105.3188, -51.9253, 133.7751, 78.9629, -3.4360, 2.2137, 22.9375, -106.3468, 138.2529]
    names = ['Việt Nam', 'Mỹ', 'Trung Quốc', 'Nga', 'Brazil', 'Úc', 'Ấn Độ', 'Anh', 'Pháp', 'Nam Phi', 'Canada', 'Nhật Bản']
    
    data_list = []
    # Tạo dữ liệu chạy từ năm 2021 đến năm 2026 (Trục thời gian thứ 4)
    for year in range(2021, 2027):
        for i in range(len(countries)):
            # Giá trị phát sáng ngẫu nhiên tăng dần theo năm
            value = np.random.randint(10, 100) + (year - 2021) * 15
            data_list.append({
                'Năm': year,
                'Mã quốc gia': countries[i],
                'Tên': names[i],
                'Vĩ độ': lats[i],
                'Kinh độ': lons[i],
                'Chỉ số phát sáng': value
            })
    return pd.DataFrame(data_list)

df_4d = generate_4d_data()

# 2. Tạo bộ lọc thời gian trực quan (Thanh trượt 4D)
selected_year = st.slider("📅 Chọn mốc thời gian (Trục 4D):", min_value=2021, max_value=2026, value=2026, step=1)

# Lọc dữ liệu theo năm đã chọn
df_filtered = df_4d[df_4d['Năm'] == selected_year]

# 3. Dựng đồ họa quả cầu Trái Đất 3D rực rỡ trên nền tối
fig = go.Figure()

# Thêm lớp dữ liệu các điểm phát sáng dạng bong bóng 3D (Scattergeo)
fig.add_trace(go.Scattergeo(
    lon = df_filtered['Kinh độ'],
    lat = df_filtered['Vĩ độ'],
    text = df_filtered['Tên'] + "<br>Chỉ số: " + df_filtered['Chỉ số phát sáng'].astype(str),
    mode = 'markers',
    marker = dict(
        size = df_filtered['Chỉ số phát sáng'] / 4, # Kích thước hạt phát sáng
        opacity = 0.85,
        reversescale = False,
        autocolorscale = False,
        symbol = 'circle',
        line = dict(width=1, color='rgba(255, 255, 255, 0.5)'),
        colorscale = 'Viridis', # Dải màu dạ quang rực rỡ (Tím - Xanh - Vàng)
        cmin = df_4d['Chỉ số phát sáng'].min(),
        cmax = df_4d['Chỉ số phát sáng'].max(),
        color = df_filtered['Chỉ số phát sáng'],
        colorbar = dict(title="Cường độ 4D", thickness=15)
    )
))

# 4. Thiết lập giao diện tối và hiệu ứng hiển thị quả cầu
fig.update_layout(
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = '#11151c',      # Màu lục địa đen sâu cực đẹp
        oceancolor = '#0b0c10',     # Màu đại dương đen tuyền
        countrycolor = '#1f2833',   # Đường biên giới các nước màu xám công nghệ
        lakecolor = '#0b0c10',
        projection_type = 'orthographic', # Ép bản đồ phẳng thành quả cầu Trái Đất 3D quay được
        lonaxis = dict(showgrid=True, gridcolor='#1f2833'),
        lataxis = dict(showgrid=True, gridcolor='#1f2833')
    ),
    paper_bgcolor = '#0b0c10', # Nền bao quanh màu đen đồng bộ
    margin = dict(l=0, r=0, t=0, b=0),
    height = 700
)

# Render đồ họa lên Streamlit
st.plotly_chart(fig, use_container_width=True)
