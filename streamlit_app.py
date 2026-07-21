import streamlit as st
import pandas as pd
import pydeck as pdk

# 1. Cấu hình giao diện Streamlit màn hình rộng và ép nền đen (Dark Mode)
st.set_page_config(layout="wide", page_title="Global Multi-Layer Money Flow")

# CSS bổ sung để ép toàn bộ giao diện Streamlit sang màu đen tuyệt đối
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    h1, p, span, div {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 Hệ Thống Toàn Cảnh Dòng Chảy Tiền Tệ Đa Tầng Toàn Cầu")
st.caption("Bản đồ gộp tổng thể kết nối xuyên suốt từ cấp cơ sở (Xã/Huyện/Tỉnh) nội địa lên cấp Nhà nước và phóng đi Liên lục địa.")

# 2. Cơ sở dữ liệu tọa độ địa lý thực tế (Gộp chung tất cả các tầng vào 1 hệ thống)
# Định dạng: [Kinh độ (Longitude), Vĩ độ (Latitude)]
global_locations = {
    # === CỤM VIỆT NAM (Dòng chảy từ đáy vi mô lên vĩ mô) ===
    "VN_Xa_CoSo": [106.2400, 20.9400],         # 1. Tế bào cấp Xã
    "VN_Huyen_Hub": [106.2800, 20.9800],       # 2. Trạm trung chuyển cấp Huyện
    "VN_Tinh_Center": [106.3330, 20.9409],     # 3. Điều phối vùng cấp Tỉnh
    "VN_HaNoi_Central": [105.8542, 21.0285],   # 4. Bộ não vĩ mô cấp Nhà nước (Hà Nội)

    # === CỤM MỸ (BẮC MỸ) ===
    "US_Rural_Commune": [-95.7129, 37.0902],    # Cấp cơ sở Mỹ (Kansas)
    "US_District_Hub": [-87.6298, 41.8781],     # Cấp trung gian Mỹ (Chicago)
    "US_NewYork_WallStreet": [-74.0113, 40.7075], # Bộ não tài chính Mỹ (Phố Wall)

    # === CỤM CHÂU ÂU (EU) ===
    "EU_Local_Production": [7.4653, 46.9480],   # Cấp cơ sở sản xuất Châu Âu (Thụy Sĩ)
    "EU_Frankfurt_Central": [8.6821, 50.1109],  # Trung tâm tiền tệ Châu Âu (ECB Frankfurt)

    # === CỤM TRẠM TRUNG CHUYỂN QUỐC TẾ ===
    "Singapore_Global_Hub": [103.8198, 1.3521], # Trung tâm điều phối vốn Đông Nam Á
    "Japan_Tokyo_Central": [139.6503, 35.6762]  # Trung tâm tài chính Đông Á
}

# 3. Danh sách dòng chảy MẠNG LƯỚI TỔNG HỢP (Gộp chung toàn bộ mạch máu kinh tế)
global_flows = [
    # ------------------ MẠCH MÁU NỘI ĐỊA VIỆT NAM (Dọc) ------------------
    {"from": "VN_Xa_CoSo", "to": "VN_Huyen_Hub", "status": "neutral", "desc": "[CẤP XÃ ➔ HUYỆN] Dân gửi tiền tích lũy lên hệ thống tín dụng"},
    {"from": "VN_Huyen_Hub", "to": "VN_Tinh_Center", "status": "strong_in", "desc": "[CẤP HUYỆN ➔ TỈNH] Doanh nghiệp nộp thuế sản xuất công nghiệp về Tỉnh"},
    {"from": "VN_Tinh_Center", "to": "VN_HaNoi_Central", "status": "strong_out", "desc": "[CẤP TỈNH ➔ NHÀ NƯỚC] Tỉnh kết chuyển thặng dư ngân sách về Trung ương"},

    # ------------------ MẠCH MÁU NỘI ĐỊA MỸ (Dọc) ------------------
    {"from": "US_Rural_Commune", "to": "US_District_Hub", "status": "strong_in", "desc": "[CẤP CƠ SỞ MỸ] Nông sản thô từ trang trại đổ về nhà máy chế biến Chicago"},
    {"from": "US_District_Hub", "to": "US_NewYork_WallStreet", "status": "strong_in", "desc": "[CẤP TRUNG GIAN MỸ] Dòng vốn doanh nghiệp niêm yết lên sàn New York"},

    # ------------------ MẠCH MÁU NỘI ĐỊA CHÂU ÂU (Dọc) ------------------
    {"from": "EU_Local_Production", "to": "EU_Frankfurt_Central", "status": "neutral", "desc": "[CẤP CƠ SỞ EU] Dòng tiền tiết kiệm Euro luân chuyển về ECB"},

    # ------------------ LIÊN KẾT XUYÊN LỤC ĐỊA (Ngang - Toàn cầu) ------------------
    {"from": "US_NewYork_WallStreet", "to": "Singapore_Global_Hub", "status": "strong_in", "desc": "[XUYÊN LỤC ĐỊA] Dòng vốn đầu tư từ Mỹ phóng sang tài chính Châu Á"},
    {"from": "Singapore_Global_Hub", "to": "VN_Huyen_Hub", "status": "strong_in", "desc": "[XUYÊN BIÊN GIỚI] Vốn ngoại FDI bơm thẳng vào cụm công nghiệp Huyện tại Việt Nam"},
    {"from": "VN_HaNoi_Central", "to": "Japan_Tokyo_Central", "status": "strong_in", "desc": "[QUỐC TẾ] Việt Nam xuất khẩu hàng hóa công nghệ sang Nhật Bản thu ngoại tệ mạnh"},
    {"from": "EU_Frankfurt_Central", "to": "US_NewYork_WallStreet", "status": "strong_out", "desc": "[XUYÊN ĐẠI DƯƠNG] Giới đầu tư Châu Âu rút vốn, chuyển dịch sang tài sản đô-la Mỹ an toàn"},
    {"from": "Japan_Tokyo_Central", "to": "US_NewYork_WallStreet", "status": "neutral", "desc": "[TOÀN CẦU] Nhật Bản luân chuyển dòng vốn mua Trái phiếu Chính phủ Mỹ"}
]

# 4. Định nghĩa mã màu dạng danh sách RGBA chuẩn của Pydeck
color_map = {
    "strong_in": [0, 255, 0, 200],     # 🟢 Xanh lá: Dòng tiền vào mạnh / Mua mạnh
    "strong_out": [255, 0, 0, 200],    # 🔴 Đỏ: Dòng tiền rút mạnh / Bán tháo
    "neutral": [255, 255, 0, 220],    # 🟡 Vàng: Sự lưỡng lự / Đi ngang
}

# 5. Xử lý dữ liệu nạp chung vào một bảng duy nhất
processed_data = []
for flow in global_flows:
    start_coords = global_locations[flow["from"]]
    end_coords = global_locations[flow["to"]]
    
    processed_data.append({
        "from_lon": start_coords[0], "from_lat": start_coords[1],
        "to_lon": end_coords[0], "to_lat": end_coords[1],
        "color": color_map[flow["status"]],
        "tooltip_text": flow["desc"]
    })

df = pd.DataFrame(processed_data)

# 6. Khởi tạo lớp xử lý đồ họa ArcLayer (Hiển thị đồng thời tất cả các luồng dây)
network_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position=["from_lon", "from_lat"],
    get_target_position=["to_lon", "to_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width=4,            # Độ dày sợi dây vừa phải để không bị rối mắt khi gộp chung
    pickable=True,
    auto_highlight=True
)

# 7. Cấu hình góc nhìn camera vĩ mô bao quát từ không gian
view_state = pdk.ViewState(
    latitude=20.0,
    longitude=40.0,
    zoom=1.3,               # Thu nhỏ góc nhìn để nhìn thấy toàn bộ hành tinh kết nối
    pitch=45,               # Nghiêng góc 45 độ để tạo hiệu ứng vòm cong 3D cho sợi dây dòng tiền
    bearing=0
)

# 8. Render bản đồ lên giao diện (Sử dụng style tối nhất CartoDB Dark Matter)
r = pdk.Deck(
    layers=[network_layer],
    initial_view_state=view_state,
    map_style="https://cartocdn.com", # Nền tối huyền bí tôn vinh các sợi dây màu
    tooltip={"text": "{tooltip_text}"}
)

st.pydeck_chart(r)
