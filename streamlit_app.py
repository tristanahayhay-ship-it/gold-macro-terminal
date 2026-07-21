import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import GroupedLayerControl
import random
import math

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu 3 Tầng",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Ma trận Kinh tế Đa tầng Tương tác Mượt mà Toàn cầu")
st.markdown("Đã sửa lỗi nhấp nháy. Bây giờ bạn có thể tự do phóng to/thu nhỏ mượt mà. Hãy tích/bỏ tích các tầng kinh tế ở bảng điều khiển góc phải bản đồ!")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

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

# Khởi tạo bản đồ nền phẳng, khóa không cho lặp màn hình ngang
m = folium.Map(
    location=[20.0, 20.0], 
    zoom_start=3, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(100)
color_flow = "#1f77b4" if scenario == "Bình Buddhist (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

# ĐỊNH NGHĨA CÁC LỚP BẢN ĐỒ CHUYÊN NGHIỆP (Feature Groups)
# Giúp người dùng có thể bật/tắt thủ công hoặc tự động hiển thị theo nhu cầu
fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)", show=True).add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)", show=True).add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)", show=True).add_to(m)

hubs_processed = {}

# 4. THUẬT TOÁN ĐỊNH VỊ ĐA ĐIỂM TOÀN CẦU
for name, coords in world_countries.items():
    lat_qg = coords
    lon_qg = coords
    
    # 🏛️ Gắn vào lớp Quốc gia
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
        
        # 🏭 Gắn vào lớp Cấp Tỉnh
        folium.Marker(
            location=tinh_coords, 
            tooltip=f"🏭 Bộ máy Cấp Tỉnh {t+1} - {name}",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(fg_cap_tinh)
        
        # Mạch tiền vĩ mô kết nối Trung ương -> Tỉnh
        folium.PolyLine([[lat_qg, lon_qg], tinh_coords], color=color_flow, weight=2.5, opacity=0.7).add_to(fg_cap_tinh)
        
        # Sinh dữ liệu các Xã trực thuộc từng Tỉnh
        for x in range(2):
            angle_xa = math.radians(angle_base + (t * 120) + (x * 60) + random.randint(-10, 10))
            dist_xa = 1.2 + random.uniform(0.2, 0.6)
            
            lat_xa = lat_tinh + dist_xa * math.sin(angle_xa)
            lon_xa = lon_tinh + dist_xa * math.cos(angle_xa)
            xa_coords = [lat_xa, lon_xa]
            
            # 🏡 Gắn vào lớp Cấp Xã
            folium.Marker(
                location=xa_coords, 
                tooltip=f"🏡 Bộ máy Cấp Xã {x+1} thuộc Tỉnh {t+1} - {name}",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(fg_cap_xa)
            
            # Mạch tiền vi mô kết nối Tỉnh -> Xã
            folium.PolyLine([tinh_coords, xa_coords], color=color_flow, weight=1.8, opacity=0.6).add_to(fg_cap_xa)
            
            # Nếu có biến, Trung ương cứu trợ đi thẳng xuống Xã
            if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
                folium.PolyLine([[lat_qg, lon_qg], xa_coords], color=color_defense, weight=1.8, opacity=0.7, dash_array="6,6").add_to(fg_cap_xa)

# 5. MA TRẬN GIAO THƯƠNG QUỐC TẾ XUYÊN LỤC ĐỊA (Nằm ở lớp vĩ mô)
country_names = list(hubs_processed.keys())
for i, src_name in enumerate(country_names):
    src = hubs_processed[src_name]
    targets = random.sample(country_names, 2)
    for dest_name in targets:
        if src_name != dest_name:
            dest = hubs_processed[dest_name]
            
            if scenario == "Bình thường (Luân chuyển mở)":
                if len(dest["TINH_LIST"]) > 0:
                    random_tinh = random.choice(dest["TINH_LIST"])
                    folium.PolyLine([src["QUOC_GIA"], random_tinh], color="#1f77b4", weight=1.0, opacity=0.25).add_to(fg_quoc_gia)
            else:
                my_hubs = hubs_processed["Mỹ (USA)"]
                if src_name != "Mỹ (USA)":
                    folium.PolyLine([src["QUOC_GIA"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.2, opacity=0.35).add_to(fg_quoc_gia)

# 6. BỘ ĐIỀU KHIỂN LỚP (Layer Control) TỰ ĐỘNG CỦA FOLIUM
# Cho phép người dùng trực tiếp bật/tắt hoặc bản đồ tự tối ưu hóa hiển thị mà không cần load lại trang
folium.LayerControl(position="topright", collapsed=False).add_to(m)

# 7. Đẩy cấu trúc hiển thị lên trang Streamlit Web
col1, col2 = st.columns([1, 4]) # Chia tỷ lệ: cột chú giải chiếm 1 phần, cột bản đồ chiếm 4 phần rất rộng

with col1:
    st.subheader("💡 Thanh quản lý tầng")
    st.markdown("""
    Ở **góc trên bên phải bản đồ** có một hộp màu trắng chứa danh sách các tầng. Bạn có thể:
    *   Tích/Bỏ tích lớp **Cấp Xã** hoặc **Cấp Tỉnh** để ẩn bớt ghim khi nhìn xa toàn cầu.
    *   **Lăn chuột zoom vô tư** mà không còn bị giật, lag hay nhấp nháy màn hình nữa!
    """)
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        st.error("🔴 Đường Đỏ: Tháo chạy dòng vốn.")
        st.success("🟢 Đường Xanh lá: Cứu trợ khẩn cấp vĩ mô.")

with col2:
    # Sử dụng st_folium nguyên bản, không dùng hàm kiểm soát zoom từ python để triệt tiêu lỗi nhấp nháy
    st_folium(m, width=1250, height=780, returned_objects=[])
