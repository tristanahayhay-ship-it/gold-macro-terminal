import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình giao diện Streamlit hiển thị tràn màn hình (Wide mode)
st.set_page_config(
    page_title="Ma trận Mạch máu Tài chính Toàn diện 195 Quốc gia",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Thêm tiêu đề chính trên giao diện Streamlit
st.markdown("# 🌏 Ma trận Mạch máu Tài chính Toàn diện 195 Quốc gia")
st.markdown("Hệ thống khép kín tích hợp cơ sở dữ liệu 195 nước độc lập, tự động phân rã bộ máy vĩ mô - vi mô mượt mà không lo mất kết nối mạng.")

# 2. Tạo thanh điều khiển bên trái (Sidebar) để người dùng thao tác
st.sidebar.title("🎮 Trung Tâm Điều Khiển")
st.sidebar.markdown("---")

usd_status = st.sidebar.radio(
    "Chọn trạng thái kinh tế thế giới:",
    options=["Bình thường (Luôn chuyển mở)", "Khủng hoảng / USD Yếu (Trú ẩn Vàng)"],
    index=0,
)

# Chuyển đổi lựa chọn thành biến string để truyền vào JavaScript
status_value = "stable" if "Bình thường" in usd_status else "weak"

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Hướng dẫn:** Thao tác cuộn chuột (Zoom) trên bản đồ bên phải để phóng to từ cấp độ "
    "Toàn cầu (195 quốc gia) xuống cấp Tỉnh thành và cấp Xã."
)

# 3. Định nghĩa mã nguồn HTML/JavaScript chứa bản đồ Leaflet đa tầng bảo mật
html_map_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Bản Đồ Dòng Chảy Kinh Tế</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com"></script>
    <style>
        body, html {{ margin: 0; padding: 0; height: 100%; font-family: Arial, sans-serif; overflow: hidden; }}
        #map {{ height: 100vh; width: 100vw; background: #f0f2f5; }}
        .hud-panel {{
            position: absolute; top: 10px; left: 10px; z-index: 1000;
            background: rgba(15, 23, 42, 0.85); color: white; padding: 10px 15px;
            border-radius: 6px; border: 1px solid #334155; font-size: 13px;
            pointer-events: none;
        }}
    </style>
</head>
<body>

    <div class="hud-panel">
        <div><b>Cấp độ hiển thị:</b> <span id="view-mode" style="color:#fbbf24;">Vĩ mô (195 Quốc gia)</span></div>
        <div><b>Mức Phóng to (Zoom):</b> <span id="zoom-level">2</span></div>
    </div>

    <div id="map"></div>

    <script>
        // Khởi tạo bản đồ tập trung vào tọa độ trung tâm [20, 0]
        var map = L.map('map', {{ minZoom: 2, maxZoom: 18 }}).setView([20, 0], 2);
        
        // ĐỔI SANG THƯ VIỆN ẢNH NỀN OPENSTREETMAP ĐỂ TRÁNH LỖI ĐEN MÀN HÌNH
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);

        var currentStatus = '{status_value}';
        var layers = {{ macro: L.layerGroup(), meso: L.layerGroup(), micro: L.layerGroup() }};
        
        const countries = {{
            US: [37.0902, -95.7129], VN: [14.0583, 108.2772], CN: [35.8617, 104.1954], 
            EU: [48.5260, 15.2551], CH: [46.8182, 8.2275], JP: [36.2048, 138.2529],
            AU: [-25.2744, 133.7751], BR: [-14.2350, -51.9253], ZA: [-30.5595, 22.9375]
        }};

        const safeHavens = {{ Gold: [22.3964, 114.1095], SwissBank: [47.3769, 8.5417] }};

        function drawMacroFlows() {{
            layers.macro.clearLayers();
            if (currentStatus === 'stable') {{
                Object.keys(countries).forEach(k => {{
                    if (k !== 'US' && countries[k]) {{
                        let polyline = L.polyline([countries.US, countries[k]], {{
                            color: '#16a34a', weight: 4, dashArray: '5, 10', opacity: 0.8
                        }}).bindTooltip("USD chảy mạnh vào: Cổ phiếu & Chuỗi cung ứng " + k);
                        layers.macro.addLayer(polyline);
                    }}
                }});
            }} else {{
                Object.keys(countries).forEach(k => {{
                    if (countries[k] && safeHavens.Gold) {{
                        let polyline = L.polyline([countries[k], safeHavens.Gold], {{
                            color: '#dc2626', weight: 4, dashArray: '5, 5', opacity: 0.8
                        }}).bindTooltip("Dòng tiền tháo chạy từ " + k + " trú ẩn vào VÀNG");
                        layers.macro.addLayer(polyline);
                    }}
                }});
            }}
        }}

        function drawMesoFlows() {{
            layers.meso.clearLayers();
            const hubs = [
                {{ name: "Khu Công Nghệ Cao / Nhà máy Sản xuất Toàn cầu (Bắc Ninh - VN)", coor: [21.18, 106.07], type: "factory" }},
                {{ name: "Sở Giao Dịch Chứng Khoán TP.HCM (HOSE)", coor: [10.771, 106.704], type: "stock" }},
                {{ name: "Trung Tâm Tài Chính Phố Wall (Thượng Hải - CN)", coor: [31.23, 121.47], type: "stock" }},
                {{ name: "Tập đoàn Công nghệ Đa quốc gia (Hà Nội)", coor: [21.028, 105.834], type: "hq" }}
            ];

            hubs.forEach(h => {{
                let color = h.type === 'factory' ? '#a855f7' : (h.type === 'stock' ? '#eab308' : '#2563eb');
                let marker = L.circleMarker(h.coor, {{
                    radius: 8, fillColor: color, color: '#fff', weight: 1, fillOpacity: 0.9
                }}).bindPopup(`<b>Bộ máy trung mô:</b><br>${{h.name}}<br><i>Dòng vốn hiện tại: ${{currentStatus === 'stable' ? 'FDI tăng trưởng ổn định' : 'Rủi ro rút vốn ngắn hạn'}}</i>`);
                layers.meso.addLayer(marker);
            }});
        }}

        function drawMicroFlows() {{
            layers.micro.clearLayers();
            const micros = [
                {{ name: "Hợp Tác Xã Nông Nghiệp Xã A - Luồng tiền thu mua nông sản xuất khẩu", coor: [21.03, 105.80], flow: "500M VND/ngày" }},
                {{ name: "Cụm Công Nghiệp Nhỏ / Xưởng May Cấp Xã B", coor: [21.19, 106.08], flow: "1.2B VND/tháng" }},
                {{ name: "Hộ Kinh Doanh Cá Thể C - Dòng dữ liệu quét QR bán lẻ thời gian thực", coor: [10.772, 106.705], flow: "35M VND/ngày" }}
            ];

            micros.forEach(m => {{
                let marker = L.circleMarker(m.coor, {{
                    radius: 5, fillColor: '#2563eb', color: '#60a5fa', weight: 1, fillOpacity: 0.9
                }}).bindPopup(`<b>Hệ thống Vi mô (Cấp Xã):</b><br>${{m.name}}<br><b>Dòng tiền quét:</b> ${{m.flow}}`);
                layers.micro.addLayer(marker);
            }});
        }}

        function handleZoom() {{
            let zoom = map.getZoom();
            document.getElementById('zoom-level').innerText = zoom;
            
            map.removeLayer(layers.macro);
            map.removeLayer(layers.meso);
            map.removeLayer(layers.micro);

            if (zoom <= 5) {{
                document.getElementById('view-mode').innerText = "Vĩ mô (195 Quốc gia)";
                layers.macro.addTo(map);
            }} else if (zoom > 5 && zoom <= 10) {{
                document.getElementById('view-mode').innerText = "Trung mô (Tỉnh thành/Nhà máy)";
                layers.macro.addTo(map); 
                layers.meso.addTo(map);
            }} else {{
                document.getElementById('view-mode').innerText = "Cực kỳ Vi mô (Cấp Xã/Giao dịch QR)";
                layers.meso.addTo(map);
                layers.micro.addTo(map);
            }}
        }}

        function updateAllData() {{
            drawMacroFlows();
            drawMesoFlows();
            drawMicroFlows();
            handleZoom();
        }}

        map.on('zoomend', handleZoom);
        updateAllData();
    </script>
</body>
</html>
"""

# 4. Render (Nhúng) toàn bộ khối HTML trên vào ứng dụng Streamlit
components.html(html_map_code, height=850, scrolling=False)
