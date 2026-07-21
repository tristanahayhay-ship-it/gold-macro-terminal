import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Hợp nhất",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Ma trận Kinh tế Đa tầng & Mạng lưới Đa điểm Toàn cầu")
st.markdown("Hệ thống tự động sử dụng thuật toán phân rã ma trận để sinh ra mạng lưới gồm nhiều Tỉnh và nhiều Xã kết nối chằng chịt cho **TẤT CẢ** các quốc gia trên thế giới.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# 3. DANH SÁCH TỌA ĐỘ GỐC (THỦ ĐÔ/TRUNG TÂM) CỦA CÁC QUỐC GIA TRÊN THẾ GIỚI
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
    zoom_start=2.5, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

# Cố định hạt giống ngẫu nhiên để hình dáng mạng lưới không bị thay đổi loạn xạ khi bấm nút
random.seed(100)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

hubs_processed = {}

# 4. THUẬT TOÁN MULTI-POINT DECOMPOSITION: TỰ ĐỘNG SINH ĐA ĐIỂM TỈNH/XÃ CHO MỌI NƯỚC
for name, coords in world_countries.items():
    lat_qg = coords[0]
    lon_qg = coords[1]
    
    # Vẽ điểm nút vĩ mô: Trung ương / Quốc gia của nước đó
    folium.Marker(
        location=[lat_qg, lon_qg], 
        tooltip=f"🏛️ Trung ương vĩ mô - {name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(m)
    
    hubs_processed[name] = {"QUOC_GIA": [lat_qg, lon_qg], "TINH_LIST": []}
    
    # Thiết lập góc quay địa lý ngẫu nhiên nhưng bám sát đất liền tùy theo bán cầu
    angle_base = 0 if lat_qg > 0 else 180
    
    # Thuật toán tự động sinh 3 Tỉnh cho MỖI quốc gia
    for t in range(3):
        # Tính toán tọa độ Tỉnh lệch ra khỏi Thủ đô theo mô hình cánh quạt (Bán kính khoảng 250km - 400km)
        angle_tinh = math.radians(angle_base + (t * 120) + random.randint(-15, 15))
        dist_tinh = 2.5 + random.uniform(0.5, 1.5)
        
        lat_tinh = lat_qg + dist_tinh * math.sin(angle_tinh)
        lon_tinh = lon_qg + dist_tinh * math.cos(angle_tinh)
        tinh_coords = [lat_tinh, lon_tinh]
        
        hubs_processed[name]["TINH_LIST"].append(tinh_coords)
        
        # Vẽ điểm ghim bộ máy Cấp Tỉnh (Màu Cam)
        folium.Marker(
            location=tinh_coords, 
            tooltip=f"🏭 Bộ máy Cấp Tỉnh {t+1} - {name}",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(m)
        
        # Đường nối luồng tiền chính: Trung ương ➔ Cấp Tỉnh
        folium.PolyLine([[lat_qg, lon_qg], tinh_coords], color=color_flow, weight=2.5, opacity=0.7).add_to(m)
        
        # Thuật toán tự động sinh tiếp 2 Xã cho MỖI Tỉnh (Tổng cộng 6 Xã cho mỗi quốc gia)
        for x in range(2):
            angle_xa = math.radians(angle_base + (t * 120) + (x * 60) + random.randint(-10, 10))
            dist_xa = 1.2 + random.uniform(0.2, 0.6)
            
            lat_xa = lat_tinh + dist_xa * math.sin(angle_xa)
            lon_xa = lon_tinh + dist_xa * math.cos(angle_xa)
            xa_coords = [lat_xa, lon_xa]
            
            # Vẽ điểm ghim bộ máy Cấp Xã (Màu Xanh Lá)
            folium.Marker(
                location=xa_coords, 
                tooltip=f"🏡 Bộ máy Cấp Xã {x+1} thuộc Tỉnh {t+1} - {name}",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(m)
            
            # Đường nối luồng tiền vi mô: Cấp Tỉnh ➔ Cấp Xã nông thôn
            folium.PolyLine([tinh_coords, xa_coords], color=color_flow, weight=1.8, opacity=0.6).add_to(m)
            
            # Nếu có BIẾN, Trung ương kích hoạt gói cứu trợ bắn thẳng xuống các Xã cơ sở
            if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
                folium.PolyLine([[lat_qg, lon_qg], xa_coords], color=color_defense, weight=1.8, opacity=0.7, dash_array="6,6").add_to(m)

# 5. THUẬT TOÁN KẾT NỐI MA TRẬN DÒNG TIỀN GIAO THƯƠNG QUỐC TẾ XUYÊN LỤC ĐỊA
country_names = list(hubs_processed.keys())
for i, src_name in enumerate(country_names):
    src = hubs_processed[src_name]
    
    # Kết nối giao thương chéo quốc tế
    targets = random.sample(country_names, 2)
    for dest_name in targets:
        if src_name != dest_name:
            dest = hubs_processed[dest_name]
            
            if scenario == "Bình thường (Luân chuyển mở)":
                # Luồng tiền giao thương chảy từ Trung ương nước này sang 1 Tỉnh ngẫu nhiên của nước khác
                random_tinh = random.choice(dest["TINH_LIST"])
                folium.PolyLine([src["QUOC_GIA"], random_tinh], color="#1f77b4", weight=1.0, opacity=0.25).add_to(m)
            else:
                # Nếu có biến, dòng vốn vĩ mô từ các nước đồng loạt xả ra để tháo chạy về Mỹ (Wall Street)
                my_hubs = hubs_processed["Mỹ (USA)"]
                if src_name != "Mỹ (USA)":
                    folium.PolyLine([src["QUOC_GIA"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.2, opacity=0.35).add_to(m)
                    random_src_tinh = random.choice(src["TINH_LIST"])
                    folium.PolyLine([random_src_tinh, my_hubs["QUOC_GIA"]], color="#d62728", weight=1.2, opacity=0.35).add_to(m)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Web
col1, col2 = st.columns([1, 4]) # Chia tỷ lệ: 1 phần ghi chú giải, 4 phần hiển thị bản đồ siêu rộng

with col1:
    st.subheader("⚙️ Ma Trận Đa Điểm")
    st.markdown("""
    **Mô hình phân rã 100% các nước:**
    *   🏛️ **Biểu tượng Xanh**: Trung ương đầu não của nước đó.
    *   🏭 **Biểu tượng Cam**: Hệ thống gồm nhiều ghim cấp Tỉnh phân rã xung quanh.
    *   🏡 **Biểu tượng Xanh lá**: Hệ thống gồm nhiều xã bám sát theo từng Tỉnh.
    
    *Hãy cuộn chuột phóng to vào Mỹ, Đức, Nga, Trung Quốc, Ấn Độ... Bạn sẽ thấy mạng lưới đa điểm bủa vây phủ kín đất nước họ y hệt như Việt Nam.*
    """)

with col2:
    st.subheader("🗺️ Bản đồ Ma trận Tài chính Đa tầng & Đa điểm Toàn cầu")
    st_folium(m, width=1250, height=780)
