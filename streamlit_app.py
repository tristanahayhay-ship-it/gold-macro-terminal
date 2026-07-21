import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Phân tầng Zoom",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Ma trận Kinh tế Đa tầng Tự động Ẩn/Hiện theo Mức Zoom")
st.markdown("Hãy sử dụng nút cuộn chuột để phóng to: Phóng to vào Đất nước sẽ xuất hiện cấp Tỉnh, Phóng to sâu tiếp vào Tỉnh sẽ tự động bung ra cấp Xã!")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# Khởi tạo hoặc lấy mức zoom hiện tại từ bộ nhớ Streamlit (Mặc định bắt đầu từ mức 3)
if 'current_zoom' not in st.session_state:
    st.session_state['current_zoom'] = 3

st.sidebar.metric(label="🔎 Mức Zoom hiện tại", value=st.session_state['current_zoom'])

# 3. DANH SÁCH TỌA ĐỘ GỐC CỦA CÁC QUỐC GIA TRÊN THẾ GIỚI
world_countries = {
    "Việt Nam (VN)": [21.0285, 105.8542],
    "Mỹ (USA)": [38.8951, -77.0364],
    "Trung Quốc (CN)": [39.9042, 116.4074],
    "Nhật Bản (JP)": [35.6762, 139.6503],
    "Đức (Germany)": [52.5200, 13.4050],
    "Pháp (France)": [48.8566, 2.3522],
    "Ấn Độ (India)": [28.6139, 77.2090],
    "Úc (Australia)": [-25.2744, 133.7751],
    "Brazil": [-15.7938, -47.8828],
    "Nga (Russia)": [55.7558, 37.6173],
    "Canada": [45.4215, -75.6972],
    "Nam Phi": [-30.5595, 22.9375]
}

# Khởi tạo bản đồ nền phẳng 1 quả địa cầu duy nhất, khóa không cho lặp lại màn hình
m = folium.Map(
    location=[20.0, 20.0], 
    zoom_start=st.session_state['current_zoom'], 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(100)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

hubs_processed = {}

# 4. THUẬT TOÁN ĐIỀU KHIỂN ĐỘ ẨN/HIỆN (ZOOM FILTERING)
# Xác định trạng thái bật/tắt các tầng dựa trên mức zoom thực tế của người dùng
show_tinh = st.session_state['current_zoom'] >= 5  # Zoom >= 5: Thấy đất nước và cấp Tỉnh
show_xa = st.session_state['current_zoom'] >= 7    # Zoom >= 7: Thấy chi tiết sâu vào cấp Xã

# Tạo các nhóm quản lý lớp (Feature Groups) để gom cụm các đường dây và ghim lại với nhau
fg_quoc_gia = folium.FeatureGroup(name="Tầng Quốc gia (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="Tầng Cấp Xã (Vi mô)").add_to(m)

# Vòng lặp quét qua tất cả quốc gia trên thế giới
for name, coords in world_countries.items():
    lat_qg = coords[0]
    lon_qg = coords[1]
    
    # 🏛️ LUÔN HIỂN THỊ: Ghim bộ máy Trung ương vĩ mô
    folium.Marker(
        location=[lat_qg, lon_qg], 
        tooltip=f"🏛️ Trung ương vĩ mô - {name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(fg_quoc_gia)
    
    hubs_processed[name] = {"QUOC_GIA": [lat_qg, lon_qg], "TINH_LIST": []}
    angle_base = 0 if lat_qg > 0 else 180
    
    # Sinh dữ liệu các Tỉnh
    for t in range(3):
        angle_tinh = math.radians(angle_base + (t * 120) + random.randint(-15, 15))
        dist_tinh = 2.5 + random.uniform(0.5, 1.5)
        
        lat_tinh = lat_qg + dist_tinh * math.sin(angle_tinh)
        lon_tinh = lon_qg + dist_tinh * math.cos(angle_tinh)
        tinh_coords = [lat_tinh, lon_tinh]
        
        hubs_processed[name]["TINH_LIST"].append(tinh_coords)
        
        # 🏭 CHỈ HIỆN KHI ZOOM VÀO ĐẤT NƯỚC (show_tinh = True)
        if show_tinh:
            folium.Marker(
                location=tinh_coords, 
                tooltip=f"🏭 Bộ máy Cấp Tỉnh {t+1} - {name}",
                icon=folium.Icon(color="orange", icon="building", prefix="fa")
            ).add_to(fg_cap_tinh)
            
            # Đường nối mạch tiền vĩ mô: Trung ương ➔ Cấp Tỉnh
            folium.PolyLine([[lat_qg, lon_qg], tinh_coords], color=color_flow, weight=2.5, opacity=0.7).add_to(fg_cap_tinh)
        
        # Sinh dữ liệu các Xã trực thuộc từng Tỉnh
        for x in range(2):
            angle_xa = math.radians(angle_base + (t * 120) + (x * 60) + random.randint(-10, 10))
            dist_xa = 1.2 + random.uniform(0.2, 0.6)
            
            lat_xa = lat_tinh + dist_xa * math.sin(angle_xa)
            lon_xa = lon_tinh + dist_xa * math.cos(angle_xa)
            xa_coords = [lat_xa, lon_xa]
            
            # 🏡 CHỈ HIỆN KHI ZOOM VÀO SÂU CẤP TỈNH (show_xa = True)
            if show_xa:
                folium.Marker(
                    location=xa_coords, 
                    tooltip=f"🏡 Bộ máy Cấp Xã {x+1} thuộc Tỉnh {t+1} - {name}",
                    icon=folium.Icon(color="green", icon="home", prefix="fa")
                ).add_to(fg_cap_xa)
                
                # Đường nối mạch tiền vi mô: Cấp Tỉnh ➔ Cấp Xã
                folium.PolyLine([tinh_coords, xa_coords], color=color_flow, weight=1.8, opacity=0.6).add_to(fg_cap_xa)
                
                # Nếu có biến, Trung ương cứu trợ đi thẳng xuống Xã
                if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
                    folium.PolyLine([[lat_qg, lon_qg], xa_coords], color=color_defense, weight=1.8, opacity=0.7, dash_array="6,6").add_to(fg_cap_xa)

# 5. KẾT NỐI MA TRẬN DÒNG TIỀN GIAO THƯƠNG QUỐC TẾ XUYÊN LỤC ĐỊA (Luôn hiện ở mức vĩ mô)
country_names = list(hubs_processed.keys())
for i, src_name in enumerate(country_names):
    src = hubs_processed[src_name]
    targets = random.sample(country_names, 2)
    for dest_name in targets:
        if src_name != dest_name:
            dest = hubs_processed[dest_name]
            
            if scenario == "Bình thường (Luân chuyển mở)":
                if show_tinh and len(dest["TINH_LIST"]) > 0:
                    random_tinh = random.choice(dest["TINH_LIST"])
                    folium.PolyLine([src["QUOC_GIA"], random_tinh], color="#1f77b4", weight=1.0, opacity=0.25).add_to(fg_quoc_gia)
            else:
                my_hubs = hubs_processed["Mỹ (USA)"]
                if src_name != "Mỹ (USA)":
                    folium.PolyLine([src["QUOC_GIA"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.2, opacity=0.35).add_to(fg_quoc_gia)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Web và bắt sự kiện Zoom từ người dùng
col1, col2 = st.columns([1, 4]) # Chia tỷ lệ: 1 phần ghi chú giải, 4 phần hiển thị bản đồ siêu rộng

with col1:
    st.subheader("⚙️ Cơ Chế Kính Hiển Vi")
    st.markdown("""
    **Quy trình hiển thị tự động:**
    1.  🌍 **Zoom < 5**: Bản đồ thế giới sạch sẽ, chỉ hiển thị ghim đầu não 🏛️ **Trung ương Quốc gia**.
    2.  🇻🇳 **Zoom từ 5 đến 6**: Khi phóng to sát vào ranh giới một đất nước, bộ máy 🏭 **Cấp Tỉnh** cùng các mạch tiền vĩ mô mới bắt đầu bung ra.
    3.  🏡 **Zoom >= 7**: Khi tiếp tục phóng to sâu hẳn vào nội địa, mạng lưới bộ máy 🏡 **Cấp Xã** vi mô cơ sở cùng các đường cứu trợ đứt nét mới hiển thị chi tiết.
    """)
    
    st.info("💡 Bạn hãy lăn con cuộn chuột trực tiếp trên bản đồ sang bên phải để kiểm tra cơ chế chuyển đổi thông minh này.")

with col2:
    st.subheader("🗺️ Bản đồ Ma trận Tài chính Đa tầng Phân cấp Zoom (Zoom-Sensitive Matrix)")
    
    # Render bản đồ tương tác đồng thời bắt dữ liệu phản hồi (zoom_start) từ hành vi của người dùng
    map_data = st_folium(m, width=1200, height=750, key="global_financial_map")
    
    # THUẬT TOÁN BẮT SỰ KIỆN ZOOM: Nếu người dùng cuộn chuột phóng to/thu nhỏ, 
    # Streamlit sẽ đọc giá trị zoom mới và cập nhật lại trạng thái ẩn/hiện ngay lập tức
    if map_data and map_data.get("zoom") is not None:
        if map_data["zoom"] != st.session_state['current_zoom']:
            st.session_state['current_zoom'] = map_data["zoom"]
            st.rerun() # Kích hoạt vẽ lại bản đồ theo mức độ ẩn hiện mới
