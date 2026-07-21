import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện chuẩn Dark Mode cho Streamlit
st.set_page_config(layout="wide", page_title="Mạng Lưới Kinh Tế Toàn Cầu")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    h1 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    p, span, label {
        color: #E0E0E0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mạng Lưới Dòng Chảy Kinh Tế Thế Giới")

# 2. Tọa độ các trung tâm kinh tế lớn
centers = {
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Shanghai": {"lat": 31.2304, "lon": 121.4737}
}

# 3. Dữ liệu các dòng chảy tiền tệ giữa các điểm
data = [
    {"from_name": "New York", "to_name": "London", "flow_value": 500},
    {"from_name": "New York", "to_name": "Tokyo", "flow_value": 400},
    {"from_name": "New York", "to_name": "Shanghai", "flow_value": 600},
    {"from_name": "London", "to_name": "Singapore", "flow_value": 350},
    {"from_name": "London", "to_name": "Tokyo", "flow_value": 300},
    {"from_name": "Shanghai", "to_name": "Singapore", "flow_value": 450}
]

df = pd.DataFrame(data)
df["from_lat"] = df["from_name"].map(lambda x: centers[x]["lat"])
df["from_lon"] = df["from_name"].map(lambda x: centers[x]["lon"])
df["to_lat"] = df["to_name"].map(lambda x: centers[x]["lat"])
df["to_lon"] = df["to_name"].map(lambda x: centers[x]["lon"])

# 4. Tạo các đường cong dòng chảy (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    get_source_color="[255, 0, 128, 200]",  # Màu hồng neon phát sáng
    get_target_color="[0, 255, 255, 200]",   # Màu xanh cyan phát sáng
    get_width="flow_value / 100",
    pickable=True,
    auto_highlight=True,
)

# 5. Tạo các nút tròn tại vị trí quốc gia (ScatterplotLayer)
nodes_data = pd.DataFrame([{"name": k, "lat": v["lat"], "lon": v["lon"]} for k, v in centers.items()])
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_data,
    get_position="[lon, lat]",
    get_color="[255, 215, 0, 255]",  # Màu vàng kim
    get_radius=250000,
    pickable=True,
)

# 6. Cấu hình vị trí xem bản đồ thế giới mặc định
view_state = pdk.ViewState(
    latitude=25.0,
    longitude=20.0,
    zoom=1.2,
    pitch=45,
)

# 7. GIẢI PHÁP: Sử dụng lệnh hiển thị tích hợp sẵn của Streamlit
# Tự động tải map nền Dark Mode mặc định từ thư viện hệ thống
st.pydeck_chart(
    pdk.Deck(
        layers=[arc_layer, nodes_layer],
        initial_view_state=view_state,
        tooltip={"text": "Dòng chảy từ: {from_name} -> Đến: {to_name}"}
    )
)
