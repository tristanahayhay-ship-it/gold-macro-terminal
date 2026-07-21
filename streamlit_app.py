import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Money Flow Network")
st.title("Hệ Thống Mô Phỏng Dòng Chảy Tiền Tệ Toàn Cầu")

# 1. Khởi tạo dữ liệu tọa độ giả lập cho các lục địa/quốc gia
# Pydeck hoạt động rất mạnh trên nền bản đồ không gian thực hoặc tọa độ phẳng
locations = {
    "North_America": [37.0902, -95.7129],
    "Europe": [48.5260, 15.2551],
    "Asia": [34.0479, 100.6197],
    "ASEAN": [0.7893, 113.9213],
    "Vietnam": [14.0583, 108.2772]
}

# 2. Định nghĩa luồng dữ liệu giữa các điểm
# Trạng thái màu: strong_in (Xanh), strong_out (Đỏ), neutral (Vàng)
flow_data = [
    {"from": "Vietnam", "to": "ASEAN", "status": "neutral", "volume": 3},
    {"from": "ASEAN", "to": "Asia", "status": "strong_in", "volume": 5},
    {"from": "Asia", "to": "Europe", "status": "strong_out", "volume": 8},
    {"from": "Europe", "to": "North_America", "status": "strong_in", "volume": 10},
    {"from": "North_America", "to": "Vietnam", "status": "strong_in", "volume": 6},
]

# Quy đổi trạng thái sang mã màu RGBA (Pydeck dùng mảng 4 số từ 0-255)
color_mapping = {
    "strong_in":,    # Xanh lá mềm
    "strong_out":,   # Đỏ
    "neutral": [255, 255, 0, 200]     # Vàng
}

# 3. Xử lý dữ liệu thành DataFrame để nạp vào Pydeck
chart_data = []
for flow in flow_data:
    start = locations[flow["from"]]
    end = locations[flow["to"]]
    color = color_mapping[flow["status"]]
    
    chart_data.append({
        "from_lat": start[0],
        "from_lon": start[1],
        "to_lat": end[0],
        "to_lon": end[1],
        "color": color,
        "width": flow["volume"]
    })

df = pd.DataFrame(chart_data)

# 4. Sử dụng hiệu ứng đường cong động (ArcLayer) trong Pydeck
# Tạo hiệu ứng chuyển động vòm từ điểm này sang điểm khác biểu thị dòng tiền phóng đi
layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width="width",
    pickable=True,
    auto_highlight=True,
)

# 5. Cấu hình góc nhìn bản đồ (Góc nhìn tối để nổi bật các sợi dây màu)
view_state = pdk.ViewState(
    latitude=20.0,
    longitude=30.0,
    zoom=1.5,
    pitch=45
)

# Render bản đồ lên giao diện Streamlit với giao diện nền tối CartoDB
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Hoặc status "light" tùy chọn
    tooltip={"text": "Dòng chảy tài sản liên lục địa"}
)

st.pydeck_chart(r)
