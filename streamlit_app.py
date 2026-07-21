import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# ====================================================
# ĐOẠN 1: CẤU HÌNH TRANG GIAO DIỆN WEB
# ====================================================
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Hợp nhất",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Hệ thống Ma trận Tài chính Đa tầng Phủ kín Toàn cầu")
st.markdown("Hệ thống đã được tối ưu hóa hiệu năng, tự động đồng bộ cấu trúc mạng lưới phân rã vĩ mô - vi mô cho các quốc gia lớn trên thế giới.")

scenario = st.sidebar.selectbox(
    "Chọn trạng thái kinh tế thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# Khởi tạo bản đồ thế giới phẳng, khóa không cho lặp màn hình ngang
m = folium.Map(
    location=[20.0, 20.0], 
    zoom_start=3, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(100)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)").add_to(m)

# ====================================================
# ĐOẠN 2: CƠ SỞ DỮ LIỆU ĐỊA LÝ THỰC TẾ ĐA ĐIỂM TOÀN CẦU
# ====================================================
global_macro_database = {
    "Việt Nam (VN)": {
        "QG": [21.0285, 105.8542],
        "PROVS": {
            "Hải Phòng (Miền Bắc)": [20.8449, 106.6881],
            "Quảng Ninh (Miền Bắc)": [20.9485, 107.0734],
            "Đà Nẵng (Miền Trung)": [16.0544, 108.2022],
            "Khánh Hòa (Miền Trung)": [12.2471, 109.1961],
            "TP. Hồ Chí Minh (Miền Nam)": [10.8231, 106.6297],
            "Cần Thơ (Miền Nam)": [10.0452, 105.7469]
        }
    },
    "Mỹ (USA)": {
        "QG": [38.8951, -77.0364],
        "PROVS": {
            "New York (Bờ Đông)": [40.7128, -74.0060],
            "Chicago (Trung Tây)": [41.8781, -87.6298],
            "Los Angeles (Bờ Tây)": [34.0522, -118.2437],
            "Houston (Miền Nam)": [29.7604, -95.3698]
        }
    },
    "Trung Quốc (CN)": {
        "QG": [39.9042, 116.4074],
        "PROVS": {
            "Thượng Hải (Bờ Biển)": [31.2304, 121.4737],
            "Quảng Châu (Miền Nam)": [23.1291, 113.2644],
            "Thành Đô (Phía Tây)": [30.6594, 104.0657]
        }
    },
    "Nhật Bản (JP)": {
        "QG": [35.6762, 139.6503],
        "PROVS": {
            "Osaka (Vùng Kansai)": [34.6937, 135.5023],
            "Hokkaido (Miền Bắc)": [43.0621, 141.3544]
        }
    },
    "Đức (Germany)": {
        "QG": [52.5200, 13.4050],
        "PROVS": {
            "Frankfurt (Tài chính)": [50.1109, 8.6821],
            "Munich (Miền Nam)": [48.1351, 11.5820]
        }
    }
}
hubs_processed = {}

# ====================================================
# ĐOẠN 3: THUẬT TOÁN PHÂN RÃ CỤM ĐÔ THỊ (TỐI ƯU BỘ NHỚ)
# ====================================================
for country_name, dataset in global_macro_database.items():
    qg_coords = dataset["QG"]
    
    # 🏛️ 1. Gắn ghim Tầng Quốc gia
    folium.Marker(
        location=qg_coords, tooltip=f"🏛️ Trung ương vĩ mô - {country_name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(fg_quoc_gia)
    
    hubs_processed[country_name] = {"QG": qg_coords, "TINH_COORDS": list(dataset["PROVS"].values())}
    
    # 🏭 2. Gắn ghim mạng lưới cấp Tỉnh/Thành phố
    for prov_name, prov_coords in dataset["PROVS"].items():
        folium.Marker(
            location=prov_coords, tooltip=f"🏭 Bộ máy Cấp Tỉnh: {prov_name}",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(fg_cap_tinh)
        
        # Mạch tiền vĩ mô: Trung ương ➔ Cấp Tỉnh
        folium.PolyLine([qg_coords, prov_coords], color=color_flow, weight=2.0, opacity=0.6).add_to(fg_cap_tinh)
        
        # 🏡 3. Cụm vi mô: Tự động sinh 1 ghim Xã bám sát theo hình tròn để giảm tải cho server
        angle = math.radians(random.randint(0, 360))
        dist = 0.12  
        
        lat_xa = prov_coords[0] + dist * math.sin(angle)
        lon_xa = prov_coords[1] + dist * math.cos(angle)
        xa_coords = [lat_xa, lon_xa]
        
        folium.Marker(
            location=xa_coords, tooltip=f"🏡 Bộ máy Cấp Xã trực thuộc vùng {prov_name}",
            icon=folium.Icon(color="green", icon="home", prefix="fa")
        ).add_to(fg_cap_xa)
        
        # Mạch tiền vi mô địa phương: Tỉnh ➔ Xã
        folium.PolyLine([prov_coords, xa_coords], color=color_flow, weight=1.2, opacity=0.5).add_to(fg_cap_xa)

# ====================================================
# ĐOẠN 4: MA TRẬN GIAO THƯƠNG QUỐC TẾ XUYÊN LỤC ĐỊA
# ====================================================
country_names = list(hubs_processed.keys())
for src_name in country_names:
    if src_name != "Mỹ (USA)":
        src_qg = hubs_processed[src_name]["QG"]
        us_qg = hubs_processed["Mỹ (USA)"]["QG"]
        
        if scenario == "Bình thường (Luân chuyển mở)":
            random_us_tinh = random.choice(hubs_processed["Mỹ (USA)"]["TINH_COORDS"])
            folium.PolyLine([src_qg, random_us_tinh], color="#1f77b4", weight=1.0, opacity=0.2).add_to(fg_quoc_gia)
        else:
            folium.PolyLine([src_qg, us_qg], color="#d62728", weight=1.2, opacity=0.3).add_to(fg_quoc_gia)

# ====================================================
# ĐOẠN 5: NHÚNG MÃ JAVASCRIPT ĐIỀU KHIỂN ẨN/HIỆN ZOOM SỬ DỤNG WINDOW
# ====================================================
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
                var layerTinhId = window["{fg_cap_tinh.get_name()}"];
                var layerXaId = window["{fg_cap_xa.get_name()}"];
                
                function updateLayers() {{
                    var currentZoom = leafletMap.getZoom();
                    if (currentZoom < 5) {{
                        if (leafletMap.hasLayer(layerTinhId)) leafletMap.removeLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    else if (currentZoom >= 5 && currentZoom < 7) {{
                        if (!leafletMap.hasLayer(layerTinhId)) leafletMap.addLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
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

# ====================================================
# ĐOẠN 6: ĐẨY HÌNH ẢNH GIAO DIỆN LÊN DASHBOARD WEB
# ====================================================
col1, col2 = st.columns([1, 4]) # Tối ưu tỷ lệ cột để bản đồ mở rộng tối đa

with col1:
    st.subheader("⚙️ Kính Hiển Vi Toàn Cầu")
    st.markdown("""
    **Cấu trúc Đa điểm Toàn diện:**
    *   🏛️ **Zoom xa (Zoom < 5)**: Chỉ hiển thị cơ quan vĩ mô Trung ương của các nước trên thế giới.
    *   🏭 **Zoom vừa (Zoom 5 - 6)**: Hiện toàn bộ mạng lưới Cấp Tỉnh thực tế (Hải Phòng, Đà Nẵng, New York, Thượng Hải, Tokyo...).
    *   🏡 **Zoom sâu (Zoom >= 7)**: Bung mạng lưới Cấp Xã vệ tinh bám chặt trong đất liền.
    """)

with col2:
    st_folium(m, width=1300, height=800, returned_objects=[])
