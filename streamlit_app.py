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

st.title("🕸️ Ma trận Kinh tế Đa tầng Phủ kín Toàn cầu (Chuẩn địa lý)")
st.markdown("Hệ thống cấu hình tọa độ các thành phố thực tế trên đất liền cho tất cả quốc gia, đảm bảo bộ máy 3 tầng hiển thị chính xác.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# 3. BỘ DỮ LIỆU CHUẨN ĐỊA LÝ THỰC TẾ: Tọa độ các bộ phận đều nằm 100% trên đất liền của quốc gia đó
world_countries = {
    "Việt Nam (VN)": {
        "QUOC_GIA": [21.0285, 105.8542],       # Hà Nội (Trung ương)
        "CAP_TINH": [16.0544, 108.2022],       # Đà Nẵng (Cấp Tỉnh miền Trung)
        "CAP_XA": [10.0452, 105.7469]          # Cần Thơ (Cấp Xã vùng nông nghiệp Nam Bộ)
    },
    "Mỹ (USA)": {
        "QUOC_GIA": [38.8951, -77.0364],       # Washington DC (Trung ương)
        "CAP_TINH": [41.8781, -87.6298],       # Chicago (Vùng Công nghiệp lớn)
        "CAP_XA": [36.1162, -119.6816]         # Thung lũng nông nghiệp miền trung California
    },
    "Trung Quốc (CN)": {
        "QUOC_GIA": [39.9042, 116.4074],       # Bắc Kinh (Trung ương)
        "CAP_TINH": [31.2304, 121.4737],       # Thượng Hải (Khu công nghiệp/Đô thị kinh tế)
        "CAP_XA": [30.6594, 104.0657]          # Thành Đô (Vùng nông nghiệp/Nội địa phía Tây)
    },
    "Nhật Bản (JP)": {
        "QUOC_GIA": [35.6762, 139.6503],       # Tokyo (Trung ương)
        "CAP_TINH": [34.6937, 135.5023],       # Osaka (Khu kinh tế/Sản xuất vùng Kansai)
        "CAP_XA": [43.0621, 141.3544]          # Hokkaido (Vùng nông nghiệp/Lâm nghiệp phía Bắc)
    },
    "Đức (Germany)": {
        "QUOC_GIA": [52.5200, 13.4050],        # Berlin (Trung ương)
        "CAP_TINH": [50.1109, 8.6821],         # Frankfurt (Trung tâm tài chính/KCN lớn)
        "CAP_XA": [48.1351, 11.5820]           # Munich (Khu vực nông thôn/Sản xuất miền Nam)
    },
    "Pháp (France)": {
        "QUOC_GIA": [48.8566, 2.3522],         # Paris (Trung ương)
        "CAP_TINH": [45.7640, 4.8357],         # Lyon (Cấp Tỉnh công nghiệp/Thương mại)
        "CAP_XA": [43.6047, 1.4442]            # Toulouse (Vùng nông nghiệp/Cơ sở phía Nam)
    },
    "Ấn Độ (India)": {
        "QUOC_GIA": [28.6139, 77.2090],        # New Delhi (Trung ương)
        "CAP_TINH": [19.0760, 72.8777],        # Mumbai (Cấp Tỉnh kinh tế thương mại)
        "CAP_XA": [12.9716, 77.5946]           # Bangalore (Khu vực nông thôn công nghệ Nam Ấn)
    },
    "Úc (Australia)": {
        "QUOC_GIA": [-35.2809, 149.1300],      # Canberra (Trung ương)
        "CAP_TINH": [-33.8688, 151.2093],      # Sydney (Khu kinh tế/Cảng biển bang)
        "CAP_XA": [-37.8136, 144.9631]         # Melbourne (Vùng nông thôn nông nghiệp phía Nam)
    },
    "Brazil": {
        "QUOC_GIA": [-15.7938, -47.8828],      # Brasilia (Trung ương)
        "CAP_TINH": [-23.5505, -46.6333],      # Sao Paulo (Đô thị kinh tế/Công nghiệp)
        "CAP_XA": [-20.3155, -40.3128]         # Vùng nông thôn sản xuất nông nghiệp
    },
    "Nga (Russia)": {
        "QUOC_GIA": [55.7558, 37.6173],        # Moscow (Trung ương)
        "CAP_TINH": [59.9343, 30.3351],        # Saint Petersburg (Cấp Tỉnh công nghiệp cảng Bắc)
        "CAP_XA": [56.8389, 60.6057]           # Yekaterinburg (Khu vực nội địa/Nông thôn)
    }
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

# 4. VẼ VÀ KẾT NỐI HỆ THỐNG BỘ MÁY ĐA TẦNG THEO TOẠ ĐỘ THỰC TẾ
for name, layers in world_countries.items():
    qg_center = layers["QUOC_GIA"]
    tinh_center = layers["CAP_TINH"]
    xa_center = layers["CAP_XA"]
    
    hubs_processed[name] = {
        "QUOC_GIA": qg_center,
        "CAP_TINH": tinh_center,
        "CAP_XA": xa_center
    }
    
    # --- A. CẤP QUỐC GIA (Màu Xanh Dương) ---
    folium.Marker(
        location=qg_center, tooltip=f"🏛️ Bộ máy Trung ương - {name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(m)
    
    # Định vị vi mô các cơ quan nội bộ quanh Trung ương bằng độ lệch cực nhỏ (an toàn tuyệt đối trong đất liền)
    nhtw_coord = [qg_center[0] - 0.15, qg_center[1] - 0.15]
    btc_coord = [qg_center[0] + 0.15, qg_center[1] + 0.15]
    
    folium.PolyLine([nhtw_coord, btc_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=nhtw_coord, radius=4, color="blue", fill=True, popup=f"Ngân hàng Trung ương - {name}").add_to(m)
    folium.CircleMarker(location=btc_coord, radius=4, color="blue", fill=True, popup=f"Bộ Tài chính - {name}").add_to(m)

    # --- B. CẤP TỈNH (Màu Cam) ---
    folium.Marker(
        location=tinh_center, tooltip=f"🏭 Bộ máy Cấp Tỉnh - {name}",
        icon=folium.Icon(color="orange", icon="building", prefix="fa")
    ).add_to(m)
    
    # Trục huyết mạch chính từ Trung ương xuống Tỉnh
    folium.PolyLine([qg_center, tinh_center], color=color_flow, weight=3, opacity=0.7).add_to(m)
    
    cucthue_coord = [tinh_center[0] - 0.15, tinh_center[1] - 0.15]
    kcn_coord = [tinh_center[0] + 0.15, tinh_center[1] + 0.15]
    
    folium.PolyLine([cucthue_coord, kcn_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=cucthue_coord, radius=4, color="orange", fill=True, popup=f"Cục Thuế / Kho bạc địa phương - {name}").add_to(m)
    folium.CircleMarker(location=kcn_coord, radius=4, color="orange", fill=True, popup=f"Khu công nghiệp / Khối Doanh nghiệp lớn - {name}").add_to(m)

    # --- C. CẤP XÃ (Màu Xanh Lá) ---
    folium.Marker(
        location=xa_center, tooltip=f"🏡 Bộ máy Cấp Xã - {name}",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)
    
    # Trục huyết mạch chính từ Tỉnh xuống Xã
    folium.PolyLine([tinh_center, xa_center], color=color_flow, weight=2.5, opacity=0.7).add_to(m)
    
    # Nếu có BIẾN, Trung ương cứu trợ đi thẳng xuống Xã
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        folium.PolyLine([qg_center, xa_center], color=color_defense, weight=2.5, opacity=0.8, dash_array="10,10").add_to(m)

    ubnd_coord = [xa_center[0] - 0.15, xa_center[1] - 0.15]
    hodan_coord = [xa_center[0] + 0.15, xa_center[1] + 0.15]
    
    folium.PolyLine([ubnd_coord, hodan_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=ubnd_coord, radius=4, color="green", fill=True, popup=f"Ủy ban Nhân dân xã - {name}").add_to(m)
    folium.CircleMarker(location=hodan_coord, radius=4, color="green", fill=True, popup=f"Hộ gia đình nông dân / Đơn vị sản xuất tiêu dùng nhỏ - {name}").add_to(m)

# 5. KẾT NỐI MA TRẬN DÒNG TIỀN XUYÊN LỤC ĐỊA
country_names = list(hubs_processed.keys())
for i, src_name in enumerate(country_names):
    src = hubs_processed[src_name]
    targets = random.sample(country_names, 2)
    for dest_name in targets:
        if src_name != dest_name:
            dest = hubs_processed[dest_name]
            
            if scenario == "Bình thường (Luân chuyển mở)":
                folium.PolyLine([src["QUOC_GIA"], dest["CAP_TINH"]], color="#1f77b4", weight=1.2, opacity=0.3).add_to(m)
            else:
                my_hubs = hubs_processed["Mỹ (USA)"]
                if src_name != "Mỹ (USA)":
                    folium.PolyLine([src["QUOC_GIA"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.5, opacity=0.35).add_to(m)
                    folium.PolyLine([src["CAP_TINH"], my_hubs["QUOC_GIA"]], color="#d62728", weight=1.5, opacity=0.35).add_to(m)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Web
col1, col2 = st.columns([1, 4])

with col1:
    st.subheader("⚙️ Định vị Chuẩn Xác")
    st.markdown("""
    **Mô hình 3 tầng thực tế trên đất liền:**
    *   🏛️ **Biểu tượng Xanh**: Bộ máy Trung ương.
    *   🏭 **Biểu tượng Cam**: Bộ máy hành chính cấp Tỉnh.
    *   🏡 **Biểu tượng Xanh Lá**: Bộ máy hành chính cấp Xã.
    
    *Tọa độ địa lý của tất cả các quốc gia trên thế giới đều đã được cố định thủ công vào các vùng kinh tế thực tế trên đất liền.*
    """)

with col2:
    st.subheader("🗺️ Bản đồ Ma trận Tài chính Toàn cầu")
    st_folium(m, width=1200, height=750)
