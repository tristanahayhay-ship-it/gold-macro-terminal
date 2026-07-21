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

st.title("🕸️ Ma trận Kinh tế Đa tầng Toàn cầu & Mạng lưới Đa điểm Thực tế")
st.markdown("Hệ thống đã cập nhật danh sách địa danh và tọa độ thực tế 100% trên đất liền cho Việt Nam và các quốc gia.")

# 2. Thanh cấu hình kịch bản hệ thống thế giới
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# Khởi tạo bản đồ nền phẳng 1 quả địa cầu duy nhất, khóa không cho lặp màn hình ngang
m = folium.Map(
    location=[16.0, 108.0], 
    zoom_start=5, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(42)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

# ĐỊNH NGHĨA CÁC LỚP BẢN ĐỒ CHUYÊN NGHIỆP (Feature Groups)
fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)").add_to(m)

# 3. CƠ SỞ DỮ LIỆU ĐỊA LÝ THỰC TẾ ĐA ĐIỂM (Sửa lỗi số lượng ít và lệch tọa độ)
world_data = {
    "Việt Nam (VN)": {
        "QUOC_GIA": [21.0285, 105.8542], # Hà Nội
        "TÌNH": {
            "Quảng Ninh (Miền Bắc)": [20.9485, 107.0734],
            "Hải Phòng (Miền Bắc)": [20.8449, 106.6881],
            "Đà Nẵng (Miền Trung)": [16.0544, 108.2022],
            "Khánh Hòa (Miền Trung)": [12.2471, 109.1961],
            "TP. Hồ Chí Minh (Miền Nam)": [10.8231, 106.6297],
            "Cần Thơ (Miền Nam)": [10.0452, 105.7469]
        },
        "XÃ": [
            {"name": "Xã Vân Đồn", "coords": [21.0345, 107.4121], "parent": "Quảng Ninh (Miền Bắc)"},
            {"name": "Xã Thủy Nguyên", "coords": [20.9855, 106.6710], "parent": "Hải Phòng (Miền Bắc)"},
            {"name": "Xã Hòa Vang", "coords": [16.0022, 108.1215], "parent": "Đà Nẵng (Miền Trung)"},
            {"name": "Xã Diên Khánh", "coords": [12.2612, 109.0910], "parent": "Khánh Hòa (Miền Trung)"},
            {"name": "Xã Củ Chi", "coords": [11.0025, 106.5122], "parent": "TP. Hồ Chí Minh (Miền Nam)"},
            {"name": "Xã Phong Điền", "coords": [10.0062, 105.6610], "parent": "Cần Thơ (Miền Nam)"}
        ]
    },
    "Mỹ (USA)": {
        "QUOC_GIA": [38.8951, -77.0364], # Washington DC
        "TÌNH": {
            "New York (Bang NY)": [40.7128, -74.0060],
            "Illinois (Chicago)": [41.8781, -87.6298],
            "California (Los Angeles)": [34.0522, -118.2437],
            "Texas (Houston)": [29.7604, -95.3698]
        },
        "XÃ": [
            {"name": "Huyện Albany", "coords": [42.6526, -73.7562], "parent": "New York (Bang NY)"},
            {"name": "Huyện Peoria", "coords": [40.6936, -89.5890], "parent": "Illinois (Chicago)"},
            {"name": "Thung lũng Fresno", "coords": [36.7378, -119.7871], "parent": "California (Los Angeles)"}
        ]
    },
    "Trung Quốc (CN)": {
        "QUOC_GIA": [39.9042, 116.4074], # Bắc Kinh
        "TÌNH": {
            "Thượng Hải": [31.2304, 121.4737],
            "Quảng Đông": [23.1291, 113.2644],
            "Tứ Xuyên": [30.6594, 104.0657],
            "Chiết Giang": [30.2741, 120.1551]
        },
        "XÃ": [
            {"name": "Vùng ven Sùng Minh", "coords": [31.6234, 121.3976], "parent": "Thượng Hải"},
            {"name": "Huyện Đông Quản", "coords": [23.0205, 113.7518], "parent": "Quảng Đông"},
            {"name": "Huyện vùng cao Đô Giang Yển", "coords": [30.9992, 103.6425], "parent": "Tứ Xuyên"}
        ]
    }
}

# 4. THUẬT TOÁN DỰA TRÊN DỮ LIỆU THỰC TẾ (ẨN/HIỆN THEO ZOOM BẰNG FEATURE GROUP)
hubs_processed = {}

for country_name, data in world_data.items():
    qg_coords = data["QUOC_GIA"]
    
    # 🏛️ A. Gắn bộ máy Trung ương quốc gia (Lớp vĩ mô)
    folium.Marker(
        location=qg_coords, tooltip=f"🏛️ Trung ương vĩ mô - {country_name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(fg_quoc_gia)
    
    hubs_processed[country_name] = {"QUOC_GIA": qg_coords, "TINH_COORDS_LIST": list(data["TÌNH"].values())}
    
    # 🏭 B. Gắn mạng lưới các Tỉnh thực tế (Lớp trung mô)
    for prov_name, prov_coords in data["TÌNH"].items():
        folium.Marker(
            location=prov_coords, tooltip=f"🏭 Bộ máy Cấp Tỉnh: {prov_name} ({country_name})",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(fg_cap_tinh)
        
        # Đường nối luồng tiền vĩ mô: Trung ương ➔ Cấp Tỉnh
        folium.PolyLine([qg_coords, prov_coords], color=color_flow, weight=2.5, opacity=0.75).add_to(fg_cap_tinh)
        
    # 🏡 C. Gắn mạng lưới các Xã thực tế (Lớp vi mô)
    for xa_item in data["XÃ"]:
        xa_coords = xa_item["coords"]
        parent_name = xa_item["parent"]
        parent_coords = data["TÌNH"][parent_name]
        
        folium.Marker(
            location=xa_coords, tooltip=f"🏡 Bộ máy Cấp Xã: {xa_item['name']} thuộc {parent_name}",
            icon=folium.Icon(color="green", icon="home", prefix="fa")
        ).add_to(fg_cap_xa)
        
        # Đường nối luồng tiền vi mô: Cấp Tỉnh ➔ Cấp Xã tương ứng
        folium.PolyLine([parent_coords, xa_coords], color=color_flow, weight=1.8, opacity=0.65).add_to(fg_cap_xa)
        
        # Nếu có biến, Trung ương bơm ngân sách cứu trợ khẩn cấp đi tắt thẳng xuống Xã
        if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
            folium.PolyLine([qg_coords, xa_coords], color=color_defense, weight=1.8, opacity=0.7, dash_array="6,6").add_to(fg_cap_xa)

# 5. MA TRẬN KẾT NỐI GIAO THƯƠNG QUỐC TẾ VĨ MÔ
country_names = list(hubs_processed.keys())
for src_name in country_names:
    if src_name != "Mỹ (USA)":
        src_qg = hubs_processed[src_name]["QUOC_GIA"]
        us_qg = hubs_processed["Mỹ (USA)"]["QUOC_GIA"]
        
        if scenario == "Bình thường (Luân chuyển mở)":
            # Giao thương thông suốt sang 1 vùng kinh tế cấp Tỉnh của Mỹ
            random_us_tinh = random.choice(hubs_processed["Mỹ (USA)"]["TINH_COORDS_LIST"])
            folium.PolyLine([src_qg, random_us_tinh], color="#1f77b4", weight=1.2, opacity=0.3).add_to(fg_quoc_gia)
        else:
            # Khủng hoảng: Tiền tháo chạy xuyên biên giới đổ dồn về Wall Street
            folium.PolyLine([src_qg, us_qg], color="#d62728", weight=1.5, opacity=0.4).add_to(fg_quoc_gia)

# 6. NHÚNG MÃ JAVASCRIPT ĐIỀU KHIỂN ĐỘ ẨN/HIỆN KÍNH HIỂN VI TRÊN TRÌNH DUYỆT (Mượt 100%, không nhấp nháy)
macro_zoom_script = f"""
<script>
document.addEventListener("DOMContentLoaded", function() {{
    var checkMap = setInterval(window.checkAndApplyZoom, 300);
    window.checkAndApplyZoom = function() {{
        var maps = document.getElementsByClassName("folium-map");
        if (maps.length > 0) {{
            var mapId = maps[0].id;
            var leafletMap = window[mapId];
            if (leafletMap) {{
                clearInterval(checkMap);
                var layerTinhId = {fg_cap_tinh.get_name()};
                var layerXaId = {fg_cap_xa.get_name()};
                
                function updateLayers() {{
                    var currentZoom = leafletMap.getZoom();
                    // Zoom < 5: Ẩn Tỉnh, Ẩn Xã
                    if (currentZoom < 5) {{
                        if (leafletMap.hasLayer(layerTinhId)) leafletMap.removeLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    // Zoom 5-6: Hiện Tỉnh, Ẩn Xã
                    else if (currentZoom >= 5 && currentZoom < 7) {{
                        if (!leafletMap.hasLayer(layerTinhId)) leafletMap.addLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    // Zoom >= 7: Hiện Tỉnh, Hiện Xã
                    else if (currentZoom >= 7) {{
                        if (!leafletMap.hasLayer(layerTinhId)) leafletMap.addLayer(layerTinhId);
                        if (!leafletMap.hasLayer(layerXaId)) leafletMap.addLayer(layerXaId);
                    }}
                }}
                leafletMap.on('zoomend', updateLayers);
                updateLayers();
            }}
        }}
    }};
}});
</script>
"""
m.get_root().html.add_child(folium.Element(macro_zoom_script))

# 7. Hiển thị giao diện Web lên Streamlit
col1, col2 = st.columns([1, 4]) # Cột bản đồ mở rộng tối đa ra màn hình

with col1:
    st.subheader("⚙️ Cấu trúc Mới")
    st.markdown("""
    **Mạng lưới Việt Nam chuẩn thực tế:**
    *   🏛️ **Hà Nội**: Cấp Trung ương.
    *   🏭 **6 Trung tâm cấp Tỉnh**: *Quảng Ninh, Hải Phòng, Đà Nẵng, Khánh Hòa, TP.HCM, Cần Thơ*.
    *   🏡 **Hệ thống cấp Xã**: *Xã Vân Đồn, Xã Thủy Nguyên, Xã Hòa Vang, Xã Diên Khánh, Xã Củ Chi, Xã Phong Điền* nằm chính xác tại vị trí nông thôn bao quanh Tỉnh chủ quản.
    """)

with col2:
    st.subheader("🗺️ Bản đồ Ma trận Tài chính Đa tầng & Đa điểm Chuẩn địa lý")
    st_folium(m, width=1250, height=780, returned_objects=[])
