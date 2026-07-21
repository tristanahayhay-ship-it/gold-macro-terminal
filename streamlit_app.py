import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Thiết lập giao diện Web
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu 3 Tầng",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Mạng lưới Dòng chảy Tiền tệ Đa tầng Toàn thế giới")
st.markdown("Hệ thống ma trận mô phỏng các luồng tiền tệ 3 tầng kết nối đan xen chằng chịt giữa tất cả các trung tâm kinh tế lớn trên thế giới.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
st.sidebar.header("⚙️ Kịch bản Khủng hoảng")
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng hệ thống)"]
)

# 3. Khai báo danh mục các quốc gia/khu vực lớn, mỗi nơi đều có đủ 3 tầng (Quốc gia - Tỉnh - Xã)
# Định dạng: [Vĩ độ, Kinh độ] để định vị trên bản đồ thế giới
hubs = {
    "MY": {
        "QUOC_GIA": [38.8951, -77.0364],      # Washington DC
        "TINH_KCN": [41.8781, -87.6298],      # Chicago (Công nghiệp)
        "XA_DAN": [36.7783, -119.4179],       # California (Nông thôn/Nông nghiệp)
        "name": "Mỹ (USA)"
    },
    "CHAU_AU": {
        "QUOC_GIA": [50.1109, 8.6821],        # Frankfurt (Đức)
        "TINH_KCN": [48.8566, 2.3522],        # Paris (Pháp)
        "XA_DAN": [41.9028, 12.4964],         # Ý (Nông thôn Nam Âu)
        "name": "Châu Âu (EU)"
    },
    "TRUNG_QUOC": {
        "QUOC_GIA": [39.9042, 116.4074],      # Bắc Kinh
        "TINH_KCN": [31.2304, 121.4737],      # Thượng Hải
        "XA_DAN": [30.6594, 104.0657],        # Thành Đô (Nông thôn nội địa)
        "name": "Trung Quốc (CN)"
    },
    "VIET_NAM": {
        "QUOC_GIA": [21.0285, 105.8542],      # Hà Nội
        "TINH_KCN": [16.0544, 108.2022],      # Đà Nẵng
        "XA_DAN": [10.8231, 106.6297],        # Vùng nông thôn Nam Bộ
        "name": "Việt Nam (VN)"
    },
    "NHAT_BAN": {
        "QUOC_GIA": [35.6762, 139.6503],      # Tokyo
        "TINH_KCN": [34.6937, 135.5023],      # Osaka
        "XA_DAN": [43.0621, 141.3544],        # Hokkaido
        "name": "Nhật Bản (JP)"
    }
}

# 4. Khởi tạo bản đồ thế giới phẳng
m = folium.Map(location=[30.0, 10.0], zoom_start=2.5, tiles="CartoDB positron")

# Vẽ tất cả các nút (Nodes) 3 tầng của TẤT CẢ các quốc gia lên bản đồ
for hub_code, layers in hubs.items():
    # Tầng 3: Quốc gia (Màu đỏ/xanh đậm)
    folium.CircleMarker(
        location=layers["QUOC_GIA"], radius=8, color="darkblue", fill=True,
        popup=f"🏛️ Tầng Vĩ mô: Ngân hàng Trung ương / Chính phủ {layers['name']}"
    ).add_to(m)
    
    # Tầng 2: Tỉnh/Khu công nghiệp (Màu cam)
    folium.CircleMarker(
        location=layers["TINH_KCN"], radius=6, color="orange", fill=True,
        popup=f"🏭 Tầng Trung mô: Cấp Tỉnh / Khu công nghiệp {layers['name']}"
    ).add_to(m)
    
    # Tầng 1: Xã/Hộ dân (Màu xanh lá)
    folium.CircleMarker(
        location=layers["XA_DAN"], radius=4, color="green", fill=True,
        popup=f"🏡 Tầng Vi mô: Cấp Xã / Hộ gia đình {layers['name']}"
    ).add_to(m)

# 5. Thuật toán tạo "Đường dây mạng lưới tài chính đa quốc gia" tự động theo kịch bản
if scenario == "Bình thường (Luân chuyển mở)":
    st.sidebar.success("🔵 Hệ thống đang vận hành thông suốt toàn cầu.")
    st.info("🔵 **Mạng lưới mở**: Tiền chảy đan xen xuyên quốc gia. Cấp Xã nước này xuất khẩu nông sản sang cấp Tỉnh nước khác. Vốn đầu tư của Ngân hàng Trung ương nước này đổ vào các khu công nghiệp toàn cầu.")
    
    # Vòng lặp liên kết nội bộ các quốc gia và đan chéo ra thế giới
    hub_keys = list(hubs.keys())
    for i, source_key in enumerate(hub_keys):
        src = hubs[source_key]
        
        # Luồng 1: Luân chuyển nội bộ 3 tầng của CHÍNH QUỐC GIA ĐÓ (Xã -> Tỉnh -> Quốc gia)
        folium.PolyLine([src["XA_DAN"], src["TINH_KCN"]], color="#1f77b4", weight=2, opacity=0.5).add_to(m)
        folium.PolyLine([src["TINH_KCN"], src["QUOC_GIA"]], color="#1f77b4", weight=2, opacity=0.5).add_to(m)
        
        # Luồng 2: Kết nối giao thương chéo sang QUỐC GIA KHÁC trên thế giới
        next_key = hub_keys[(i + 1) % len(hub_keys)]
        dest = hubs[next_key]
        
        # Tiền từ Vĩ mô nước giàu bơm vào công nghiệp nước đang phát triển
        folium.PolyLine([src["QUOC_GIA"], dest["TINH_KCN"]], color="#1f77b4", weight=3, opacity=0.6, tooltip=f"Vốn đầu tư từ {src['name']} sang {dest['name']}").add_to(m)
        # Tiền mua hàng hóa tiêu dùng từ Xã nước này sang nhà máy nước khác
        folium.PolyLine([src["XA_DAN"], dest["TINH_KCN"]], color="#7f7f7f", weight=1.5, opacity=0.4, tooltip="Giao thương thương mại quốc tế").add_to(m)

else:
    st.sidebar.danger("⚠️ Khủng hoảng dây chuyền toàn cầu.")
    st.error("⚠️ **Hiệu ứng Domino toàn cầu**: Khủng hoảng kích hoạt làn sóng 'rút rỗng' đồng loạt. Các đường dây chuyển dịch tài sản lập tức đổi hướng: Tiền từ các khu công nghiệp và vùng nông thôn của tất cả các nước bị 'xả' tháo chạy, dồn tất cả về tháp tài chính vĩ mô của Mỹ (Wall Street) và các kênh bảo hộ chính phủ.")
    
    hub_keys = list(hubs.keys())
    for source_key in hub_keys:
        src = hubs[source_key]
        
        # Luồng Đỏ (Xả ra): Tất cả các nước bị tháo chạy dòng vốn khỏi tầng sản xuất (Tỉnh) và tiêu dùng (Xã)
        folium.PolyLine([src["XA_DAN"], src["TINH_KCN"]], color="#d62728", weight=2, opacity=0.6).add_to(m)
        
        # Nếu không phải nước Mỹ, dòng tiền vĩ mô từ các nước khác sẽ bị xả để tháo chạy về Mỹ (Trú ẩn USD)
        if source_key != "MY":
            folium.PolyLine([src["QUOC_GIA"], hubs["MY"]["QUOC_GIA"]], color="#d62728", weight=4, opacity=0.7, tooltip=f"Vốn tháo chạy từ {src['name']} về tài sản an toàn của Mỹ").add_to(m)
            folium.PolyLine([src["TINH_KCN"], hubs["MY"]["QUOC_GIA"]], color="#d62728", weight=3, opacity=0.6, tooltip="Khối ngoại rút rỗng vốn đầu tư nhà máy").add_to(m)
        
        # Luồng Xanh (Đổ vào): Cơ chế phòng thủ nội địa riêng của từng nước (Chính phủ bơm tiền cứu doanh nghiệp của mình)
        folium.PolyLine([src["QUOC_GIA"], src["TINH_KCN"]], color="#2ca02c", weight=3, opacity=0.7, tooltip="Gói kích thích tài chính khẩn cấp nội địa").add_to(m)

# 6. Hiển thị Bản đồ lên giao diện Dashboard Web
col1, col2 = st.columns([1, 3]) # Cột bản đồ chiếm 75% chiều rộng màn hình để nhìn rõ toàn cầu

with col1:
    st.subheader("💡 Bản đồ Ma trận")
    st.markdown("""
    **Cấu trúc 3 chấm màu tại mỗi quốc gia:**
    *   🔵 **Chấm Đậm**: Cơ quan vĩ mô Trung ương.
    *   🟠 **Chấm Cam**: Khu công nghiệp / Cấp Tỉnh.
    *   🟢 **Chấm Nhỏ**: Người dân / Cấp Xã.
    """)
    
    st.subheader("📊 Quy luật dịch chuyển")
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng hệ thống)":
        st.markdown("""
        *   **Xả ra (Đường Đỏ) 🔴**: Tiền tháo chạy từ các mắt xích sản xuất toàn cầu đổ dồn về trung tâm tài chính Mỹ.
        *   **Đổ vào (Đường Xanh) 🟢**: Các đường dây cứu trợ nội bộ của riêng từng quốc gia tự cô lập để cứu dòng máu kinh tế của mình.
        """)
    else:
        st.markdown("*   **Mạng lưới Xanh dương 🔵**: Dòng chảy tiền tệ lưu thông tự do, kết nối đan chéo không biên giới.")

with col2:
    st.subheader("🗺️ Bản đồ Dòng chảy Tiền tệ Mạng lưới Toàn cầu")
    # Render bản đồ thế giới tương tác với chiều rộng tối đa
    st_folium(m, width=1100, height=700)
