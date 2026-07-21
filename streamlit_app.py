import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện Dark Mode toàn diện cho hệ thống
st.set_page_config(layout="wide", page_title="Hệ Thống Mạch Máu Kinh Tế Phân Cấp")

st.markdown(
    """
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1 { color: #FFFFFF !important; font-weight: 700; }
    p, span, label, th, td { color: #E0E0E0 !important; }
    /* Tùy chỉnh màu sắc thanh bên Sidebar */
    [data-testid="stSidebar"] { background-color: #1A1C23; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sơ Đồ Mạng Lưới Kinh Tế & Dòng Chảy Tiền Tệ Phân Cấp")

# 2. Xây dựng Thanh Điều Khiển Cấp Độ Hệ Thống ở bên trái (Sidebar)
st.sidebar.header("BẢNG ĐIỀU KHIỂN")
selected_level = st.sidebar.radio(
    "Chọn cấp độ mạng lưới kinh tế muốn xem:",
    [
        "Tất cả các cấp độ",
        "Cấp Nông thôn & Cấp Xã",
        "Cấp Huyện & Cấp Tỉnh",
        "Cấp Nhà nước / Toàn quốc gia",
        "Cấp Liên quốc gia & Liên lục địa"
    ]
)

# Chú thích màu sắc dòng tiền trên màn hình chính
st.markdown("""
<div style="display: flex; gap: 20px; font-weight: bold; margin-bottom: 15px; padding: 10px; background-color: #1A1C23; border-radius: 5px;">
    <div><span style="color: #00FFCC;">■</span> Màu Xanh: Tiền đang chảy vào (Inflow)</div>
    <div><span style="color: #FF3366;">■</span> Màu Đỏ: Tiền đang tháo/rút ra (Outflow)</div>
</div>
""", unsafe_allow_html=True)

# 3. Cơ sở dữ liệu Tọa độ phân cấp (Đầy đủ từ Thôn quê đến Toàn cầu)
centers = {
    # --- LIÊN LỤC ĐỊA & LIÊN QUỐC GIA ---
    "New York (Bắc Mỹ)": {"lat": 40.7128, "lon": -74.0060, "level": "Liên lục địa"},
    "London (Châu Âu)": {"lat": 51.5074, "lon": -0.1278, "level": "Liên lục địa"},
    "Tokyo (Đông Á)": {"lat": 35.6762, "lon": 139.6503, "level": "Liên lục địa"},
    "Singapore (Đông Nam Á)": {"lat": 1.3521, "lon": 103.8198, "level": "Liên quốc gia"},
    
    # --- CẤP TRUNG ƯƠNG / NHÀ NƯỚC ---
    "Hà Nội (Trung ương)": {"lat": 21.0285, "lon": 105.8542, "level": "Nhà nước"},
    "TP.HCM (Trung ương)": {"lat": 10.8231, "lon": 106.6297, "level": "Nhà nước"},
    
    # --- CẤP TỈNH ---
    "Cần Thơ (Cấp Tỉnh)": {"lat": 10.0452, "lon": 105.7469, "level": "Tỉnh"},
    "An Giang (Cấp Tỉnh)": {"lat": 10.5314, "lon": 105.1259, "level": "Tỉnh"},
    
    # --- CẤP HUYỆN ---
    "Huyện Thoại Sơn": {"lat": 10.2789, "lon": 105.2855, "level": "Huyện"},
    "Huyện Châu Thành": {"lat": 10.4512, "lon": 105.3210, "level": "Huyện"},
    
    # --- CẤP XÃ ---
    "Xã Thoại Giang": {"lat": 10.2520, "lon": 105.2410, "level": "Xã"},
    "Xã Định Mỹ": {"lat": 10.2910, "lon": 105.3050, "level": "Xã"},
    
    # --- CẤP NÔNG THÔN ---
    "Ấp Kênh Sáng (Nông thôn)": {"lat": 10.2450, "lon": 105.2120, "level": "Nông thôn"},
    "Ấp Hòa Trung (Nông thôn)": {"lat": 10.2610, "lon": 105.2580, "level": "Nông thôn"},
}

# 4. Cơ sở dữ liệu dòng chảy phân cấp được định nghĩa rõ ràng
raw_flows = [
    # CẤP: Liên lục địa & Liên quốc gia
    {"from": "New York (Bắc Mỹ)", "to": "London (Châu Âu)", "value": 1500, "type": "inflow", "level": "Liên lục địa"},
    {"from": "London (Châu Âu)", "to": "Tokyo (Đông Á)", "value": 1300, "type": "outflow", "level": "Liên lục địa"},
    {"from": "Tokyo (Đông Á)", "to": "Singapore (Đông Nam Á)", "value": 1200, "type": "inflow", "level": "Liên lục địa"},
    {"from": "Singapore (Đông Nam Á)", "to": "TP.HCM (Trung ương)", "value": 950, "type": "inflow", "level": "Liên quốc gia"},
    {"from": "Hà Nội (Trung ương)", "to": "New York (Bắc Mỹ)", "value": 800, "type": "outflow", "level": "Liên quốc gia"},

    # CẤP: Nhà nước / Toàn quốc gia
    {"from": "Hà Nội (Trung ương)", "to": "TP.HCM (Trung ương)", "value": 700, "type": "inflow", "level": "Nhà nước"},
    {"from": "TP.HCM (Trung ương)", "to": "Cần Thơ (Cấp Tỉnh)", "value": 450, "type": "inflow", "level": "Nhà nước"},
    {"from": "TP.HCM (Trung ương)", "to": "An Giang (Cấp Tỉnh)", "value": 400, "type": "outflow", "level": "Nhà nước"},

    # CẤP: Huyện & Tỉnh
    {"from": "An Giang (Cấp Tỉnh)", "to": "Huyện Thoại Sơn", "value": 250, "type": "inflow", "level": "Tỉnh"},
    {"from": "An Giang (Cấp Tỉnh)", "to": "Huyện Châu Thành", "value": 200, "type": "inflow", "level": "Tỉnh"},
    {"from": "Cần Thơ (Cấp Tỉnh)", "to": "Huyện Thoại Sơn", "value": 180, "type": "outflow", "level": "Huyện"},

    # CẤP: Xã & Nông thôn
    {"from": "Huyện Thoại Sơn", "to": "Xã Thoại Giang", "value": 120, "type": "inflow", "level": "Xã"},
    {"from": "Huyện Thoại Sơn", "to": "Xã Định Mỹ", "value": 90, "type": "outflow", "level": "Xã"},
    {"from": "Xã Thoại Giang", "to": "Ấp Kênh Sáng (Nông thôn)", "value": 45, "type": "inflow", "level": "Nông thôn"},
    {"from": "Xã Thoại Giang", "to": "Ấp Hòa Trung (Nông thôn)", "value": 35, "type": "outflow", "level": "Nông thôn"},
]

# Chuyển đổi dữ liệu sang bảng Pandas
df_flows = pd.DataFrame(raw_flows)
df_flows["from_lat"] = df_flows["from"].map(lambda x: centers[x]["lat"])
df_flows["from_lon"] = df_flows["from"].map(lambda x: centers[x]["lon"])
df_flows["to_lat"] = df_flows["to"].map(lambda x: centers[x]["lat"])
df_flows["to_lon"] = df_flows["to"].map(lambda x: centers[x]["lon"])

# 5. Hàm gán màu chuẩn (Xóa bỏ hoàn toàn Lambda để tránh lỗi cú pháp)
def assign_flow_color(flow_type):
    if flow_type == "inflow":
        return [0, 255, 204, 220]  # Xanh ngọc phát sáng
    else:
        return [255, 51, 102, 220]  # Đỏ hồng tháo vốn

df_flows["color"] = df_flows["type"].apply(assign_flow_color)

# 6. Thuật toán Lọc dữ liệu thông minh theo lựa chọn của người dùng trên thanh điều khiển
if selected_level == "Cấp Nông thôn & Cấp Xã":
    filtered_flows = df_flows[df_flows["level"].isin(["Xã", "Nông thôn"])]
    target_lat, target_lon, default_zoom = 10.25, 105.25, 12.0  # Tự động zoom cận cảnh vào làng quê
elif selected_level == "Cấp Huyện & Cấp Tỉnh":
    filtered_flows = df_flows[df_flows["level"].isin(["Huyện", "Tỉnh"])]
    target_lat, target_lon, default_zoom = 10.35, 105.40, 9.5   # Tự động zoom vào khu vực miền Tây
elif selected_level == "Cấp Nhà nước / Toàn quốc gia":
    filtered_flows = df_flows[df_flows["level"] == "Nhà nước"]
    target_lat, target_lon, default_zoom = 15.5, 108.0, 5.0     # Tự động zoom nhìn toàn cảnh Việt Nam
elif selected_level == "Cấp Liên quốc gia & Liên lục địa":
    filtered_flows = df_flows[df_flows["level"].isin(["Liên quốc gia", "Liên lục địa"])]
    target_lat, target_lon, default_zoom = 25.0, 20.0, 1.5      # Tự động lùi góc nhìn ra toàn cầu
else:
    filtered_flows = df_flows  # Hiển thị tất cả các cấp độ cùng lúc
    target_lat, target_lon, default_zoom = 20.0, 80.0, 2.0

# 7. Thiết lập tầng mạng lưới luồng tiền (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=filtered_flows,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    get_source_color="color",
    get_target_color="color",
    get_width="value / 70",
    pickable=True,
    auto_highlight=True,
)

# 8. Thiết lập các nút điểm phân cấp
df_nodes = pd.DataFrame([{"name": k, **v} for k, v in centers.items()])
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_nodes,
    get_position="[lon, lat]",
    get_color=[255, 204, 0, 230],  # Điểm nút màu vàng kim
    get_radius="level == 'Liên lục địa' ? 250000 : (level == 'Nhà nước' ? 90000 : (level == 'Tỉnh' ? 25000 : 1500))",
    pickable=True,
)

# 9. Đẩy cấu hình góc nhìn động lên bản đồ
view_state = pdk.ViewState(
    latitude=target_lat,
    longitude=target_lon,
    zoom=default_zoom,
    pitch=35,
)

# 10. Hiển thị đồ họa sơ đồ
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Mức độ sơ đồ:</b> {level}<br/>"
                "<b>Nguồn phát:</b> {from}<br/>"
                "<b>Điểm tiếp nhận:</b> {to}<br/>"
                "<b>Trạng thái:</b> {type}<br/>"
                "<b>Quy mô dòng vốn:</b> {value} Tỷ",
        "style": {"backgroundColor": "#1C1E24", "color": "white", "borderRadius": "5px"}
    }
)

st.pydeck_chart(r)

# Thống kê số lượng mạch máu kinh tế đang chạy dưới chân trang
st.sidebar.success(f"Đang hiển thị {len(filtered_flows)} mạch dữ liệu.")
