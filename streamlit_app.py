import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Hợp nhất",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Mạng lưới Dòng chảy Tiền tệ Phủ kín Toàn cầu")
st.markdown("Hệ thống sử dụng thuật toán mạng nhện để tự động tạo ra các đường dây dòng chảy tài chính 3 tầng kết nối toàn bộ các châu lục trên thế giới.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
st.sidebar.header("⚙️ Kịch bản Khủng hoảng")
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở toàn cầu)", "Khi Toàn cầu có BIẾN (Khủng hoảng hệ thống)"]
)

# 3. Bộ dữ liệu mở rộng: Danh sách tọa độ trung tâm của các quốc gia
world_countries = {
    "Mỹ (USA)": [38.8951, -77.0364],
    "Canada": [45.4215, -75.6972],
    "Brazil": [-15.7938, -47.8828],
    "Argentina": [-34.6037, -58.3816],
    "Anh (UK)": [51.5074, -0.1278],
    "Châu Âu (EU - Đức)": [50.1109, 8.6821],
    "Pháp": [48.8566, 2.3522],
    "Nga": [55.7558, 37.6173],
    "Trung Quốc (CN)": [39.9042, 116.4074],
    "Nhật Bản (JP)": [35.6762, 139.6503],
    "Hàn Quốc": [37.5665, 126.9780],
    "Việt Nam (VN)": [21.0285, 105.8542],
    "Ấn Độ": [28.6139, 77.2090],
    "Úc (Australia)": [-35.2809, 149.1300],
    "Nam Phi": [-25.7471, 28.1881],
    "Ai Cập": [30.0444, 31.2357],
    "Ả Rập Xê Út": [24.7136, 46.6753],
    "Singapore": [1.3521, 103.8198],
    "Indonesia": [-6.2088, 106.8456],
    "Thái Lan": [13.7563, 100.5018]
}

# KHẮC PHỤC LỖI: Thêm no_wrap=True và max_bounds=True để bản đồ không bị nhân bản lặp lại
m = folium.Map(
    location=[20.0, 0.0], 
    zoom_start=2, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

# Thiết lập hạt giống ngẫu nhiên
random.seed(42)

# 4. Vẽ các nút (Nodes) 3 tầng cho TẤT CẢ các quốc gia
hubs_processed = {}
for name, coords in world_countries.items():
    quoc_gia = coords
    tinh_kcn = [coords[0] - 1.5, coords[1] + 1.5]
    xa_dan = [coords[0] - 3.0, coords[1] + 3.0]
    
    hubs_processed[name] = {
        "QUOC_GIA": quoc_gia,
        "TINH_KCN": tinh_kcn,
        "XA_DAN": xa_dan
    }
    
    # Vẽ Chấm Vĩ mô (Trung ương) - Xanh đậm
    folium.CircleMarker(
        location=quoc_gia, radius=6, color="darkblue", fill=True, fill_opacity=0.8,
        popup=f"🏛️ Vĩ mô: Trung ương / NHTW - {name}"
    ).add_to(m)
    
    # Vẽ Chấm Trung mô (Cấp Tỉnh/KCN) - Cam
    folium.CircleMarker(
        location=tinh_kcn, radius=4, color="orange", fill=True, fill_opacity=0.8,
        popup=f"🏭 Trung mô: Cấp Tỉnh / Khu công nghiệp - {name}"
    ).add_to(m)
    
    # Vẽ Chấm Vi mô (Cấp Xã/Hộ dân) - Xanh lá
    folium.CircleMarker(
        location=xa_dan, radius=3, color="green", fill=True, fill_opacity=0.8,
        popup=f"🏡 Vi mô: Cấp Xã / Hộ gia đình - {name}"
    ).add_to(m)

# 5. Thuật toán tạo "Mạng lưới đường dây tài chính"
country_names = list(hubs_processed.keys())

if scenario == "Bình thường (Luân chuyển mở toàn cầu)":
    st.info("🔵 **Mạng lưới toàn cầu thông suốt**: Tiền tệ luân chuyển tự do chằng chịt qua lại giữa mọi châu lục. Chuỗi cung ứng vĩ mô kết nối các vùng sản xuất cấp Tỉnh và tiêu dùng cấp Xã trên phạm vi toàn cầu.")
    
    for i, src_name in enumerate(country_names):
        src = hubs_processed[src_name]
        
        folium.PolyLine([src["XA_DAN"], src["TINH_KCN"]], color="#1f77b4", weight=1.5, opacity=0.4).add_to(m)
        folium.PolyLine([src["TINH_KCN"], src["QUOC_GIA"]], color="#1f77b4", weight=1.5, opacity=0.4).add_to(m)
        
        targets = random.sample(country_names, 3)
        for dest_name in targets:
            if src_name != dest_name:
                dest = hubs_processed[dest_name]
                folium.PolyLine(
                    locations=[src["QUOC_GIA"], dest["TINH_KCN"]],
                    color="#1f77b4", weight=1.2, opacity=0.3,
                    tooltip=f"Dòng tiền giao thương: {src_name} ➔ Khu công nghiệp {dest_name}"
                ).add_to(m)

else:
    st.error("⚠️ **Khủng hoảng hệ thống / Hiệu ứng Domino**: Toàn bộ các đường dây giao thương quốc tế bị tháo chạy. Dòng vốn từ khu công nghiệp (Tỉnh) và dòng tiền từ người dân (Xã) của tất cả các quốc gia đồng loạt 'xả ra' (Đường Đỏ) để rút về tài sản an toàn vĩ mô ở Mỹ (Wall Street). Các nước tự cô lập bằng cách bơm tiền nội địa (Đường Xanh lá).")
    
    my_hubs = hubs_processed["Mỹ (USA)"]
    
    for src_name in country_names:
        src = hubs_processed[src_name]
        
        folium.PolyLine([src["XA_DAN"], src["TINH_KCN"]], color="#d62728", weight=1.5, opacity=0.5).add_to(m)
        
        if src_name != "Mỹ (USA)":
            folium.PolyLine(
                locations=[src["QUOC_GIA"], my_hubs["QUOC_GIA"]],
                color="#d62728", weight=2.0, opacity=0.4,
                tooltip=f"Vốn tháo chạy: Trung ương {src_name} ➔ Trữ USD tại Mỹ"
            ).add_to(m)
            folium.PolyLine(
                locations=[src["TINH_KCN"], my_hubs["QUOC_GIA"]],
                color="#d62728", weight=1.8, opacity=0.4,
                tooltip=f"Rút rỗng dòng vốn đầu tư tại {src_name} về Mỹ"
            ).add_to(m)
        
        folium.PolyLine([src["QUOC_GIA"], src["TINH_KCN"]], color="#2ca02c", weight=2.0, opacity=0.6).add_to(m)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Cloud
col1, col2 = st.columns([1, 4]) # Điều chỉnh tỷ lệ cột để bản đồ có không gian hiển thị lớn nhất

with col1:
    st.subheader("💡 Chú giải Ma trận Toàn cầu")
    st.markdown("""
    *   🔵 **Chấm Đậm**: Trung ương quốc gia.
    *   🟠 **Chấm Cam**: Cấp Tỉnh / Khu sản xuất.
    *   🟢 **Chấm Nhỏ**: Cấp Xã / Hộ tiêu dùng.
    """)
    st.subheader("📊 Quy luật dòng chảy")
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng hệ thống)":
        st.markdown("""
        *   🔴 **Đường Đỏ (Xả ra)**: Tiền tháo chạy từ mọi lục địa về Mỹ.
        *   🟢 **Đường Xanh lá (Đổ vào)**: Các nước tự bơm tiền cứu nội bộ.
        """)
    else:
        st.markdown("🔵 **Mạng lưới Xanh**: Tiền tệ toàn cầu tuần hoàn tự do.")

with col2:
    st.subheader("🗺️ Bản đồ Dòng chảy Tiền tệ Mạng lưới Toàn cầu")
    st_folium(m, width=1200, height=700)
