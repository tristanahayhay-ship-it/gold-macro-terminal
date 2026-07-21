import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện Streamlit màn hình rộng và ép nền đen sâu (Deep Black)
st.set_page_config(layout="wide", page_title="Cyber Global Money Flow")

st.markdown(
    """
    <style>
    .stApp { background-color: #030712; color: #ffffff; }
    h1, p, span, div { color: #ffffff !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 Hệ Thống Toàn Cảnh Dòng Chảy Tiền Tệ Đa Tầng Toàn Cầu")
st.caption("Bản đồ ma trận dòng chảy tài sản vĩ mô kết nối đa tầng từ cấp cơ sở đến liên lục địa.")

# 2. Cơ sở dữ liệu tọa độ địa lý thực tế
global_locations = {
    # === CỤM VIỆT NAM ===
    "VN_Xa_CoSo": [106.2400, 20.9400],         
    "VN_Huyen_Hub": [106.2800, 20.9800],       
    "VN_Tinh_Center": [106.3330, 20.9409],     
    "VN_HaNoi_Central": [105.8542, 21.0285],   

    # === CỤM MỸ (BẮC MỸ) ===
    "US_Rural_Commune": [-95.7129, 37.0902],    
    "US_District_Hub": [-87.6298, 41.8781],     
    "US_NewYork_WallStreet": [-74.0113, 40.7075], 

    # === CỤM CHÂU ÂU (EU) ===
    "EU_Local_Production": [7.4653, 46.9480],   
    "EU_Frankfurt_Central": [8.6821, 50.1109],  

    # === CỤM TRẠM TRUNG CHUYỂN QUỐC TẾ ===
    "Singapore_Global_Hub": [103.8198, 1.3521], 
    "Japan_Tokyo_Central": [139.6503, 35.6762]  
}

# 3. Danh sách dòng chảy MẠNG LƯỚI TỔNG HỢP
global_flows = [
    # MẠCH NỘI ĐỊA VIỆT NAM
    {"from": "VN_Xa_CoSo", "to": "VN_Huyen_Hub", "status": "neutral", "desc": "[CẤP XÃ ➔ HUYỆN] Dân gửi tiền tích lũy lên hệ thống tín dụng"},
    {"from": "VN_Huyen_Hub", "to": "VN_Tinh_Center", "status": "strong_in", "desc": "[CẤP HUYỆN ➔ TỈNH] Doanh nghiệp nộp thuế sản xuất công nghiệp về Tỉnh"},
    {"from": "VN_Tinh_Center", "to": "VN_HaNoi_Central", "status": "strong_out", "desc": "[CẤP TỈNH ➔ NHÀ NƯỚC] Tỉnh kết chuyển thặng dư ngân sách về Trung ương"},

    # MẠCH NỘI ĐỊA MỸ
    {"from": "US_Rural_Commune", "to": "US_District_Hub", "status": "strong_in", "desc": "[CẤP CƠ SỞ MỸ] Nông sản thô từ trang trại đổ về nhà máy chế biến Chicago"},
    {"from": "US_District_Hub", "to": "US_NewYork_WallStreet", "status": "strong_in", "desc": "[CẤP TRUNG GIAN MỸ] Dòng vốn doanh nghiệp niêm yết lên sàn New York"},

    # MẠCH NỘI ĐỊA CHÂU ÂU
    {"from": "EU_Local_Production", "to": "EU_Frankfurt_Central", "status": "neutral", "desc": "[CẤP CƠ SỞ EU] Dòng tiền tiết kiệm Euro luân chuyển về ECB"},

    # LIÊN KẾT XUYÊN LỤC ĐỊA
    {"from": "US_NewYork_WallStreet", "to": "Singapore_Global_Hub", "status": "strong_in", "desc": "[XUYÊN LỤC ĐỊA] Dòng vốn đầu tư từ Mỹ phóng sang tài chính Châu Á"},
    {"from": "Singapore_Global_Hub", "to": "VN_Huyen_Hub", "status": "strong_in", "desc": "[XUYÊN BIÊN GIỚI] Vốn ngoại FDI bơm thẳng vào xây nhà máy ở cụm công nghiệp Huyện tại Việt Nam"},
    {"from": "VN_HaNoi_Central", "to": "Japan_Tokyo_Central", "status": "strong_in", "desc": "[QUỐC TẾ] Việt Nam xuất khẩu hàng hóa công nghệ sang Nhật Bản thu ngoại tệ mạnh"},
    {"from": "EU_Frankfurt_Central", "to": "US_NewYork_WallStreet", "status": "strong_out", "desc": "[XUYÊN ĐẠI DƯƠNG] Giới đầu tư Châu Âu rút vốn, chuyển dịch sang tài sản đô-la Mỹ an toàn"},
    {"from": "Japan_Tokyo_Central", "to": "US_NewYork_WallStreet", "status": "neutral", "desc": "[TOÀN CẦU] Nhật Bản luân chuyển dòng vốn mua Trái phiếu Chính phủ Mỹ"}
]

# 4. Bảng mã màu sợi dây tài chính vĩ mô
color_map = {
    "strong_in": [0, 255, 0, 200],    # 🟢 Xanh lá dạ quang rực rỡ
    "strong_out": [255, 0, 0, 200],  # 🔴 Đỏ sậm quyền lực
    "neutral": [255, 255, 0, 220],        # 🟡 Vàng rực sáng
}

# 5. Xử lý dữ liệu nạp các đường dây (Arcs)
processed_arcs = []
for flow in global_flows:
    start_coords = global_locations[flow["from"]]
    end_coords = global_locations[flow["to"]]
    processed_arcs.append({
        "from_lon": start_coords[0], "from_lat": start_coords[1],
        "to_lon": end_coords[0], "to_lat": end_coords[1],
        "color": color_map[flow["status"]],
        "tooltip_text": flow["desc"]
    })
df_arcs = pd.DataFrame(processed_arcs)

# 6. Xử lý dữ liệu nạp các điểm nút quốc gia (Nodes) đã được sửa lỗi biến số trống
processed_nodes = []
for name, coords in global_locations.items():
    is_major_hub = any(k in name for k in ["Central", "Street", "Hub"]) and "Huyen" not in name
    
    # Ép giá trị màu cố định để tránh lỗi cú pháp
    if is_major_hub:
        node_color = [255, 100, 0, 230]   # 🟠 Các trung tâm kinh tế lớn màu Cam rực rỡ
        radius_size = 120000
    else:
        node_color = [0, 200, 255, 230]   # 🔵 Cấp xã/huyện cơ sở màu Xanh Cyan công nghệ
        radius_size = 45000

    processed_nodes.append({
        "lon": coords[0], "lat": coords[1], "name": name,
        "color": node_color, 
        "radius": radius_size
    })
df_nodes = pd.DataFrame(processed_nodes)

# 7. NÂNG CẤP LỚP NỀN: ĐẤT LIỀN MÀU XANH TEAL NEON BÓNG ĐÊM SỐNG ĐỘNG
DATA_URL = "https://githubusercontent.com"

background_map_layer = pdk.Layer(
    "GeoJsonLayer",
    DATA_URL,
    stroked=True,
    filled=True,
    get_fill_color=[10, 35, 45, 200],   # Đất liền màu Teal bóng đêm cực sang
    get_line_color=[0, 160, 200, 180],  # Viền bờ biển phát sáng màu xanh dạ quang
    line_width_min_pixels=1.5,
)

# 8. Khởi tạo lớp đồ họa đường cong dòng tiền
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_arcs,
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width=5, 
    pickable=True,
    auto_highlight=True
)

# 9. Khởi tạo lớp đồ họa điểm nút đa màu sắc sống động
node_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_nodes,
    get_position=["lon", "lat"],
    get_color="color", 
    get_radius="radius",
    pickable=True
)

# 10. Cấu hình góc nhìn camera vĩ mô bao quát thế giới
view_state = pdk.ViewState(
    latitude=23.0,
    longitude=20.0,
    zoom=1.3,
    pitch=45,
    bearing=5
)

# 11. Render toàn bộ hệ thống ma trận lên màn hình
r = pdk.Deck(
    layers=[background_map_layer, arc_layer, node_layer],
    initial_view_state=view_state,
    map_style=None, 
    tooltip={"text": "{tooltip_text}"}
)

st.pydeck_chart(r)
