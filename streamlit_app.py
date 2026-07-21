import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện Streamlit (Nền đen, chữ trắng) bằng CSS
st.set_page_config(layout="wide", page_title="Mạng Lưới Kinh Tế Toàn Cầu")

st.markdown(
    """
    <style>
    /* Đổi nền của ứng dụng thành màu đen */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Đổi màu tiêu đề thành màu trắng sáng */
    h1 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    /* Tùy chỉnh màu chữ text thông thường */
    p, span, label {
        color: #E0E0E0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mạng Lưới Dòng Chảy Kinh Tế Thế Giới")

# 2. Khởi tạo dữ liệu tọa độ các trung tâm kinh tế lớn
centers = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Shanghai": {"lat": 31.2304, "lon": 121.4737}
}

# 3. Tạo danh sách dữ liệu các dòng chảy tiền tệ
data = [
    {"from_name": "New York", "to_name": "London", "flow_value": 500},
    {"from_name": "New York", "to_name": "Tokyo", "flow_value": 400},
    {"from_name": "New York", "to_name": "Shanghai", "flow_value": 600},
    {"from_name": "London", "to_name": "Singapore", "flow_value": 350},
    {"from_name": "London", "to_name": "Tokyo", "flow_value": 300},
    {"from_name": "Shanghai", "to_name": "Singapore", "flow_value": 450}
]

# Chuyển đổi cấu trúc dữ liệu sang DataFrame
df = pd.DataFrame(data)
df["from_lat"] = df["from_name"].map(lambda x: centers[x]["lat"])
df["from_lon"] = df["from_name"].map(lambda x: centers[x]["lon"])
df["to_lat"] = df["to_name"].map(lambda x: centers[x]["lat"])
df["to_lon"] = df["to_name"].map(lambda x: centers[x]["lon"])

# 4. Định nghĩa tầng mạng lưới dòng chảy kết nối (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    # Màu sắc phát sáng: Hồng chuyển sang Xanh Neon trên nền tối
    get_source_color="[255, 0, 128, 200]",
    get_target_color="[0, 255, 255, 200]",
    get_width="flow_value / 100",
    pickable=True,
    auto_highlight=True,
)

# 5. Định nghĩa các nút thắt quốc gia (ScatterplotLayer)
nodes_data = pd.DataFrame([{"name": k, "lat": v["lat"], "lon": v["lon"]} for k, v in centers.items()])
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_data,
    get_position="[lon, lat]",
    get_color="[255, 215, 0, 255]", # Nút tròn màu vàng kim
    get_radius=200000,
    pickable=True,
)

# 6. Cấu hình góc nhìn bản đồ thế giới mặc định (Cho phép cuộn chuột để zoom)
view_state = pdk.ViewState(
    latitude=30.0,
    longitude=10.0,
    zoom=1.5,
    pitch=45,
)

# 7. Giao diện hiển thị bản đồ Pydeck với bản đồ nền tối miễn phí của CartoDB
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    # SỬA ĐỔI: Dùng bản đồ nền tối mã nguồn mở không cần Token Mapbox
    map_style="https://cartocdn.com",
    tooltip={"text": "Dòng chảy từ: {from_name} -> Đến: {to_name}"}
)

# Hiển thị bản đồ lên ứng dụng
st.pydeck_chart(r)
