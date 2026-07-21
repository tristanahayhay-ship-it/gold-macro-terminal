import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Mạng lưới Tài chính Toàn cầu Hợp nhất",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Hệ thống Ma trận Tài chính Đa tầng Phủ kín Toàn cầu")
st.markdown("Hệ thống tự động đồng bộ cấu trúc mạng lưới phân rã thực tế vĩ mô - vi mô cho **TẤT CẢ** các quốc gia lớn trên thế giới.")

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

# Thiết lập các phân lớp quản lý ghim
fg_quoc_gia = folium.FeatureGroup(name="🏛️ Tầng Trung ương (Vĩ mô)").add_to(m)
fg_cap_tinh = folium.FeatureGroup(name="🏭 Tầng Cấp Tỉnh (Trung mô)").add_to(m)
fg_cap_xa = folium.FeatureGroup(name="🏡 Tầng Cấp Xã (Vi mô)").add_to(m)
# Hệ thống dữ liệu gắn cứng tọa độ thực tế của MỌI quốc gia lớn để tránh lỗi lệch ghim
global_macro_database = {
    "Việt Nam (VN)": {
        "QG": [21.0285, 105.8542], # Hà Nội
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
        "QG": [38.8951, -77.0364], # Washington DC
        "PROVS": {
            "New York (Bờ Đông)": [40.7128, -74.0060],
            "Chicago (Trung Tây)": [41.8781, -87.6298],
            "Los Angeles (Bờ Tây)": [34.0522, -118.2437],
            "Houston (Miền Nam)": [29.7604, -95.3698],
            "Seattle (Tây Bắc)": [47.6062, -122.3321]
        }
    },
    "Trung Quốc (CN)": {
        "QG": [39.9042, 116.4074], # Bắc Kinh
        "PROVS": {
            "Thượng Hải (Bờ Biển)": [31.2304, 121.4737],
            "Quảng Châu (Miền Nam)": [23.1291, 113.2644],
            "Thâm Quyến (Công nghệ)": [22.5431, 114.0579],
            "Thành Đô (Phía Tây)": [30.6594, 104.0657],
            "Vũ Hán (Trung tâm)": [30.5928, 114.3055]
        }
    },
    "Nhật Bản (JP)": {
        "QG": [35.6762, 139.6503], # Tokyo
        "PROVS": {
            "Osaka (Vùng Kansai)": [34.6937, 135.5023],
            "Nagoya (Trung tâm)": [35.1814, 136.9063],
            "Hokkaido (Miền Bắc)": [43.0621, 141.3544],
            "Fukuoka (Miền Nam)": [33.5902, 130.4017]
        }
    },
    "Đức (Germany)": {
        "QG": [52.5200, 13.4050], # Berlin
        "PROVS": {
            "Frankfurt (Tài chính)": [50.1109, 8.6821],
            "Munich (Miền Nam)": [48.1351, 11.5820],
            "Hamburg (Cảng Bắc)": [53.5511, 9.9937],
            "Stuttgart (Công nghiệp)": [48.7758, 9.1829]
        }
    },
    "Anh (UK)": {
        "QG": [51.5074, -0.1278], # London
        "PROVS": {
            "Manchester": [53.4808, -2.2426],
            "Birmingham": [52.4862, -1.8904],
            "Edinburgh": [55.9533, -3.1883]
        }
    },
    "Pháp (France)": {
        "QG": [48.8566, 2.3522], # Paris
        "PROVS": {
            "Lyon": [45.7640, 4.8357],
            "Marseille": [43.2965, 5.3698],
            "Toulouse": [43.6047, 1.4442]
        }
    },
    "Ấn Độ (India)": {
        "QG": [28.6139, 77.2090], # New Delhi
        "PROVS": {
            "Mumbai": [19.0760, 72.8777],
            "Bangalore": [12.9716, 77.5946],
            "Kolkata": [22.5726, 88.3639]
        }
    },
    "Úc (Australia)": {
        "QG": [-35.2809, 149.1300], # Canberra
        "PROVS": {
            "Sydney": [-33.8688, 151.2093],
            "Melbourne": [-37.8136, 144.9631],
            "Brisbane": [-27.4698, 153.0251]
        }
    },
    "Brazil": {
        "QG": [-15.7938, -47.8828], # Brasilia
        "PROVS": {
            "Sao Paulo": [-23.5505, -46.6333],
            "Rio de Janeiro": [-22.9068, -43.1729],
            "Salvador": [-12.9777, -38.5016]
        }
    }
}
hubs_processed = {}
# Quét qua cơ sở dữ liệu để cắm mốc và giăng các mạch tiền
for country_name, dataset in global_macro_database.items():
    qg_coords = dataset["QG"]
    
    # 🏛️ 1. Cấp Quốc gia
    folium.Marker(
        location=qg_coords, tooltip=f"🏛️ Trung ương vĩ mô - {country_name}",
        icon=folium.Icon(color="blue", icon="university", prefix="fa")
    ).add_to(fg_quoc_gia)
    
    hubs_processed[country_name] = {"QG": qg_coords, "TINH_COORDS": list(dataset["PROVS"].values())}
    
    # 🏭 2. Cấp Tỉnh thực tế
    for prov_name, prov_coords in dataset["PROVS"].items():
        folium.Marker(
            location=prov_coords, tooltip=f"🏭 Bộ máy Cấp Tỉnh: {prov_name}",
            icon=folium.Icon(color="orange", icon="building", prefix="fa")
        ).add_to(fg_cap_tinh)
        
        folium.PolyLine([qg_coords, prov_coords], color=color_flow, weight=2.2, opacity=0.65).add_to(fg_cap_tinh)
        
        # 🏡 3. Cấp Xã cụm vi mô vệ tinh (Xoay tròn hình bán quạt ôm sát sườn đô thị chủ quản)
        for x in range(2):
            angle = math.radians((x * 180) + random.randint(-20, 20))
            dist = 0.12  # Giới hạn bán kính siêu hẹp giữ ghim luôn nằm trên đất liền nội địa
            
            lat_xa = prov_coords[0] + dist * math.sin(angle)
            lon_xa = prov_coords[1] + dist * math.cos(angle)
            xa_coords = [lat_xa, lon_xa]
            
            folium.Marker(
                location=xa_coords, tooltip=f"🏡 Bộ máy Cấp Xã {x+1} trực thuộc vùng {prov_name}",
                icon=folium.Icon(color="green", icon="home", prefix="fa")
            ).add_to(fg_cap_xa)
            
            folium.PolyLine([prov_coords, xa_coords], color=color_flow, weight=1.2, opacity=0.55).add_to(fg_cap_xa)
            
            if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng vĩ mô)":
                folium.PolyLine([qg_coords, xa_coords], color=color_defense, weight=1.2, opacity=0.5, dash_array="5,5").add_to(fg_cap_xa)

# MA TRẬN GIAO THƯƠNG QUỐC TẾ XUYÊN LỤC ĐỊA
country_names = list(hubs_processed.keys())
for src_name in country_names:
    if src_name != "Mỹ (USA)":
        src_qg = hubs_processed[src_name]["QG"]
        us_qg = hubs_processed["Mỹ (USA)"]["QG"]
        
        if scenario == "Bình thường (Luân chuyển mở)":
            random_us_tinh = random.choice(hubs_processed["Mỹ (USA)"]["TINH_COORDS"])
            folium.PolyLine([src_qg, random_us_tinh], color="#1f77b4", weight=1.0, opacity=0.25).add_to(fg_quoc_gia)
        else:
            folium.PolyLine([src_qg, us_qg], color="#d62728", weight=1.5, opacity=0.35).add_to(fg_quoc_gia)
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
