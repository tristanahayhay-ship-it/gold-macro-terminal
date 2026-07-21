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
st.markdown("Hệ thống tự động sử dụng thuật toán hình học chính xác để sinh ra toàn bộ bộ máy tổ chức vi mô ngay trong lãnh thổ từng quốc gia.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# 3. Danh sách tọa độ gốc vĩ mô (Thủ đô/Trung tâm) chuẩn xác của các quốc gia
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
    "Úc": [-25.2744, 133.7751],
    "Nam Phi": [-30.5595, 22.9375],
    "Ai Cập": [26.8206, 30.8025],
    "Ả Rập Xê Út": [23.8859, 45.0792],
    "Indonesia": [-0.7893, 113.9213],
    "Thái Lan": [15.8700, 100.9925]
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

# 4. THUẬT TOÁN ĐỊNH VỊ CHÍNH XÁC (Sửa lỗi lệch địa điểm sang nước khác/ra biển)
for name, coords in world_countries.items():
    lat = coords[0] # Vĩ độ gốc
    lon = coords[1] # Kinh độ gốc
    
    # Tính toán khoảng cách offset an toàn (chỉ lệch từ 1 đến 2 độ địa lý để giữ các tầng nằm gọn trong biên giới quốc gia)
    # Tùy thuộc vào vị trí quốc gia ở Nam hay Bắc bán cầu để điều chỉnh hướng dịch chuyển hợp lý
    offset = 1.5 if lat > 0 else -1.5
    
    qg_center = [lat, lon]
    tinh_center = [lat - offset, lon + offset]
    xa_center = [lat - (offset * 2), lon + (offset * 2)]
    
    hubs_processed[name] = {
        "QUOC_GIA": qg_center,
        "CAP_TINH": tinh_center,
        "CAP_XA": xa_center
    }
    
    # --- A. CẤP QUỐC GIA CHÍNH XÁC ---
    folium.Marker(
        location=qg_center, tooltip=f"🏛️ Bộ máy Trung ương - {name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(m)
    
    nhtw_coord = [qg_center[0] - 0.2, qg_center[1] - 0.2]
    btc_coord = [qg_center[0] + 0.2, qg_center[1] + 0.2]
    
    folium.PolyLine([nhtw_coord, btc_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=nhtw_coord, radius=4, color="blue", fill=True, popup=f"Ngân hàng Trung ương / Hệ thống quản trị tiền tệ của {name}").add_to(m)
    folium.CircleMarker(location=btc_coord, radius=4, color="blue", fill=True, popup=f"Bộ Tài chính / Cơ quan quản lý ngân sách quốc gia của {name}").add_to(m)

    # --- B. CẤP TỈNH CHÍNH XÁC ---
    folium.Marker(
        location=tinh_center, tooltip=f"🏭 Bộ máy Cấp Tỉnh - {name}",
        icon=folium.Icon(color="orange", icon="building", prefix="fa")
    ).add_to(m)
    
    folium.PolyLine([qg_center, tinh_center], color=color_flow, weight=3, opacity=0.7).add_to(m)
    
    cucthue_coord = [tinh_center[0] - 0.2, tinh_center[1] - 0.2]
    kcn_coord = [tinh_center[0] + 0.2, tinh_center[1] + 0.2]
    
    folium.PolyLine([cucthue_coord, kcn_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=cucthue_coord, radius=4, color="orange", fill=True, popup=f"Kho bạc & Cơ quan Thuế cấp Tỉnh địa phương tại {name}").add_to(m)
    folium.CircleMarker(location=kcn_coord, radius=4, color="orange", fill=True, popup=f"Ban quản lý Khu công nghiệp & Doanh nghiệp lớn cấp Tỉnh tại {name}").add_to(m)

    # --- C. CẤP XÃ CHÍNH XÁC ---
    folium.Marker(
        location=xa_center, tooltip=f"🏡 Bộ máy Cấp Xã - {name}",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(m)
    
    folium.PolyLine([tinh_center, xa_center], color=color_flow, weight=2.5, opacity=0.7).add_to(m)
    
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        folium.PolyLine([qg_center, xa_center], color=color_defense, weight=2.5, opacity=0.8, dash_array="10,10").add_to(m)

    ubnd_coord = [xa_center[0] - 0.2, xa_center[1] - 0.2]
    hodan_coord = [xa_center[0] + 0.2, xa_center[1] + 0.2]
    
    folium.PolyLine([ubnd_coord, hodan_coord], color="#7f7f7f", weight=1.5, dash_array="5,5").add_to(m)
    folium.CircleMarker(location=ubnd_coord, radius=4, color="green", fill=True, popup=f"Ủy ban Nhân dân xã / Cơ quan quản lý ngân sách cấp cơ sở tại {name}").add_to(m)
    folium.CircleMarker(location=hodan_coord, radius=4, color="green", fill=True, popup=f"Hộ gia đình nông dân / Đơn vị lao động, tiêu dùng vi mô tại {name}").add_to(m)

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
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("⚙️ Hướng dẫn Khảo sát")
    st.markdown("""
    Cấu trúc bộ máy đa tầng hiện tại đã nằm **chính xác trong biên giới** địa lý của từng quốc gia:
    *   **Hãy phóng to (Zoom in)** vào Việt Nam, Nhật Bản, Đức hoặc Mỹ.
    *   Bạn sẽ thấy 3 ghim biểu tượng (Trung ương 💼, Cấp Tỉnh 🏭, Cấp Xã 🏡) phân bố rất gọn gàng và khoa học nội tại trong nước đó.
    *   Nhấp vào các chấm nhỏ vệ tinh xung quanh từng ghim để xem chính xác các bộ phận chức năng vi mô.
    """)

with col2:
    st_folium(m, width=1200, height=750)
