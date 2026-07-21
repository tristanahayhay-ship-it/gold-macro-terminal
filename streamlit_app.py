import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Hệ thống Tài chính Ma trận Toàn cầu",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Ma trận Kinh tế Đa tầng Chi tiết Phủ kín Toàn cầu")
st.markdown("Hệ thống tự động sử dụng thuật toán hình học để sinh ra toàn bộ bộ máy tổ chức vi mô chi tiết cho tất cả quốc gia trên thế giới.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# 3. Danh sách tọa độ gốc vĩ mô của tất cả các quốc gia/khu vực lớn trên toàn bộ thế giới
world_countries = {
    "Mỹ (USA)": [38.8951, -77.0364],
    "Canada": [45.4215, -75.6972],
    "Brazil": [-15.7938, -47.8828],
    "Argentina": [-34.6037, -58.3816],
    "Anh (UK)": [51.5074, -0.1278],
    "Đức (EU)": [50.1109, 8.6821],
    "Pháp": [48.8566, 2.3522],
    "Nga": [55.7558, 37.6173],
    "Trung Quốc (CN)": [39.9042, 116.4074],
    "Nhật Bản (JP)": [35.6762, 139.6503],
    "Hàn Quốc": [37.5665, 126.9780],
    "Việt Nam (VN)": [21.0285, 105.8542],
    "Ấn Độ": [28.6139, 77.2090],
    "Úc": [-35.2809, 149.1300],
    "Nam Phi": [-25.7471, 28.1881],
    "Ai Cập": [30.0444, 31.2357],
    "Ả Rập Xê Út": [24.7136, 46.6753],
    "Singapore": [1.3521, 103.8198],
    "Indonesia": [-6.2088, 106.8456],
    "Thái Lan": [13.7563, 100.5018]
}

# Khởi tạo bản đồ nền phẳng 1 quả địa cầu duy nhất, khóa không cho lặp lại màn hình
m = folium.Map(
    location=[20.0, 20.0], 
    zoom_start=2.5, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(42)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

hubs_processed = {}

# 4. THUẬT TOÁN HÌNH HỌC TỰ ĐỘNG NHÂN BẢN BỘ MÁY CHI TIẾT CHO TOÀN THẾ GIỚI
for name, coords in world_countries.items():
    # Tự động tính toán khoảng cách địa lý riêng biệt cho 3 tầng hành chính (Quốc gia - Tỉnh - Xã)
    qg_center = coords
    tinh_center = [coords[0] - 4.0, coords[1] + 4.0]
    xa_center = [coords[0] - 8.0, coords[1] + 8.0]
    
    hubs_processed[name] = {
        "QUOC_GIA": qg_center,
        "CAP_TINH": tinh_center,
        "CAP_XA": xa_center
    }
    
    # --- A. TỰ ĐỘNG TẠO BỘ MÁY QUỐC GIA VI MÔ ---
    folium.Marker(
        location=qg_center, tooltip=f"🏛️ Bộ máy Trung ương - {name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(m)
    
    # Định vị các cơ quan nội bộ của Trung ương bằng thuật toán offset bán kính nhỏ
    nhtw_coord = [qg_center[0] - 0.4, qg_center[1] - 0.4]
    btc_coord = [qg_center[0] + 0.4, qg_center[1] + 0.4]
    
    folium.PolyLine([nhtw_coord, btc_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=nhtw_coord, radius=4, color="blue", fill=True, popup=f"Ngân hàng Trung ương / Hệ thống quản trị tiền tệ của {name}").add_to(m)
    folium.CircleMarker(location=btc_coord, radius=4, color="blue", fill=True, popup=f"Bộ Tài chính / Cơ quan quản lý ngân sách quốc gia của {name}").add_to(m)

    # --- B. TỰ ĐỘNG TẠO BỘ MÁY CẤP TỈNH VI MÔ ---
    folium.Marker(
        location=tinh_center, tooltip=f"🏭 Bộ máy Cấp Tỉnh - {name}",
        icon=folium.Icon(color="orange", icon="building", prefix="fa")
    ).add_to(m)
    
    # Trục kết nối huyết mạch từ Trung ương vĩ mô xuống Cấp Tỉnh trung mô
    folium.PolyLine([qg_center, tinh_center], color=color_flow, weight=3, opacity=0.7).add_to(m)
    
    # Định vị cơ quan nội bộ cấp Tỉnh
    cucthue_coord = [tinh_center[0] - 0.4, tinh_center[1] - 0.4]
    kcn_coord = [tinh_center[0] + 0.4, tinh_center[1] + 0.4]
    
    folium.PolyLine([cucthue_coord, kcn_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=cucthue_coord, radius=4, color="orange", fill=True, popup=f"Kho bạc & Cơ quan Thuế cấp Tỉnh địa phương tại {name}").add_to(m)
    folium.CircleMarker(location=kcn_coord, radius=4, color="orange", fill=True, popup=f"Ban quản lý Khu công nghiệp & Doanh nghiệp lớn cấp Tỉnh tại {name}").add_to(m)

    # --- C. TỰ ĐỘNG TẠO BỘ MÁY CẤP XÃ VI MÔ ---
    folium.Marker(
        location=xa_center, tooltip=f"🏡 Bộ máy Cấp Xã - {name}",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)
    
    # Trục kết nối huyết mạch từ Cấp Tỉnh xuống Cấp Xã vi mô nông thôn
    folium.PolyLine([tinh_center, xa_center], color=color_flow, weight=2.5, opacity=0.7).add_to(m)
    
    # Cơ chế phòng thủ khẩn cấp: Nếu có biến, Trung ương cứu trợ đi thẳng xuống Xã
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        folium.PolyLine([qg_center, xa_center], color=color_defense, weight=2.5, opacity=0.8, dash_array="10,10").add_to(m)

    # Định vị bộ phận cơ sở tại cấp Xã
    ubnd_coord = [xa_center[0] - 0.4, xa_center[1] - 0.4]
    hodan_coord = [xa_center[0] + 0.4, xa_center[1] + 0.4]
    
    folium.PolyLine([ubnd_coord, hodan_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=ubnd_coord, radius=4, color="green", fill=True, popup=f"Ủy ban Nhân dân xã / Cơ quan quản lý ngân sách cấp cơ sở tại {name}").add_to(m)
    folium.CircleMarker(location=hodan_coord, radius=4, color="green", fill=True, popup=f"Hộ gia đình nông dân / Đơn vị lao động, tiêu dùng vi mô tại {name}").add_to(m)

# 5. THUẬT TOÁN KẾT NỐI MA TRẬN DÒNG TIỀN XUYÊN LỤC ĐỊA GIỮA CÁC QUỐC GIA KHÁC NHAU
country_names = list(hubs_processed.keys())
for i, src_name in enumerate(country_names):
    src = hubs_processed[src_name]
    
    # Mỗi nước tự động liên kết giao thương vĩ mô chéo ngẫu nhiên với 2 nước khác trên toàn cầu
    targets = random.sample(country_names, 2)
    for dest_name in targets:
        if src_name != dest_name:
            dest = hubs_processed[dest_name]
            
            if scenario == "Bình thường (Luân chuyển mở)":
                # Bình thường: Các luồng tiền giao thương chảy thông suốt chéo từ Quốc gia này sang Tỉnh nước khác
                folium.PolyLine([src["QUOC_GIA"], dest["CAP_TINH"]], color="#1f77b4", weight=1.2, opacity=0.3).add_to(m)
            else:
                # Khủng hoảng: Tiền toàn cầu tháo chạy tháo mạng xả ra đổ dồn hết về Bộ máy vĩ mô của Mỹ (Wall Street)
                my_hubs = hubs_processed["Mỹ (USA)"]
                if src_name != "Mỹ (USA)":
                    folium.PolyLine([src["QUOC_GIA"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.5, opacity=0.35).add_to(m)
                    folium.PolyLine([src["CAP_TINH"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.5, opacity=0.35).add_to(m)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Web
col1, col2 = st.columns()

with col1:
    st.subheader("⚙️ Hướng dẫn Khảo sát Toàn cầu")
    st.markdown("""
    Thuật toán đã áp dụng cấu trúc đa tầng phân rã cho **TẤT CẢ các quốc gia trên thế giới** (Mỹ, Châu Âu, Châu Á, Châu Phi, Nam Mỹ...):
    *   **Cuộn chuột để di chuyển đến bất kỳ nước nào** trên thế giới (Ví dụ: Đức, Ấn Độ, Brazil, Nhật Bản...).
    *   **Phóng to (Zoom in)** vào nước đó, bạn sẽ thấy xuất hiện đầy đủ cấu trúc ghim biểu tượng kéo dài: 🏛️ Trung ương (Xanh) ➔ 🏭 Cấp Tỉnh (Cam) ➔ 🏡 Cấp Xã (Xanh lá).
    *   **Phóng to sâu nhất** vào từng ghim để nhấp chọn các chấm tròn vệ tinh xem chi tiết chức năng *Ngân hàng Nhà nước, Bộ tài chính, Cục thuế, Hộ dân...* của quốc gia đó.
    """)
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        st.error("🔴 Đường Đỏ: Dòng tiền sản xuất của tất cả các nước bị tháo chạy xuyên biên giới gom về nước Mỹ.")
        st.success("🟢 Đường Xanh lá: Gói kích thích khẩn cấp từ Trung ương đi thẳng xuống cứu trợ cấp Xã tại mỗi nước.")

with col2:
    st.subheader("🗺️ Bản đồ Ma trận Tài chính Đa tầng Toàn cầu")
    st_folium(m, width=1200, height=750)
