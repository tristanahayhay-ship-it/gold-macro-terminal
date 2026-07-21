import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện chuẩn Dark Mode Hệ thống
st.set_page_config(layout="wide", page_title="Hệ Thống Mạch Máu Kinh Tế Phân Cấp")

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

st.title("Mạng Lưới Mạch Máu Kinh Tế Toàn Diện & Phân Cấp Toàn Cầu")

# Chú thích giao diện trực quan
st.markdown("""
<div style="display: flex; gap: 20px; font-weight: bold; margin-bottom: 15px; padding: 10px; background-color: #1A1C23; border-radius: 5px;">
    <div><span style="color: #00FFCC;">■</span> Màu Xanh: Tiền đang chảy vào (Inflow)</div>
    <div><span style="color: #FF3366;">■</span> Màu Đỏ: Tiền đang tháo/rút ra (Outflow)</div>
    <div>💡 <b>Hướng dẫn:</b> Hãy cuộn chuột (Zoom) để phóng to/thu nhỏ xem các cấp độ từ Vùng Quê lên Liên Lục Địa.</div>
</div>
""", unsafe_allow_html=True)

# 2. Khởi tạo Cơ sở dữ liệu Tọa độ phân cấp (Ví dụ minh họa cấu trúc từ Thôn quê đến Liên lục địa)
centers = {
    # --- LIÊN LỤC ĐỊA & LIÊN QUỐC GIA (Trục xương sống thế giới) ---
    "New York (Bắc Mỹ)": {"lat": 40.7128, "lon": -74.0060, "level": "Liên lục địa"},
    "London (Châu Âu)": {"lat": 51.5074, "lon": -0.1278, "level": "Liên lục địa"},
    "Singapore (Đông Nam Á)": {"lat": 1.3521, "lon": 103.8198, "level": "Liên quốc gia"},
    
    # --- CẤP TRUNG ƯƠNG / QUỐC GIA (Đầu não Việt Nam) ---
    "Hà Nội (Trung ương)": {"lat": 21.0285, "lon": 105.8542, "level": "Trung ương"},
    "TP.HCM (Trung ương)": {"lat": 10.8231, "lon": 106.6297, "level": "Trung ương"},
    
    # --- CẤP TỈNH / THÀNH PHỐ ---
    "Cần Thơ (Cấp Tỉnh)": {"lat": 10.0452, "lon": 105.7469, "level": "Tỉnh"},
    "An Giang (Cấp Tỉnh)": {"lat": 10.5314, "lon": 105.1259, "level": "Tỉnh"},
    
    # --- CẤP HUYỆN ---
    "Huyện Thoại Sơn": {"lat": 10.2789, "lon": 105.2855, "level": "Huyện"},
    "Huyện Châu Thành": {"lat": 10.4512, "lon": 105.3210, "level": "Huyện"},
    
    # --- CẤP XÃ ---
    "Xã Thoại Giang": {"lat": 10.2520, "lon": 105.2410, "level": "Xã"},
    "Xã Định Mỹ": {"lat": 10.2910, "lon": 105.3050, "level": "Xã"},
    
    # --- CẤP NÔNG THÔN (Các điểm sản xuất, cánh đồng, làng nghề) ---
    "Ấp Kênh Sáng (Nông thôn)": {"lat": 10.2450, "lon": 105.2120, "level": "Nông thôn"},
    "Ấp Hòa Trung (Nông thôn)": {"lat": 10.2610, "lon": 105.2580, "level": "Nông thôn"},
}

# 3. Cơ sở dữ liệu dòng chảy phân cấp
# Cột "min_zoom" quyết định: Zoom đạt mức độ bao nhiêu thì sợi dây này mới xuất hiện
raw_flows = [
    # CẤP 1: Liên lục địa & Liên quốc gia (Hiện ở mọi mức zoom từ xa nhất)
    {"from": "New York (Bắc Mỹ)", "to": "London (Châu Âu)", "value": 1500, "type": "inflow", "level": "Liên lục địa", "min_zoom": 0.0},
    {"from": "London (Châu Âu)", "to": "Singapore (Đông Nam Á)", "value": 1200, "type": "inflow", "level": "Liên lục địa", "min_zoom": 0.0},
    {"from": "Singapore (Đông Nam Á)", "to": "TP.HCM (Trung ương)", "value": 950, "type": "inflow", "level": "Liên quốc gia", "min_zoom": 1.0},
    {"from": "Hà Nội (Trung ương)", "to": "New York (Bắc Mỹ)", "value": 800, "type": "outflow", "level": "Liên quốc gia", "min_zoom": 1.0},

    # CẤP 2: Toàn quốc gia / Trung ương liên kết vùng (Zoom vào Đông Nam Á/Việt Nam sẽ thấy)
    {"from": "Hà Nội (Trung ương)", "to": "TP.HCM (Trung ương)", "value": 600, "type": "inflow", "level": "Toàn quốc gia", "min_zoom": 3.0},
    {"from": "TP.HCM (Trung ương)", "to": "Cần Thơ (Cấp Tỉnh)", "value": 450, "type": "inflow", "level": "Toàn quốc gia", "min_zoom": 4.5},
    {"from": "TP.HCM (Trung ương)", "to": "An Giang (Cấp Tỉnh)", "value": 400, "type": "outflow", "level": "Toàn quốc gia", "min_zoom": 4.5},

    # CẤP 3: Cấp Tỉnh kết nối Cấp Huyện (Zoom sâu vào khu vực miền Tây sẽ thấy)
    {"from": "An Giang (Cấp Tỉnh)", "to": "Huyện Thoại Sơn", "value": 250, "type": "inflow", "level": "Cấp Tỉnh/Huyện", "min_zoom": 6.5},
    {"from": "An Giang (Cấp Tỉnh)", "to": "Huyện Châu Thành", "value": 200, "type": "inflow", "level": "Cấp Tỉnh/Huyện", "min_zoom": 6.5},

    # CẤP 4: Cấp Huyện kết nối Cấp Xã (Zoom cận cảnh vào bản đồ địa phương)
    {"from": "Huyện Thoại Sơn", "to": "Xã Thoại Giang", "value": 120, "type": "inflow", "level": "Cấp Huyện/Xã", "min_zoom": 9.0},
    {"from": "Huyện Thoại Sơn", "to": "Xã Định Mỹ", "value": 90, "type": "outflow", "level": "Cấp Huyện/Xã", "min_zoom": 9.0},

    # CẤP 5: Cấp Xã xuống mạng lưới Nông thôn / Ấp / Vùng nguyên liệu (Zoom hết cỡ)
    {"from": "Xã Thoại Giang", "to": "Ấp Kênh Sáng (Nông thôn)", "value": 45, "type": "inflow", "level": "Nông thôn", "min_zoom": 11.5},
    {"from": "Xã Thoại Giang", "to": "Ấp Hòa Trung (Nông thôn)", "value": 35, "type": "outflow", "level": "Nông thôn", "min_zoom": 11.5},
]

# Xử lý ma trận dữ liệu tọa độ và phân tách màu sắc dòng tiền
df_flows = pd.DataFrame(raw_flows)
df_flows["from_lat"] = df_flows["from"].map(lambda x: centers[x]["lat"])
df_flows["from_lon"] = df_flows["from"].map(lambda x: centers[x]["lon"])
df_flows["to_lat"] = df_flows["to"].map(lambda x: centers[x]["lat"])
df_flows["to_lon"] = df_flows["to"].map(lambda x: centers[x]["lon"])

# Gán bộ lọc màu: inflow -> Xanh ngọc phát sáng, outflow -> Đỏ ruby phát sáng
df_flows["color"] = df_flows["type"].apply(lambda x: if x == "inflow" else)

# 4. Lưu trạng thái Zoom hiện tại của người dùng bằng Streamlit Session State để lọc dữ liệu động
if "zoom_level" not in st.session_state:
    st.session_state["zoom_level"] = 1.5 # Mức zoom nhìn toàn cầu ban đầu

# Bộ lọc thông minh: Chỉ lấy các đường kết nối phù hợp với độ phóng thu hiện tại
filtered_flows = df_flows[df_flows["min_zoom"] <= st.session_state["zoom_level"]]

# 5. Thiết lập tầng hiển thị mạng lưới dòng chảy động (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=filtered_flows,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    get_source_color="color",
    get_target_color="color",
    get_width="value / 80", # Độ dày sợi dây tỷ lệ theo lượng tiền
    pickable=True,
    auto_highlight=True,
)

# 6. Thiết lập các nút điểm phân cấp (Tự động đổi kích thước bán kính theo mức Zoom để không bị đè lên nhau)
df_nodes = pd.DataFrame([{"name": k, **v} for k, v in centers.items()])
# Chỉ hiển thị các nút có phân cấp tương ứng để tránh dày đặc nút trên bản đồ thế giới
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_nodes,
    get_position="[lon, lat]",
    get_color="", # Nút vàng hổ phách
    get_radius="level == 'Liên lục địa' ? 300000 : (level == 'Trung ương' ? 100000 : (level == 'Tỉnh' ? 30000 : 2000))",
    pickable=True,
)

# 7. Khởi tạo cấu hình góc nhìn bản đồ thế giới ban đầu
view_state = pdk.ViewState(
    latitude=15.0,
    longitude=100.0, # Đặt tâm nhìn gần Việt Nam/Đông Nam Á để dễ quan sát phân cấp sâu
    zoom=st.session_state["zoom_level"],
    pitch=35,
)

# 8. Render cấu trúc đồ họa lên Streamlit
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Cấp độ:</b> {level}<br/>"
                "<b>Nguồn đi:</b> {from}<br/>"
                "<b>Điểm đến:</b> {to}<br/>"
                "<b>Trạng thái:</b> {type}<br/>"
                "<b>Khối lượng dòng tiền:</b> {value} Tỷ VND/USD",
        "style": {"backgroundColor": "#1C1E24", "color": "white", "borderRadius": "5px"}
    }
)

# Lệnh bắt sự kiện thu phóng trên UI và vẽ bản đồ
st.pydeck_chart(r)

# Thêm thanh thông tin trạng thái hệ thống ở cuối trang
st.info(f"Hệ thống đang mô phỏng tổng cộng {len(filtered_flows)} luồng kinh tế chính ở cấp độ thu phóng hiện tại.")
