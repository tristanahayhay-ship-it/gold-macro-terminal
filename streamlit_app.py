import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import random
import math

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Ma trận Tài chính 195 Quốc gia",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Ma trận Mạch máu Tài chính Phủ kín 195 Quốc gia")
st.markdown("Mô hình sử dụng dữ liệu bản đồ số quốc tế để tự động dựng bộ máy kinh tế 3 tầng cho **TẤT CẢ** các quốc gia và vùng lãnh thổ trên thế giới.")

scenario = st.sidebar.selectbox(
    "Chọn trạng thái kinh tế thế giới:",
    options=["Bình thường (Luân chuyển mở)", "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)"]
)

# 2. Tải cơ sở dữ liệu ranh giới địa lý của 195 quốc gia từ kho lưu trữ quốc tế công cộng
@st.cache_data # Lưu vào bộ nhớ đệm để bản đồ tải siêu nhanh, không bị lag sập server
def load_world_geojson():
    url = "https://githubusercontent.com"
    response = requests.get(url)
    return response.json()

try:
    world_geo = load_world_geojson()
except Exception as e:
    st.error("Không thể kết nối đến máy chủ dữ liệu quốc tế. Vui lòng kiểm tra internet.")
    st.stop()

# Khởi tạo bản đồ thế giới phẳng, khóa không cho lặp màn hình ngang
m = folium.Map(
    location=[20.0, 0.0], 
    zoom_start=2, 
    tiles="CartoDB positron",
    no_wrap=True,
    max_bounds=True
)

random.seed(42)
color_flow = "#1f77b4" if scenario == "Bình thường (Luân chuyển mở)" else "#d62728"
color_defense = "#2ca02c"

# Thiết lập các phân lớp quản lý ghim tự động
fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)").add_to(m)

# 3. THUẬT TOÁN QUÉT VÀ TỰ ĐỘNG DỰNG BỘ MÁY CHO TẤT CẢ CÁC NƯỚC TRÊN TRÁI ĐẤT
# Duyệt qua từng quốc gia trong file dữ liệu quốc tế
for feature in world_geo['features']:
    country_name = feature['properties']['name']
    
    # Tìm tọa độ trọng tâm đất liền của quốc gia đó để cắm mốc ghim
    # Thuật toán tự động bóc tách hình học đa giác (Polygons) của biên giới nước đó
    geom = feature['geometry']
    if geom['type'] == 'Polygon':
        coords_list = geom['coordinates'][0]
    elif geom['type'] == 'MultiPolygon':
        coords_list = geom['coordinates'][0][0]
    else:
        continue
        
    # Tính toán tọa độ trung tâm đất liền (Average Mean) để ghim không bị lệch ra ngoài biển
    lats = [c[1] for c in coords_list if isinstance(c, list) and len(c)>=2]
    lons = [c[0] for c in coords_list if isinstance(c, list) and len(c)>=2]
    
    if not lats or not lons:
        continue
        
    lat_qg = sum(lats) / len(lats)
    lon_qg = sum(lons) / len(lons)
    qg_ctr = [lat_qg, lon_qg]
    
    # Loại trừ các điểm lỗi tính toán vĩ độ vượt quá ranh giới cực địa
    if not (-75 < lat_qg < 75) or not (-170 < lon_qg < 170):
        continue

    # --- A. TỰ ĐỘNG CẮM MARKER TRUNG ƯƠNG QUỐC GIA ---
    folium.Marker(
        location=qg_ctr, 
        tooltip=f"🏛️ Trung ương vĩ mô - {country_name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(fg_quoc_gia)
    
    # Tạo các cơ quan vi mô nội bộ (Ngân hàng TW & Bộ tài chính) bám sát sườn thủ đô nước đó
    nhtw = [lat_qg - 0.1, lon_qg - 0.1]
    btc = [lat_qg + 0.1, lon_qg + 0.1]
    folium.CircleMarker(location=nhtw, radius=3, color="blue", fill=True, popup=f"Ngân hàng Trung ương - {country_name}").add_to(fg_quoc_gia)
    folium.CircleMarker(location=btc, radius=3, color="blue", fill=True, popup=f"Bộ Tài chính - {country_name}").add_to(fg_quoc_gia)
    folium.PolyLine([nhtw, btc], color="#7f7f7f", weight=1, dash_array="3,3").add_to(fg_quoc_gia)

    # --- B. TỰ ĐỘNG DỰNG BỘ MÁY CẤP TỈNH TRÊN ĐẤT LIỀN ---
    # Tỉnh được dịch chuyển một khoảng cách cực nhỏ theo hướng địa hình của ranh giới nước đó
    lat_tinh = lat_qg - 0.8 if lat_qg > 0 else lat_qg + 0.8
    lon_tinh = lon_qg + 0.8
    tinh_ctr = [lat_tinh, lon_tinh]
    
    folium.Marker(
        location=tinh_center, tooltip=f"🏭 Bộ máy Cấp Tỉnh - {country_name}",
        icon=folium.Icon(color="orange", icon="building", prefix="fa")
    ).add_to(fg_cap_tinh)
    
    # Đường mạch tiền vĩ mô: Trung ương ➔ Tỉnh
    folium.PolyLine([qg_ctr, tinh_ctr], color=color_flow, weight=2, opacity=0.6).add_to(fg_cap_tinh)
    
    # Cơ quan thành phần của Tỉnh
    tax = [lat_tinh - 0.08, lon_tinh - 0.08]
    kcn = [lat_tinh + 0.08, lon_tinh + 0.08]
    folium.CircleMarker(location=tax, radius=3, color="orange", fill=True, popup=f"Cục Thuế địa phương - {country_name}").add_to(fg_cap_tinh)
    folium.CircleMarker(location=kcn, radius=3, color="orange", fill=True, popup=f"Khu công nghiệp / DN lớn - {country_name}").add_to(fg_cap_tinh)

    # --- C. TỰ ĐỘNG DỰNG BỘ MÁY CẤP XÃ TRÊN ĐẤT LIỀN ---
    lat_xa = lat_tinh - 0.6 if lat_tinh > 0 else lat_tinh + 0.6
    lon_xa = lon_tinh + 0.6
    xa_ctr = [lat_xa, lon_xa]
    
    folium.Marker(
        location=xa_ctr, tooltip=f"🏡 Bộ máy Cấp Xã - {country_name}",
        icon=folium.Icon(color="green", icon="home", prefix="fa")
    ).add_to(fg_cap_xa)
    
    # Đường mạch tiền vi mô: Tỉnh ➔ Xã
    folium.PolyLine([tinh_ctr, xa_ctr], color=color_flow, weight=1.5, opacity=0.5).add_to(fg_cap_xa)
    
    # Cơ quan thành phần của Xã
    ubnd = [lat_xa - 0.06, lon_xa - 0.06]
    hodan = [lat_xa + 0.06, lon_xa + 0.06]
    folium.CircleMarker(location=ubnd, radius=3, color="green", fill=True, popup=f"Ủy ban Nhân dân xã - {country_name}").add_to(fg_cap_xa)
    folium.CircleMarker(location=hodan, radius=3, color="green", fill=True, popup=f"Hộ dân / Nông dân sản xuất - {country_name}").add_to(fg_cap_xa)

    # Nếu có BIẾN, đường cứu trợ khẩn cấp từ Trung ương bắn thẳng xuống Xã
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        folium.PolyLine([qg_ctr, xa_ctr], color=color_defense, weight=1.2, opacity=0.5, dash_array="6,6").add_to(fg_cap_xa)

# 4. NHÚNG MÃ JAVASCRIPT ĐIỀU KHIỂN KÍNH HIỂN VI CHUYỂN LỚP (Mượt 100%, không nhấp nháy)
macro_zoom_script = f"""
<script>
document.addEventListener("DOMContentLoaded", function() {{
    var checkMap = setInterval(window.checkAndApplyZoom, 300);
    window.checkAndApplyZoom = function() {{
        var maps = document.getElementsByClassName("folium-map");
        if (maps.length > 0) {{
            var mapId = maps.id;
            var leafletMap = window[maps.id];
            if (leafletMap) {{
                clearInterval(checkMap);
                var layerTinhId = window["{fg_cap_tinh.get_name()}"];
                var layerXaId = window["{fg_cap_xa.get_name()}"];
                
                function updateLayers() {{
                    var currentZoom = leafletMap.getZoom();
                    if (currentZoom < 4) {{
                        if (leafletMap.hasLayer(layerTinhId)) leafletMap.removeLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    else if (currentZoom >= 4 && currentZoom < 6) {{
                        if (!leafletMap.hasLayer(layerTinhId)) leafletMap.addLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    else if (currentZoom >= 6) {{
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

# 5. ĐẨY HÌNH ẢNH GIAO DIỆN LÊN DASHBOARD STREAMLIT
col1, col2 = st.columns()

with col1:
    st.subheader("⚙️ Kính Hiển Vi 195 Nước")
    st.markdown("""
    **Cơ chế ma trận toàn hành tinh:**
    *   🌍 **Nhìn bao quát**: 195 quốc gia đều có ghim đầu não 🏛️ **Trung ương**.
    *   🏭 **Phóng to vào nước bất kỳ**: Bộ máy 🏭 **Cấp Tỉnh** cùng các cơ quan nội bộ (Cục thuế, KCN) tự động bung ra trên đất liền nước đó.
    *   🏡 **Phóng to sát sườn**: Bộ máy 🏡 **Cấp Xã** (UBND, Hộ dân) xuất hiện chi tiết.
    """)

with col2:
    st_folium(m, width=1250, height=780, returned_objects=[])
