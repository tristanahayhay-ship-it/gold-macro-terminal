import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện chuẩn Dark Mode
st.set_page_config(layout="wide", page_title="Hệ Thống Dòng Chảy Kinh Tế Toàn Cầu")

st.markdown(
    """
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1 { color: #FFFFFF !important; font-weight: 700; }
    p, span, label, th, td { color: #E0E0E0 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Hệ Thống Mạng Lưới Kinh Tế & Dòng Chảy Tiền Tệ")

# Chú thích màu sắc cho người dùng dễ nhìn
st.markdown("""
<div style="display: flex; gap: 20px; font-weight: bold; margin-bottom: 10px;">
    <div><span style="color: #00FFCC;">■</span> Màu Xanh: Tiền đang chảy vào (Inflow)</div>
    <div><span style="color: #FF3366;">■</span> Màu Đỏ: Tiền đang tháo/rút ra (Outflow)</div>
    <div><span style="color: #FFCC00;">■</span> Nút Vàng: Trung tâm kinh tế quốc gia</div>
</div>
""", unsafe_allow_html=True)

# 2. Định nghĩa Tọa độ các Quốc gia & Các khu vực kinh tế nội bộ trong nước đó
# Để khi phóng to (Zoom in) người dùng sẽ nhìn thấy mạng lưới kinh tế riêng của từng quốc gia
centers = {
    # Nút mạng lưới Mỹ
    "Mỹ - New York": {"lat": 40.7128, "lon": -74.0060, "country": "Mỹ"},
    "Mỹ - San Francisco": {"lat": 37.7749, "lon": -122.4194, "country": "Mỹ"},
    "Mỹ - Chicago": {"lat": 41.8781, "lon": -87.6298, "country": "Mỹ"},
    
    # Nút mạng lưới Anh
    "Anh - London": {"lat": 51.5074, "lon": -0.1278, "country": "Anh"},
    "Anh - Manchester": {"lat": 53.4808, "lon": -2.2426, "country": "Anh"},
    
    # Nút mạng lưới Nhật Bản
    "Nhật - Tokyo": {"lat": 35.6762, "lon": 139.6503, "country": "Nhật Bản"},
    "Nhật - Osaka": {"lat": 34.6937, "lon": 135.5023, "country": "Nhật Bản"},
    
    # Nút mạng lưới Trung Quốc
    "Trung Quốc - Shanghai": {"lat": 31.2304, "lon": 121.4737, "country": "Trung Quốc"},
    "Trung Quốc - Beijing": {"lat": 39.9042, "lon": 116.4074, "country": "Trung Quốc"},
    
    # Nút Đông Nam Á
    "Singapore": {"lat": 1.3521, "lon": 103.8198, "country": "Singapore"},
    "Việt Nam - HCM": {"lat": 10.8231, "lon": 106.6297, "country": "Việt Nam"}
}

# 3. Khởi tạo danh sách Dòng chảy Tiền tệ
# Thêm cột "type": "inflow" (tiền chảy vào -> Xanh) hoặc "outflow" (tiền tháo ra -> Đỏ)
raw_flow_data = [
    # --- MẠNG LƯỚI TOÀN CẦU (Kết nối giữa các quốc gia) ---
    {"from": "Mỹ - New York", "to": "Anh - London", "value": 500, "type": "inflow", "scope": "Toàn cầu"},
    {"from": "Mỹ - New York", "to": "Trung Quốc - Shanghai", "value": 700, "type": "outflow", "scope": "Toàn cầu"},
    {"from": "Nhật - Tokyo", "to": "Mỹ - New York", "value": 600, "type": "inflow", "scope": "Toàn cầu"},
    {"from": "Trung Quốc - Shanghai", "to": "Singapore", "value": 450, "type": "inflow", "scope": "Toàn cầu"},
    {"from": "Anh - London", "to": "Việt Nam - HCM", "value": 300, "type": "inflow", "scope": "Toàn cầu"},
    {"from": "Mỹ - San Francisco", "to": "Nhật - Tokyo", "value": 550, "type": "outflow", "scope": "Toàn cầu"},

    # --- MẠNG LƯỚI NỘI BỘ RIÊNG CỦA CÁC QUỐC GIA (Chảy trong nước) ---
    # Nội bộ Mỹ
    {"from": "Mỹ - New York", "to": "Mỹ - San Francisco", "value": 350, "type": "inflow", "scope": "Nội bộ"},
    {"from": "Mỹ - Chicago", "to": "Mỹ - New York", "value": 250, "type": "outflow", "scope": "Nội bộ"},
    # Nội bộ Anh
    {"from": "Anh - London", "to": "Anh - Manchester", "value": 200, "type": "inflow", "scope": "Nội bộ"},
    # Nội bộ Nhật
    {"from": "Nhật - Tokyo", "to": "Nhật - Osaka", "value": 300, "type": "outflow", "scope": "Nội bộ"},
    # Nội bộ Trung Quốc
    {"from": "Trung Quốc - Beijing", "to": "Trung Quốc - Shanghai", "value": 400, "type": "inflow", "scope": "Nội bộ"}
]

# Chuyển đổi và tính toán tọa độ cho bảng dữ liệu dòng chảy
df_flows = pd.DataFrame(raw_flow_data)
df_flows["from_lat"] = df_flows["from"].map(lambda x: centers[x]["lat"])
df_flows["from_lon"] = df_flows["from"].map(lambda x: centers[x]["lon"])
df_flows["to_lat"] = df_flows["to"].map(lambda x: centers[x]["lat"])
df_flows["to_lon"] = df_flows["to"].map(lambda x: centers[x]["lon"])

# Hàm gán màu sắc RGB dựa trên thuộc tính Tháo/Chảy của dòng tiền
# type == "inflow" -> Xanh Neon, type == "outflow" -> Đỏ Neon [255, 51, 102]
df_flows["color"] = df_flows["type"].apply(lambda x: [0, 255, 204, 200] if x == "inflow" else)

# 4. Cấu hình lớp hiển thị các sợi dây liên kết dòng chảy (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_flows,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    # Sợi dây liên kết sẽ lấy màu trực tiếp theo trạng thái Tiền chảy (Xanh) hay Tiền tháo (Đỏ)
    get_source_color="color",
    get_target_color="color",
    get_width="value / 100",  # Độ dày tỷ lệ thuận với lượng tiền
    pickable=True,
    auto_highlight=True,
)

# 5. Cấu hình lớp hiển thị các nút mạng lưới kinh tế (ScatterplotLayer)
nodes_list = [{"name": k, "lat": v["lat"], "lon": v["lon"], "country": v["country"]} for k, v in centers.items()]
df_nodes = pd.DataFrame(nodes_list)

nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_nodes,
    get_position="[lon, lat]",
    get_color="[255, 204, 0]", # Các điểm nút màu vàng kim phát sáng
    get_radius=150000,          # Kích thước nút vừa phải để khi zoom nhìn rõ mạng lưới nội bộ
    pickable=True,
)

# 6. Cấu hình góc nhìn thế giới ban đầu
view_state = pdk.ViewState(
    latitude=30.0,
    longitude=10.0,
    zoom=1.3,
    pitch=40,
)

# 7. Render bản đồ Pydeck lồng ghép dữ liệu
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Hệ thống:</b> {scope}<br/>"
                "<b>Nguồn:</b> {from}<br/>"
                "<b>Đích:</b> {to}<br/>"
                "<b>Trạng thái:</b> {type}<br/>"
                "<b>Giá trị:</b> {value} Tỷ USD",
        "style": {"backgroundColor": "#1C1E24", "color": "white"}
    }
)

st.pydeck_chart(r)
