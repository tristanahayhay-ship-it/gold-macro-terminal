import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Cấu hình trang giao diện Web toàn màn hình
st.set_page_config(
    page_title="Bản đồ Dòng chảy Tiền tệ Toàn cầu",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Mô phỏng Bản đồ Dòng chảy Tiền tệ Toàn cầu (Từ Vi mô đến Vĩ mô)")
st.markdown("Hệ thống mô phỏng cách dòng tiền dịch chuyển xuyên biên giới giữa các trung tâm kinh tế lớn và các tầng kinh tế tại Việt Nam.")

# 2. Thanh điều khiển kịch bản toàn cầu
st.sidebar.header("⚙️ Kịch bản Khủng hoảng")
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống thế giới:",
    options=["Bình thường", "Khi Toàn cầu có BIẾN (Khủng hoảng)"]
)

# 3. Định nghĩa tọa độ các điểm nút trục kinh tế Thế giới & Việt Nam
# [Vĩ độ, Kinh độ]
locations = {
    # Trục quốc tế
    "WALL_STREET": {"coords": [40.7128, -74.0060], "name": "🇺🇸 Trung tâm Tài chính Mỹ (Wall Street - Trú ẩn toàn cầu)", "color": "red"},
    "CHAU_AU": {"coords": [50.1109, 8.6821], "name": "🇪🇺 Ngân hàng Trung ương Châu Âu (Frankfurt)", "color": "purple"},
    "TRUNG_QUOC": {"coords": [31.2304, 121.4737], "name": "🇨🇳 Công xưởng Thế giới (Thượng Hải - Chuỗi cung ứng)", "color": "darkred"},
    
    # Trục Việt Nam (3 tầng từ vĩ mô đến vi mô)
    "VN_TRUNG_UONG": {"coords": [21.0285, 105.8542], "name": "🏛️ TẦNG 3: Trung ương Việt Nam (Hà Nội - NHTW)", "color": "blue"},
    "VN_CAP_TINH": {"coords": [16.0544, 108.2022], "name": "🏢 TẦNG 2: Cấp Tỉnh / Khu công nghiệp FDI (Đà Nẵng)", "color": "orange"},
    "VN_CAP_XA": {"coords": [10.8231, 106.6297], "name": "🏡 TẦNG 1: Cấp Xã / Hộ gia đình sản xuất (Khu vực phía Nam)", "color": "green"}
}

# 4. Thiết lập luồng dịch chuyển dòng tiền toàn cầu
flows = []
description = ""

if scenario == "Bình thường":
    description = "🔵 **Môi trường toàn cầu ổn định**: Dòng vốn đầu tư nước ngoài (FDI/FII) chảy mạnh từ Mỹ và Châu Âu vào chuỗi sản xuất Trung Quốc và Việt Nam. Các nhà máy cấp Tỉnh hoạt động hết công suất, xuất khẩu hàng hóa ra thế giới và trả lương đều đặn, kích thích dòng tiền tiêu dùng luân chuyển mạnh mẽ xuống tận cấp Xã."
    flows = [
        {"from": "WALL_STREET", "to": "VN_TRUNG_UONG", "label": "Dòng vốn đầu tư tài chính quốc tế (FII)", "color": "#1f77b4"},
        {"from": "CHAU_AU", "to": "VN_CAP_TINH", "label": "Đơn hàng xuất khẩu dệt may/điện tử sang EU", "color": "#1f77b4"},
        {"from": "TRUNG_QUOC", "to": "VN_CAP_TINH", "label": "Nhập khẩu nguyên vật liệu đầu vào linh kiện", "color": "#1f77b4"},
        {"from": "VN_TRUNG_UONG", "to": "VN_CAP_TINH", "label": "Phân bổ ngân sách phát triển hạ tầng", "color": "#1f77b4"},
        {"from": "VN_CAP_TINH", "to": "VN_CAP_XA", "label": "Tiền lương công nhân và tiền thu mua nông sản", "color": "#1f77b4"},
        {"from": "VN_CAP_XA", "to": "VN_CAP_TINH", "label": "Tiêu dùng nhu yếu phẩm, phân bón sản xuất", "color": "#1f77b4"},
        {"from": "VN_CAP_TINH", "to": "VN_TRUNG_UONG", "label": "Nộp thuế doanh nghiệp về ngân sách quốc gia", "color": "#1f77b4"}
    ]
else:
    description = "⚠️ **Khủng hoảng toàn cầu (Có BIẾN)**: Khối ngoại hoảng loạn kích hoạt cơ chế rút vốn. Tiền tháo chạy xuyên biên giới, xả mạnh khỏi thị trường Việt Nam để gom về mua Trái phiếu Chính phủ Mỹ và giữ USD tại Wall Street. Đơn hàng quốc tế bị hủy làm các nhà máy cấp Tỉnh đóng băng, dòng tiền lương đổ về nông thôn cấp Xã bị rút rỗng, người dân siết chặt tiêu dùng phòng thủ."
    flows = [
        {"from": "VN_TRUNG_UONG", "to": "WALL_STREET", "label": "💸 Vốn ngoại tháo chạy (Capital Flight về Mỹ)", "color": "#d62728"}, # Đỏ: Tháo chạy
        {"from": "VN_CAP_TINH", "to": "WALL_STREET", "label": "💸 Đứt gãy đơn hàng, rút rỗng dòng tiền doanh nghiệp", "color": "#d62728"},
        {"from": "TRUNG_QUOC", "to": "VN_CAP_TINH", "label": "💸 Đình trệ chuỗi cung ứng nguyên liệu", "color": "#d62728"},
        {"from": "VN_TRUNG_UONG", "to": "VN_CAP_TINH", "label": "🟢 Ngân hàng Nhà nước bơm vốn cứu trợ, hạ lãi suất", "color": "#2ca02c"}, # Xanh: Phòng thủ
        {"from": "VN_CAP_TINH", "to": "VN_CAP_XA", "label": "💸 Sa thải lao động, dòng tiền lương sụt giảm 80%", "color": "#d62728"},
        {"from": "VN_CAP_XA", "to": "VN_TRUNG_UONG", "label": "🟢 Người dân ôm tiền gửi tiết kiệm ngân hàng quốc doanh lớn", "color": "#2ca02c"}
    ]

# 5. Khởi tạo bản đồ Folium, đặt trung tâm ở khu vực Châu Á nhưng zoom rộng thấy cả thế giới
m = folium.Map(location=[25.0, 40.0], zoom_start=3, tiles="CartoDB positron")

# Thêm các vị trí mốc (Markers) cố định
for key, info in locations.items():
    folium.Marker(
        location=info["coords"],
        popup=info["name"],
        tooltip=info["name"],
        icon=folium.Icon(color=info["color"], icon="globe")
    ).add_to(m)

# Vẽ các đường liên kết luồng tiền chạy xuyên lục địa
for flow in flows:
    start_coords = locations[flow["from"]]["coords"]
    end_coords = locations[flow["to"]]["coords"]
    
    # Sử dụng PolyLine vẽ đường kết nối thẳng xuyên quốc gia
    folium.PolyLine(
        locations=[start_coords, end_coords],
        color=flow["color"],
        weight=4,
        opacity=0.7,
        tooltip=flow["label"],
        popup=flow["label"]
    ).add_to(m)

# 6. Đẩy cấu trúc hiển thị lên trang Streamlit Cloud
col1, col2 = st.columns([1, 2]) # Chia tỷ lệ cột trái nhỏ, cột bản đồ to để dễ nhìn

with col1:
    st.subheader("📋 Báo cáo tác động vĩ mô")
    st.info(description)
    
    st.subheader("🗺️ Bản đồ thế giới tương tác")
    st.markdown("""
    *   **Cuộn chuột** để phóng to/thu nhỏ toàn bộ bản đồ thế giới từ Mỹ sang Việt Nam.
    *   **Nhấp hoặc di chuột vào các đường chỉ hướng** nối giữa New York (Mỹ), Frankfurt (Đức), Thượng Hải (Trung Quốc) và Việt Nam để đọc bản chất dòng tiền.
    """)
    if scenario == "Khi Toàn cầu có BIẾN (Khủng hoảng)":
        st.error("🔴 Luồng Đỏ: Tiền tháo chạy xuyên biên giới hoặc đóng băng chuỗi giá trị.")
        st.success("🟢 Luồng Xanh lá: Biện pháp cứu trợ/Co cụm tài sản nội địa Việt Nam.")
    else:
        st.info("🔵 Luồng Xanh dương: Dòng vốn lưu thông tự do toàn cầu.")

with col2:
    st.subheader("🌐 Hệ thống dòng chảy tài chính vĩ mô toàn cầu")
    # Render bản đồ thế giới lên trình duyệt
    st_folium(m, width=1000, height=650)
