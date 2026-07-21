import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình không gian Dark Mode vũ trụ (Nền đen sâu)
st.set_page_config(layout="wide", page_title="Hệ Thống Mạch Máu Kinh Tế Toàn Cầu")

st.markdown(
    """
    <style>
    .stApp { background-color: #020408; color: #FFFFFF; }
    h1 { color: #FFFFFF !important; font-weight: 800; text-shadow: 0px 0px 15px rgba(0,255,204,0.3); }
    p, span, label, th, td { color: #E0E0E0 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mạng Lưới Thần Kinh Kinh Tế & Mạch Máu Tiền Tệ Toàn Cầu")

# Bảng chú thích màu sắc
st.markdown("""
<div style="display: flex; gap: 20px; font-weight: bold; margin-bottom: 15px; padding: 12px; background-color: #0B0E14; border-radius: 6px; border: 1px solid #1A2233;">
    <div><span style="color: #00FFCC; font-size: 18px;">■</span> Dòng tiền CHẢY VÀO (Inflow - Xanh Ngọc)</div>
    <div><span style="color: #FF3366; font-size: 18px;">■</span> Dòng tiền THÁO ĐI (Outflow - Đỏ Hồng)</div>
    <div style="margin-left: auto; color: #FFCC00;">🌐 Bản đồ Tổng quan Toàn cầu (Từ Làng quê đến Liên Lục địa gộp chung 1 bộ dữ liệu)</div>
</div>
""", unsafe_allow_html=True)

# 2. CƠ SỞ DỮ LIỆU TỌA ĐỘ TOÀN CẦU (Phân cấp từ Nông thôn lên Quốc tế)
centers = {
    # === KHU VỰC BẮC MỸ ===
    "Trung tâm New York (Liên lục địa)": {"lat": 40.7128, "lon": -74.0060, "level": "Liên lục địa"},
    "Bang California (Cấp Nhà nước)": {"lat": 36.7783, "lon": -119.4179, "level": "Nhà nước"},
    "Huyện Fresno (Cấp Huyện)": {"lat": 36.7378, "lon": -119.7871, "level": "Huyện"},
    "Thị trấn Lanare (Cấp Xã)": {"lat": 36.4177, "lon": -119.8329, "level": "Xã"},
    "Trang trại Westlands (Nông thôn)": {"lat": 36.3500, "lon": -120.1000, "level": "Nông thôn"},

    # === KHU VỰC CHÂU ÂU ===
    "Trung tâm London (Liên lục địa)": {"lat": 51.5074, "lon": -0.1278, "level": "Liên lục địa"},
    "Vùng Bavaria Đức (Cấp Tỉnh)": {"lat": 48.7904, "lon": 11.4975, "level": "Tỉnh"},
    "Huyện Dingolfing (Cấp Huyện)": {"lat": 48.6293, "lon": 12.4991, "level": "Huyện"},
    "Xã Loiching (Cấp Xã)": {"lat": 48.6167, "lon": 12.4333, "level": "Xã"},
    "Cánh đồng Nông nghiệp (Nông thôn Đan Mạch)": {"lat": 55.6000, "lon": 10.3000, "level": "Nông thôn"},

    # === KHU VỰC ĐÔNG Á & TRUNG QUỐC ===
    "Trung tâm Thượng Hải (Liên lục địa)": {"lat": 31.2304, "lon": 121.4737, "level": "Liên lục địa"},
    "Tỉnh Chiết Giang (Cấp Tỉnh)": {"lat": 29.1416, "lon": 119.7889, "level": "Tỉnh"},
    "Huyện Nghĩa Ô (Cấp Huyện)": {"lat": 29.3068, "lon": 120.0754, "level": "Huyện"},
    "Thị trấn Sục Khê (Cấp Xã)": {"lat": 29.2700, "lon": 120.1200, "level": "Xã"},
    "Xưởng sản xuất Nông thôn (Trung Quốc)": {"lat": 29.2300, "lon": 120.1500, "level": "Nông thôn"},

    # === KHU VỰC ĐÔNG NAM Á & VIỆT NAM ===
    "Trung tâm Singapore (Liên quốc gia)": {"lat": 1.3521, "lon": 103.8198, "level": "Liên quốc gia"},
    "TP. Hồ Chí Minh (Trung ương)": {"lat": 10.8231, "lon": 106.6297, "level": "Nhà nước"},
    "An Giang (Cấp Tỉnh)": {"lat": 10.5314, "lon": 105.1259, "level": "Tỉnh"},
    "Huyện Thoại Sơn": {"lat": 10.2789, "lon": 105.2855, "level": "Huyện"},
    "Xã Thoại Giang": {"lat": 10.2520, "lon": 105.2410, "level": "Xã"},
    "Ấp Kênh Sáng (Nông thôn)": {"lat": 10.2450, "lon": 105.2120, "level": "Nông thôn"},

    # === KHU VỰC ÚC & PHI & NAM MỸ ===
    "Trung tâm Sydney (Úc)": {"lat": -33.8688, "lon": 151.2093, "level": "Liên lục địa"},
    "Khu mỏ Johannesburg (Nam Phi)": {"lat": -26.2041, "lon": 28.0473, "level": "Liên lục địa"},
    "Cảng Sao Paulo (Nam Mỹ)": {"lat": -23.5505, "lon": -46.6333, "level": "Liên lục địa"}
}

# 3. MẠNG LƯỚI DÒNG CHẢY KẾT NỐI CHẰNG CHỊT ĐA QUỐC GIA (Xanh = Vào, Đỏ = Tháo)
raw_flows = [
    # --- TRỤC XƯƠNG SỐNG LIÊN LỤC ĐỊA (Mạng lưới bao phủ hành tinh) ---
    {"from": "Trung tâm New York (Liên lục địa)", "to": "Trung tâm London (Liên lục địa)", "value": 2000, "type": "inflow", "level": "Liên lục địa"},
    {"from": "Trung tâm London (Liên lục địa)", "to": "Trung tâm Thượng Hải (Liên lục địa)", "value": 1800, "type": "outflow", "level": "Liên lục địa"},
    {"from": "Trung tâm Thượng Hải (Liên lục địa)", "to": "Trung tâm Singapore (Liên quốc gia)", "value": 1600, "type": "inflow", "level": "Liên lục địa"},
    {"from": "Trung tâm Singapore (Liên quốc gia)", "to": "Trung tâm Sydney (Úc)", "value": 1100, "type": "inflow", "level": "Liên quốc gia"},
    {"from": "Trung tâm New York (Liên lục địa)", "to": "Cảng Sao Paulo (Nam Mỹ)", "value": 1300, "type": "outflow", "level": "Liên lục địa"},
    {"from": "Khu mỏ Johannesburg (Nam Phi)", "to": "Trung tâm Thượng Hải (Liên lục địa)", "value": 1400, "type": "inflow", "level": "Liên lục địa"},
    {"from": "Trung tâm Sydney (Úc)", "to": "Trung tâm New York (Liên lục địa)", "value": 1200, "type": "outflow", "level": "Liên lục địa"},

    # --- CHẰNG CHỊT XUYÊN CẤP BẮC MỸ (Từ Thế giới -> Quốc gia -> Quận -> Làng quê Mỹ) ---
    {"from": "Trung tâm New York (Liên lục địa)", "to": "Bang California (Cấp Nhà nước)", "value": 900, "type": "inflow", "level": "Nhà nước"},
    {"from": "Bang California (Cấp Nhà nước)", "to": "Huyện Fresno (Cấp Huyện)", "value": 550, "type": "inflow", "level": "Huyện"},
    {"from": "Huyện Fresno (Cấp Huyện)", "to": "Thị trấn Lanare (Cấp Xã)", "value": 300, "type": "outflow", "level": "Xã"},
    {"from": "Thị trấn Lanare (Cấp Xã)", "to": "Trang trại Westlands (Nông thôn)", "value": 150, "type": "inflow", "level": "Nông thôn"},
    {"from": "Trang trại Westlands (Nông thôn)", "to": "Trung tâm New York (Liên lục địa)", "value": 400, "type": "inflow", "level": "Đan chéo toàn cầu"},

    # --- CHẰNG CHỊT XUYÊN CẤP CHÂU ÂU ---
    {"from": "Trung tâm London (Liên lục địa)", "to": "Vùng Bavaria Đức (Cấp Tỉnh)", "value": 850, "type": "inflow", "level": "Tỉnh"},
    {"from": "Vùng Bavaria Đức (Cấp Tỉnh)", "to": "Huyện Dingolfing (Cấp Huyện)", "value": 480, "type": "inflow", "level": "Huyện"},
    {"from": "Huyện Dingolfing (Cấp Huyện)", "to": "Xã Loiching (Cấp Xã)", "value": 200, "type": "outflow", "level": "Xã"},
    {"from": "Cánh đồng Nông nghiệp (Nông thôn Đan Mạch)", "to": "Trung tâm London (Liên lục địa)", "value": 500, "type": "inflow", "level": "Đan chéo toàn cầu"},

    # --- CHẰNG CHỊT XUYÊN CẤP CHÂU Á & TRUNG QUỐC ---
    {"from": "Trung tâm Thượng Hải (Liên lục địa)", "to": "Tỉnh Chiết Giang (Cấp Tỉnh)", "value": 950, "type": "outflow", "level": "Tỉnh"},
    {"from": "Tỉnh Chiết Giang (Cấp Tỉnh)", "to": "Huyện Nghĩa Ô (Cấp Huyện)", "value": 700, "type": "inflow", "level": "Huyện"},
    {"from": "Huyện Nghĩa Ô (Cấp Huyện)", "to": "Thị trấn Sục Khê (Cấp Xã)", "value": 410, "type": "inflow", "level": "Xã"},
    {"from": "Thị trấn Sục Khê (Cấp Xã)", "to": "Xưởng sản xuất Nông thôn (Trung Quốc)", "value": 250, "type": "outflow", "level": "Nông thôn"},
    {"from": "Xưởng sản xuất Nông thôn (Trung Quốc)", "to": "Trung tâm New York (Liên lục địa)", "value": 800, "type": "inflow", "level": "Đan chéo toàn cầu"},

    # --- CHẰNG CHỊT XUYÊN CẤP VIỆT NAM (Kết nối thẳng trục quốc tế) ---
    {"from": "Trung tâm Singapore (Liên quốc gia)", "to": "TP. Hồ Chí Minh (Trung ương)", "value": 950, "type": "inflow", "level": "Nhà nước"},
    {"from": "TP. Hồ Chí Minh (Trung ương)", "to": "An Giang (Cấp Tỉnh)", "value": 500, "type": "inflow", "level": "Tỉnh"},
    {"from": "An Giang (Cấp Tỉnh)", "to": "Huyện Thoại Sơn", "value": 300, "type": "inflow", "level": "Huyện"},
    {"from": "Huyện Thoại Sơn", "to": "Xã Thoại Giang", "value": 180, "type": "inflow", "level": "Xã"},
    {"from": "Xã Thoại Giang", "to": "Ấp Kênh Sáng (Nông thôn)", "value": 90, "type": "inflow", "level": "Nông thôn"},
    {"from": "Ấp Kênh Sáng (Nông thôn)", "to": "Trung tâm Singapore (Liên quốc gia)", "value": 350, "type": "outflow", "level": "Đan chéo toàn cầu"}
]

# Chuyển ma trận dữ liệu tọa độ
df_flows = pd.DataFrame(raw_flows)
df_flows["from_lat"] = df_flows["from"].map(lambda x: centers[x]["lat"])
df_flows["from_lon"] = df_flows["from"].map(lambda x: centers[x]["lon"])
df_flows["to_lat"] = df_flows["to"].map(lambda x: centers[x]["lat"])
df_flows["to_lon"] = df_flows["to"].map(lambda x: centers[x]["lon"])

# Hàm gán màu chuẩn: inflow -> Xanh ngọc phát sáng, outflow -> Đỏ ruby
def assign_flow_color(flow_type):
    if flow_type == "inflow":
        return 
    else:
        return 

df_flows["color"] = df_flows["type"].apply(assign_flow_color)

# 4. Định nghĩa lớp hiển thị các sợi dây vòng cung chằng chịt (ArcLayer)
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df_flows,
    get_source_position="[from_lon, from_lat]",
    get_target_position="[to_lon, to_lat]",
    get_source_color="color",
    get_target_color="color",
    get_width="value / 70",
    pickable=True,
    auto_highlight=True,
)

# 5. Định nghĩa lớp các nút thắt tròn vàng (ScatterplotLayer)
df_nodes = pd.DataFrame([{"name": k, **v} for k, v in centers.items()])
nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_nodes,
    get_position="[lon, lat]",
    get_color=,
    get_radius=8000,  # Kích thước tối ưu để nhìn bao quát toàn bộ thế giới phẳng
    pickable=True,
)

# 6. Cấu hình góc nhìn từ trên cao (Góc nhìn toàn cầu bao quát)
view_state = pdk.ViewState(
    latitude=20.0,
    longitude=0.0,
    zoom=1.2,   # Thu nhỏ tối đa để bao quát toàn lục địa Trái Đất cùng lúc
    pitch=40,   # Tạo độ nghiêng 3D để các đường đan chéo vồng lên chằng chịt
)

# 7. Khởi tạo bản đồ tổng lực
r = pdk.Deck(
    layers=[arc_layer, nodes_layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Mạch kinh tế:</b> {from} ➔ {to}<br/>"
                "<b>Bản chất cấp:</b> {level}<br/>"
                "<b>Trạng thái:</b> {type}<br/>"
                "<b>Quy mô dòng vốn:</b> {value} Tỷ USD",
        "style": {"backgroundColor": "#0A0D14", "color": "white", "borderRadius": "6px", "border": "1px solid #222"}
    }
)

st.pydeck_chart(r)

