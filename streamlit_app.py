import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

# 1. Cấu hình trang hiển thị giao diện tối toàn diện
st.set_page_config(layout="wide", page_title="Bản Đồ Đồ Họa Cao Cấp")

st.title("📊 Bản Đồ Đồ Họa 3D Đậm Chất Công Nghệ")
st.write("Giao diện tối kết hợp hiệu ứng Neon phát sáng sắc nét.")

# 2. Khởi tạo dữ liệu giả lập (Vị trí các điểm sáng đồ họa)
@st.cache_data
def generate_data():
    # Tạo ngẫu nhiên 500 điểm xung quanh một khu vực trung tâm
    chart_data = pd.DataFrame(
        np.random.randn(500, 2) / [50, 50] + [21.0285, 105.8542], # Tọa độ mặc định: Hà Nội
        columns=['lat', 'lon']
    )
    # Thêm cột giá trị độ cao và màu sắc sắc nét (Đỏ/Cam/Vàng Neon)
    chart_data['elevation'] = np.random.randint(100, 2000, size=500)
    return chart_data

df = generate_data()

# 3. Thiết lập lớp bản đồ 3D (Hexagon hoặc Column Layer)
layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position="[lon, lat]",
    radius=150,
    elevation_scale=1,
    elevation_range=[0, 3000],
    get_elevation="elevation",
    pickable=True,
    extruded=True,
    # Dải màu sắc phát sáng cực đẹp từ Tím, Hồng đến Cam rực
    color_range=[
        [63, 0, 128],
        [120, 0, 180],
        [200, 0, 150],
        [255, 0, 100],
        [255, 100, 50],
        [255, 200, 0]
    ],
)

# 4. Cấu hình góc nhìn và Giao diện nền tối (mapbox_style)
view_state = pdk.ViewState(
    latitude=21.0285,
    longitude=105.8542,
    zoom=11,
    pitch=50, # Độ nghiêng tạo góc nhìn 3D đồ họa
    bearing=30
)

# Render bản đồ lên giao diện Streamlit với nền bản đồ tối của CartoDB
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Hoặc dùng chuỗi không cần token: "https://cartocdn.com"
    tooltip={"text": "Mật độ: {count}\nĐộ cao đồ họa: {elevation}m"}
)

st.pydeck_chart(r)
