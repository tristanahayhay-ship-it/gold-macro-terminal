import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện Streamlit màn hình rộng
st.set_page_config(layout="wide", page_title="Global Money Flow Network")

st.title("🌐 Hệ Thống Dòng Chảy Tiền Tệ & Tài Sản Toàn Cầu Xuyên Lục Địa")
st.caption("Mô phỏng mạng lưới kinh tế tuần hoàn liên kết từ cấp cơ sở (Xã/Huyện) của từng quốc gia ra toàn thế giới.")

# 2. Định nghĩa tọa độ địa lý thực tế của các thực thể từ Vi mô đến Toàn cầu
# Định dạng: [Kinh độ (Longitude), Vĩ độ (Latitude)] - Lưu ý Pydeck nhận [Lon, Lat]
global_locations = {
    # === CỤM VIỆT NAM (CHÂU Á) ===
    "VN_Xa_CoSo": [106.2400, 20.9400],         # Cấp Xã (Nông thôn VN)
    "VN_Huyen_Hub": [106.2800, 20.9800],       # Cấp Huyện (Cụm công nghiệp)
    "VN_Tinh_Center": [106.3330, 20.9409],     # Cấp Tỉnh (Trung tâm điều phối vùng)
    "VN_HaNoi_Central": [105.8542, 21.0285],   # Cấp Nhà nước (Bộ não vĩ mô Việt Nam)

    # === CỤM MỸ (BẮC MỸ) ===
    "US_Rural_Commune": [-95.7129, 37.0902],    # Cấp Xã/Vùng nông nghiệp Mỹ (Kansas)
    "US_District_Hub": [-87.6298, 41.8781],     # Cấp Huyện/Thành phố công nghiệp (Chicago)
    "US_NewYork_WallStreet": [-74.0113, 40.7075], # Cấp Nhà nước/Toàn cầu (Phố Wall, Mỹ)

    # === CỤM CHÂU ÂU (EU) ===
    "EU_Local_Production": [7.4653, 46.9480],   # Cấp Cơ sở/Xã tại Châu Âu (Thụy Sĩ)
    "EU_Frankfurt_Central": [8.6821, 50.1109],  # Cấp Nhà nước/Khu vực (Ngân hàng Trung ương Châu Âu ECB)

    # === CỤM CHÂU Á KHÁC ===
    "Singapore_Global_Hub": [103.8198, 1.3521], # Trạm trung chuyển vốn Liên lục địa (Singapore)
    "Japan_Tokyo_Central": [139.6503, 35.6762]  # Trung tâm tài chính Đông Á (Tokyo)
}

# 3. Định nghĩa mạng lưới sợi dây liên kết xuyên lục địa
# status: strong_in (Xanh lá), strong_out (Đỏ), neutral (Vàng)
global_flows = [
    # ================= MẠCH NỘI ĐỊA VIỆT NAM =================
    {"from": "VN_Xa_CoSo", "to": "VN_Huyen_Hub", "status": "neutral", "desc": "Dân gửi tiền tích lũy lên quỹ tín dụng Huyện"},
    {"from": "VN_Huyen_Hub", "to": "VN_Tinh_Center", "status": "strong_in", "desc": "Doanh nghiệp huyện nộp thuế sản xuất về Tỉnh"},
    {"from": "VN_Tinh_Center", "to": "VN_HaNoi_Central", "status": "strong_out", "desc": "Tỉnh kết chuyển thặng dư ngân sách về Kho bạc Trung ương"},

    # ================= MẠCH NỘI ĐỊA MỸ =================
    {"from": "US_Rural_Commune", "to": "US_District_Hub", "status": "strong_in", "desc": "Nông sản thô từ trang trại đổ về nhà máy chế biến Chicago"},
    {"from": "US_District_Hub", "to": "US_NewYork_WallStreet", "status": "strong_in", "desc": "Dòng vốn doanh nghiệp niêm yết lên sàn chứng khoán New York"},

    # ================= MẠCH NỘI ĐỊA CHÂU ÂU =================
    {"from": "EU_Local_Production", "to": "EU_Frankfurt_Central", "status": "neutral", "desc": "Dòng tiền tiết kiệm Euro luân chuyển về ECB"},

    # ================= MẠCH XUYÊN LỤC ĐỊA (LIÊN KẾT TOÀN THẾ GIỚI) =================
    # Dòng tiền FDI/FII từ các trung tâm lớn phóng về vùng cơ sở sản xuất toàn cầu
    {"from": "US_NewYork_WallStreet", "to": "Singapore_Global_Hub", "status": "strong_in", "desc": "Dòng vốn đầu tư Mỹ phóng sang trung tâm tài chính Châu Á"},
    {"from": "Singapore_Global_Hub", "to": "VN_Huyen_Hub", "status": "strong_in", "desc": "Vốn ngoại FDI bơm thẳng vào xây nhà máy ở cụm công nghiệp Huyện tại Việt Nam"},
    
    # Giao thương hàng hóa & Rút ròng tài sản
    {"from": "VN_HaNoi_Central", "to": "Japan_Tokyo_Central", "status": "strong_in", "desc": "Việt Nam xuất khẩu linh kiện sang Nhật Bản thu ngoại tệ mạnh"},
    {"from": "EU_Frankfurt_Central", "to": "US_NewYork_WallStreet", "status": "strong_out", "desc": "Giới đầu tư Châu Âu bán tháo tài sản Euro, chuyển dịch dòng vốn sang đô-la Mỹ an toàn"},
    {"from": "Japan_Tokyo_Central", "to": "US_NewYork_WallStreet", "status": "neutral", "desc": "Nhật Bản mua Trái phiếu Chính phủ Mỹ để giữ thế cân bằng tỷ giá"}
]

# 4. Định nghĩa mã màu RGBA theo đúng yêu cầu thiết kế của bạn
color_map = {
    "strong_in":,    # 🟢 Xanh lá: Dòng tiền vào mạnh / Mua mạnh
    "strong_out":,   # 🔴 Đỏ: Dòng tiền rút mạnh / Bán mạnh
    "neutral": [255, 255, 0, 200]     # 🟡 Vàng: Lưỡng lự / Đi ngang
}

# 5. Xây dựng bộ lọc tương tác trên Sidebar để quản lý mạng lưới khổng lồ
st.sidebar.header("🕹️ BẢNG ĐIỀU KHIỂN TOÀN CẦU")
show_level = st.sidebar.radio(
    "Góc nhìn mạng lưới:",
    ["Hiển thị toàn bộ thế giới", "Chỉ xem dòng chảy Xuyên Lục Địa", "Chỉ xem dòng chảy Nội địa các nước"]
)

# 6. Xử lý dữ liệu nạp vào Pydeck dựa trên bộ lọc của người dùng
processed_data = []
for flow in global_flows:
    is_cross_border = ("VN_" in flow["from"] and "VN_" not in flow["to"]) or \
                      ("US_" in flow["from"] and "US_" not in flow["to"]) or \
                      ("EU_" in flow["from"] and "EU_" not in flow["to"]) or \
                      ("Singapore" in flow["from"] or "Japan" in flow["from"])

    if show_level == "Chỉ xem dòng chảy Xuyên Lục Địa" and not is_cross_border:
        continue
    if show_level == "Chỉ xem dòng chảy Nội địa các nước" and is_cross_border:
        continue

    start_coords = global_locations[flow["from"]]
    end_coords = global_locations[flow["to"]]
    
    processed_data.append({
        "from_lon": start_coords[0], "from_lat": start_coords[1],
        "to_lon": end_coords[0], "to_lat": end_coords[1],
        "color": color_map[flow["status"]],
        "tooltip_text": f"Luồng: {flow['desc']}"
    })

df = pd.DataFrame(processed_data)

# 7. Khởi tạo lớp xử lý đồ họa ArcLayer của Pydeck (Tạo hiệu ứng đường vòm cong 3D)
network_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width=4,
    pickable=True,
    auto_highlight=True
)

# 8. Cấu hình góc nhìn camera (Mặc định nhìn bao quát toàn bộ Trái Đất từ không gian)
view_state = pdk.ViewState(
    latitude=30.0,
    longitude=10.0,
    zoom=1.5,      # Thu nhỏ góc nhìn để thấy toàn bộ các lục địa kết nối với nhau
    pitch=45,      # Nghiêng góc nhìn 45 độ để thấy rõ độ cong 3D của các sợi dây dòng tiền
    bearing=0
)

# 9. Render bản đồ nền tối (Darkmode) làm nổi bật các sợi dây màu phát sáng
r = pdk.Deck(
    layers=[network_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Giao diện nền tối tối ưu cho đồ thị tài chính
    tooltip={"text": "{tooltip_text}"}
)

st.pydeck_chart(r)
