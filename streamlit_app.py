import streamlit as st
import pandas as pd
import pydeck as pdk

# Cấu hình trang ứng dụng hiển thị rộng toàn màn hình
st.set_page_config(layout="wide")
st.title("Mạng Lưới Dòng Chảy Kinh Tế Thế Giới")

# 1. Khởi tạo dữ liệu mẫu (Tọa độ các trung tâm kinh tế lớn)
# lat: Vĩ độ, lon: Kinh độ
centers = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Shanghai": {"lat": 31.2304, "lon": 121.4737}
}

# 2. Tạo danh sách các dòng chảy tiền tệ (Kết nối Điểm đầu -> Điểm cuối)
data = [
    # Từ New York đi các nơi
    {"from_name": "New York", "to_name": "London", "flow_value": 500},
    {"from_name": "New York", "to_name": "Tokyo", "flow_value": 400},
    {"from_name": "New York", "to_name": "Shanghai", "flow_value": 600},
    # Từ London đi các nơi
    {"from_name": "London", "to_name": "Singapore", "flow_value": 350},
    {"from_name": "London", "to_name": "Tokyo", "flow_value": 300},
    # Từ Thượng Hải đi các nơi
    {"from_name": "Shanghai", "to_name": "Singapore", "flow_value": 450}
]

# Chuyển đổi cấu trúc dữ liệu sang dạng bảng Pandas DataFrame
df = pd.DataFrame(data)
df["from_lat"] = df["from_name"].map(lambda x: centers[x]["lat"])
df["from_lon"] = df["from_name"].map(lambda x: centers[x]["lon"])
df["to_lat"] = df["to_name"].map(lambda x: centers[x]["lat"])
df["to_lon"] = df["to_name"].map(lambda x: centers[x]["lon"])

# 3. Định nghĩa tầng hiển thị mạng lưới dòng chảy (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    # Định hình màu sắc cho dòng chảy (Đỏ = Điểm đi, Xanh = Điểm đến)
    get_source_color="[255, 0, 128, 200]",
    get_target_color="[0, 255, 255, 200]",
    # Độ dày đường truyền dựa vào giá trị dòng chảy kinh tế
    get_width="flow_value / 100",
    pickable=True,
    auto_highlight=True,
)

# 4. Định nghĩa tầng hiển thị các nút thắt/quốc gia (ScatterplotLayer)
nodes_data = pd.DataFrame([{"name": k, "lat": v["lat"], "lon": v["lon"]} for k, v in centers.items()])
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_data,
    get_position="[lon, lat]",
    get_color="[255, 255, 0, 255]", # Nút tròn màu vàng
    get_radius=200000, # Kích cỡ nút tròn trên bản đồ thế giới
    pickable=True,
)

# 5. Cấu hình góc nhìn bản đồ thế giới mặc định (Cho phép cuộn chuột để zoom to/nhỏ)
view_state = pdk.ViewState(
    latitude=20.0,
    longitude=0.0,
    zoom=1.5, # Độ thu nhỏ để nhìn toàn cảnh thế giới
    pitch=45,  # Góc nghiêng 3D giúp nhìn rõ đường cong dòng chảy
)

# 6. Giao diện hiển thị bản đồ trên Streamlit
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Giao diện tối giúp mạng lưới phát sáng rõ hơn
    tooltip={"text": "Dòng chảy từ: {from_name} -> Đến: {to_name}"}
)

st.pydeck_chart(r)
