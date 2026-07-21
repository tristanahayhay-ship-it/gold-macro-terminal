import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Thực tế",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Ma trận Mạch máu Tài chính 3 Tầng Thực tế Toàn cầu")
st.markdown("Hệ thống tự động đồng bộ **toàn bộ các Tỉnh/Thành phố của Việt Nam** và mạng lưới đa điểm vi mô trên phạm vi toàn thế giới.")

# Thanh cấu hình kịch bản hệ thống thế giới từ thanh Sidebar bên trái
scenario = st.sidebar.selectbox(
    "Chọn trạng thái kinh tế toàn cầu:",
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

# ĐỊNH NGHĨA CÁC LỚP BẢN ĐỒ PHÂN TẦNG (Feature Groups)
fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)").add_to(m)

# CƠ SỞ DỮ LIỆU ĐỊA LÝ THỰC TẾ PHỦ KÍN CÁC TỈNH THÀNH VIỆT NAM (Trục tọa độ chính xác từng vùng)
vietnam_provinces = {
    # Miền Bắc
    "Hà Nội": [21.0285, 105.8542], "Hải Phòng": [20.8449, 106.6881], "Quảng Ninh": [20.9485, 107.0734],
    "Vĩnh Phúc": [21.3614, 105.5444], "Bắc Ninh": [21.1861, 106.0763], "Bắc Giang": [21.2731, 106.1946],
    "Hải Dương": [20.9409, 106.3331], "Hưng Yên": [20.6464, 106.0511], "Thái Bình": [20.4464, 106.3364],
    "Nam Định": [20.4172, 106.1683], "Ninh Bình": [20.2526, 105.9745], "Hà Nam": [20.5403, 105.9221],
    "Lạng Sơn": [21.8547, 106.7620], "Cao Bằng": [22.6686, 106.2579], "Hà Giang": [22.8233, 104.9836],
    "Tuyên Quang": [21.8181, 105.2111], "Phú Thọ": [21.3243, 105.2181], "Thái Nguyên": [21.5939, 105.8482],
    "Yên Bái": [21.7049, 104.8741], "Lào Cai": [22.4856, 103.9707], "Điện Biên": [21.3855, 103.0212],
    "Lai Châu": [22.3958, 103.4561], "Sơn La": [21.3262, 103.9131], "Hòa Bình": [20.8172, 105.3378],
    # Miền Trung & Tây Nguyên
    "Thanh Hóa": [19.8075, 105.7764], "Nghệ An": [18.6734, 105.6923], "Hà Tĩnh": [18.3392, 105.9019],
    "Quảng Bình": [17.4715, 106.6181], "Quảng Trị": [16.7415, 107.1012], "Thừa Thiên Huế": [16.4637, 107.5909],
    "Đà Nẵng": [16.0544, 108.2022], "Quảng Nam": [15.5673, 108.4812], "Quảng Ngãi": [15.1221, 108.7997],
    "Bình Định": [13.7761, 109.2243], "Phú Yên": [13.0952, 109.3032], "Khánh Hòa": [12.2471, 109.1961],
    "Ninh Thuận": [11.5644, 108.9881], "Bình Thuận": [10.9322, 108.1009], "Kon Tum": [14.3497, 107.9947],
    "Gia Lai": [13.9831, 108.0022], "Đắk Lắk": [12.6711, 108.0381], "Đắk Nông": [12.0012, 107.6841],
    "Lâm Đồng": [11.9404, 108.4583],
    # Miền Nam
    "Bình Phước": [11.5332, 106.8841], "Tây Ninh": [11.3142, 106.1011], "Bình Dương": [11.0234, 106.6712],
    "Đồng Nai": [10.9525, 106.8214], "Bà Rịa - Vũng Tàu": [10.4114, 107.1362], "TP. Hồ Chí Minh": [10.8231, 106.6297],
    "Long An": [10.5333, 106.4000], "Tiền Giang": [10.3601, 106.3631], "Bến Tre": [10.2331, 106.3752],
    "Trà Vinh": [9.9322, 106.3331], "Vĩnh Long": [10.2526, 105.9611], "Đồng Tháp": [10.4533, 105.6331],
    "An Giang": [10.5364, 105.1331], "Kiên Giang": [9.9825, 105.0811], "Cần Thơ": [10.0452, 105.7469],
    "Hậu Giang": [9.7831, 105.4611], "Sóc Trăng": [9.6002, 105.9721], "Bạc Liêu": [9.2941, 105.7221],
    "Cà Mau": [9.1764, 105.1511]
}

# CƠ SỞ DỮ LIỆU ĐA TẦNG CỦA CÁC QUỐC GIA KHÁC TRÊN THẾ GIỚI
world_hubs = {
    "Mỹ (USA)": {"QG": [38.8951, -77.0364], "PROVS": {"New York": [40.7128, -74.0060], "Chicago": [41.8781, -87.6298], "Los Angeles": [34.0522, -118.2437], "Houston": [29.7604, -95.3698]}},
    "Trung Quốc (CN)": {"QG": [39.9042, 116.4074], "PROVS": {"Thượng Hải": [31.2304, 121.4737], "Quảng Châu": [23.1291, 113.2644], "Thâm Quyến": [22.5431, 114.0579], "Thành Đô": [30.6594, 104.0657]}},
    "Nhật Bản (JP)": {"QG": [35.6762, 139.6503], "PROVS": {"Osaka": [34.6937, 135.5023], "Nagoya": [35.1814, 136.9063], "Hokkaido": [43.0621, 141.3544], "Fukuoka": [33.5902, 130.4017]}},
    "Đức (Germany)": {"QG": [52.5200, 13.4050], "PROVS": {"Frankfurt": [50.1109, 8.6821], "Munich": [48.1351, 11.5820], "Hamburg": [53.5511, 9.9937], "Stuttgart": [48.7758, 9.1829]}}
}
hubs_processed = {}
# A. Đóng ghim Trung ương Hà Nội
folium.Marker(
    location=vietnam_provinces["Hà Nội"], 
    tooltip="🏛️ Trung ương vĩ mô: Chính phủ & Ngân hàng Nhà nước (Thủ đô Hà Nội)",
    icon=folium.Icon(color="blue", icon="university", prefix="fa")
).add_to(fg_quoc_gia)

# B. Tạo bộ máy và các xã cơ sở cho các tỉnh thành Việt Nam
for name_tinh, coords_tinh in vietnam_provinces.items():
    if name_tinh != "Hà Nội":
        folium.Marker(
            location=coords_tinh, tooltip=f"🏭 Bộ máy Cấp Tỉnh: Tỉnh {name_tinh}",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(fg_cap_tinh)
        
        folium.PolyLine([vietnam_provinces["Hà Nội"], coords_tinh], color=color_flow, weight=2, opacity=0.6).add_to(fg_cap_tinh)
        
        # C. Thuật toán tự động sinh 2 Xã/Huyện vệ tinh bám sát sườn đất liền nội tại của tỉnh đó
        for x in range(2):
            lat_xa = coords_tinh[0] + (0.15 if x == 0 else -0.15)
            lon_xa = coords_tinh[1] + (0.15 if x == 0 else -0.15)
            
            folium.Marker(
                location=[lat_xa, lon_xa], tooltip=f"🏡 Bộ máy Cấp Xã {x+1} trực thuộc Tỉnh {name_tinh}",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(fg_cap_xa)
            
            folium.PolyLine([coords_tinh, [lat_xa, lon_xa]], color=color_flow, weight=1.2, opacity=0.5).add_to(fg_cap_xa)
            
            if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
                folium.PolyLine([vietnam_provinces["Hà Nội"], [lat_xa, lon_xa]], color=color_defense, weight=1.2, opacity=0.55, dash_array="4,4").add_to(fg_cap_xa)

# D. Triển khai đa điểm cho các quốc gia khác trên thế giới
for country_name, layers in world_hubs.items():
    qg_coords = layers["QG"]
    folium.Marker(location=qg_coords, tooltip=f"🏛️ Trung ương vĩ mô - {country_name}", icon=folium.Icon(color="blue", icon="university", prefix="fa")).add_to(fg_quoc_gia)
    
    for p_name, p_coords in layers["PROVS"].items():
        folium.Marker(location=p_coords, tooltip=f"🏭 Bộ máy Cấp Tỉnh: {p_name} ({country_name})", icon=folium.Icon(color="orange", icon="building", prefix="fa")).add_to(fg_cap_tinh)
        folium.PolyLine([qg_coords, p_coords], color=color_flow, weight=2.2, opacity=0.6).add_to(fg_cap_tinh)
        
        for x in range(2):
            lat_xa = p_coords[0] + (0.2 if x == 0 else -0.2)
            lon_xa = p_coords[1] + (0.2 if x == 0 else -0.2)
            folium.Marker(location=[lat_xa, lon_xa], tooltip=f"🏡 Bộ máy Cấp Xã {x+1} thuộc {p_name}", icon=folium.Icon(color="green", icon="home", prefix="fa")).add_to(fg_cap_xa)
            folium.PolyLine([p_coords, [lat_xa, lon_xa]], color=color_flow, weight=1.2, opacity=0.5).add_to(fg_cap_xa)

# Kết nối giao thương / hoặc tháo chạy dòng vốn vĩ mô xuyên biên giới về Mỹ
for country_name in world_hubs.keys():
    if country_name != "Mỹ (USA)":
        folium.PolyLine([world_hubs[country_name]["QG"], world_hubs["Mỹ (USA)"]["QG"]], color=color_flow, weight=1.5, opacity=0.35).add_to(fg_quoc_gia)
# NHÚNG MÃ JAVASCRIPT ĐIỀU KHIỂN ĐỘ ẨN/HIỆN KÍNH HIỂN VI TRÊN TRÌNH DUYỆT (Mượt 100%, không nhấp nháy)
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
                var layerTinhId = window[{fg_cap_tinh.get_name()}];
                var layerXaId = window[{fg_cap_xa.get_name()}];
                
                function updateLayers() {{
                    var currentZoom = leafletMap.getZoom();
                    // Zoom < 5: Ẩn Tỉnh, Ẩn Xã khi nhìn toàn cầu
                    if (currentZoom < 5) {{
                        if (leafletMap.hasLayer(layerTinhId)) leafletMap.removeLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    // Zoom 5-6: Hiện Tỉnh, Ẩn Xã khi nhìn thấy ranh giới quốc gia
                    else if (currentZoom >= 5 && currentZoom < 7) {{
                        if (!leafletMap.hasLayer(layerTinhId)) leafletMap.addLayer(layerTinhId);
                        if (leafletMap.hasLayer(layerXaId)) leafletMap.removeLayer(layerXaId);
                    }} 
                    // Zoom >= 7: Hiện Tỉnh, Hiện Xã bung chi tiết vi mô
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
# Chia tỷ lệ giao diện: cột trái ghi chú, cột phải chứa bản đồ siêu rộng
col1, col2 = st.columns([1, 4])

with col1:
    st.subheader("⚙️ Ma trận Đa điểm")
    st.markdown("""
    **Mô hình phân rã thực tế vĩ mô đến vi mô:**
    *   🌍 **Zoom từ xa**: Giao diện sạch sẽ, chỉ hiển thị cơ quan vĩ mô Trung ương của các nước.
    *   🇻🇳 **Phóng to vừa (Zoom 5 - 6)**: Bung toàn bộ mạch máu tài chính kết nối **tất cả các tỉnh thành** từ Bắc vào Nam.
    *   🏡 **Phóng to sâu (Zoom >= 7)**: Hệ thống tự động bung toàn bộ các **Xã/Huyện vi mô** bám sát đất liền nội tại của tỉnh thành đó.
    """)
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
        st.error("🔴 Đường Đỏ: Dòng tiền sản xuất của tất cả các nước bị tháo chạy.")
        st.success("🟢 Đường Xanh lá: Gói kích thích khẩn cấp đi tắt xuống cứu trợ cấp Xã.")

with col2:
    # Tiến hành xuất bản đồ ra giao diện chính, cô lập đối tượng trả về để loại bỏ lỗi giật màn hình
    st_folium(m, width=1250, height=780, returned_objects=[])
