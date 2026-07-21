import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Cấu hình trang giao diện Web (Đặt ở đầu file)
st.set_page_config(
    page_title="Bản đồ Dòng chảy Tiền tệ Việt Nam",
    page_icon="🇻🇳",
    layout="wide"
)

st.title("🇻🇳 Mô phỏng Bản đồ Dòng chảy Tiền tệ 3 Tầng")
st.markdown("Hệ thống hiển thị luồng dịch chuyển tiền tệ dựa trên tọa độ địa lý thực tế tại Việt Nam.")

# 2. Thanh điều khiển kịch bản kinh tế
st.sidebar.header("⚙️ Kịch bản Hệ thống")
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống:",
    options=["Bình thường", "Khi có BIẾN (Khủng hoảng)"]
)

# 3. Định nghĩa tọa độ địa lý các chủ thể tại Việt Nam
# [Vĩ độ (Latitude), Kinh độ (Longitude)]
locations = {
    "QUOC_TE": {"coords": [22.0, 110.0], "name": "🌐 Thị trường Quốc tế (FDI, FII, IMF)", "color": "purple"},
    "QUOC_GIA": {"coords": [21.0285, 105.8542], "name": "🏛️ Trung ương / Cấp Quốc gia (Hà Nội - NHTW)", "color": "blue"},
    "TINH_CHINH_QUYEN": {"coords": [16.0544, 108.2022], "name": "🏢 Cấp Tỉnh (Chính quyền & Kho bạc Tỉnh)", "color": "orange"},
    "TINH_DOANH_NGHIEP": {"coords": [16.4637, 107.5909], "name": "🏭 Khu Công nghiệp / DN lớn cấp Tỉnh", "color": "darkblue"},
    "XA_CHINH_QUYEN": {"coords": [15.5673, 108.4812], "name": "🔰 Cấp Xã (Ủy ban Nhân dân xã vùng nông thôn)", "color": "cadetblue"},
    "XA_DAN_CU": {"coords": [15.4573, 108.5512], "name": "🏡 Hộ Gia đình / Nông dân (Kinh tế vi mô)", "color": "green"}
}

# 4. Cấu hình dữ liệu luồng tiền tệ dựa trên kịch bản chọn
flows = []
description = ""

if scenario == "Bình thường":
    description = "🔵 **Trạng thái ổn định**: Tiền thuế luân chuyển nhịp nhàng từ xã lên tỉnh, lên trung ương. Dòng vốn FDI và đơn hàng quốc tế liên tục đổ về doanh nghiệp lớn tạo công ăn việc làm, trả lương đều đặn kích cầu tiêu dùng nông thôn."
    flows = [
        {"from": "QUOC_TE", "to": "TINH_DOANH_NGHIEP", "label": "Bơm vốn đầu tư FDI", "color": "#1f77b4"},
        {"from": "TINH_DOANH_NGHIEP", "to": "QUOC_GIA", "label": "Nộp thuế xuất nhập khẩu", "color": "#1f77b4"},
        {"from": "QUOC_GIA", "to": "TINH_CHINH_QUYEN", "label": "Phân bổ ngân sách điều tiết", "color": "#1f77b4"},
        {"from": "TINH_CHINH_QUYEN", "to": "XA_CHINH_QUYEN", "label": "Hỗ trợ hạ tầng phát triển nông thôn", "color": "#1f77b4"},
        {"from": "TINH_DOANH_NGHIEP", "to": "XA_DAN_CU", "label": "Trả lương công nhân & Thu mua sản phẩm", "color": "#1f77b4"},
        {"from": "XA_DAN_CU", "to": "TINH_DOANH_NGHIEP", "label": "Tiêu dùng hàng hóa dịch vụ sản xuất", "color": "#1f77b4"},
        {"from": "XA_DAN_CU", "to": "XA_CHINH_QUYEN", "label": "Nộp phí, thuế địa phương", "color": "#1f77b4"},
        {"from": "XA_CHINH_QUYEN", "to": "TINH_CHINH_QUYEN", "label": "Nộp nghĩa vụ ngân sách tuyến trên", "color": "#1f77b4"}
    ]
else:
    description = "⚠️ **Kịch bản Khủng hoảng (Có BIẾN)**: Kích hoạt dòng tiền phòng thủ. Tiền mặt tháo chạy khỏi sản xuất và dịch vụ rủi ro để quay ngược dòng về trú ẩn tại két sắt nhà dân hoặc hệ thống tài sản quốc gia an toàn (Ngân hàng quốc doanh, Vàng, USD). Vốn ngoại rút rỗng khỏi biên giới."
    flows = [
        {"from": "QUOC_GIA", "to": "QUOC_TE", "label": "💸 Vốn ngoại tháo chạy (Capital Flight)", "color": "#d62728"}, # Đỏ: Xả ra
        {"from": "QUOC_TE", "to": "QUOC_GIA", "label": "🟢 Tiếp cận cứu trợ tài chính vĩ mô quốc tế", "color": "#2ca02c"}, # Xanh: Đổ vào
        {"from": "TINH_DOANH_NGHIEP", "to": "QUOC_GIA", "label": "🟢 Đổi nội tệ lấy USD / Vàng bảo toàn vốn", "color": "#2ca02c"},
        {"from": "QUOC_GIA", "to": "TINH_CHINH_QUYEN", "label": "🟢 Giải ngân Đầu tư công khẩn cấp", "color": "#2ca02c"},
        {"from": "TINH_DOANH_NGHIEP", "to": "TINH_CHINH_QUYEN", "label": "💸 Thất thu thuế (Đóng băng nhà máy)", "color": "#d62728"},
        {"from": "TINH_CHINH_QUYEN", "to": "XA_CHINH_QUYEN", "label": "🟢 Bơm ngân sách cứu trợ an sinh xã hội", "color": "#2ca02c"},
        {"from": "XA_DAN_CU", "to": "QUOC_GIA", "label": "🟢 Gửi tiết kiệm Ngân hàng quốc doanh lớn", "color": "#2ca02c"},
        {"from": "XA_DAN_CU", "to": "TINH_DOANH_NGHIEP", "label": "💸 Thắt lưng buộc bụng, ngừng tiêu dùng", "color": "#d62728"}
    ]

# 5. Khởi tạo bản đồ Folium, đặt trung tâm ở khu vực miền trung Việt Nam
m = folium.Map(location=[16.5, 107.5], zoom_start=6, tiles="CartoDB positron")

# Thêm các điểm mốc (Markers) đại diện cho các chủ thể
for key, info in locations.items():
    folium.Marker(
        location=info["coords"],
        popup=info["name"],
        tooltip=info["name"],
        icon=folium.Icon(color=info["color"], icon="info-sign")
    ).add_to(m)

# Vẽ các đường dòng chảy tiền tệ (AntPath để tạo hiệu ứng chuyển động dòng nước)
for flow in flows:
    start_coords = locations[flow["from"]]["coords"]
    end_coords = locations[flow["to"]]["coords"]
    
    # Tạo đường di chuyển có hướng trên nền bản đồ
    folium.PolyLine(
        locations=[start_coords, end_coords],
        color=flow["color"],
        weight=4,
        opacity=0.8,
        tooltip=flow["label"],
        popup=flow["label"]
    ).add_to(m)

# 6. Hiển thị bố cục trên Streamlit Web
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Tổng quan Kịch bản")
    st.info(description)
    
    st.subheader("💡 Hướng dẫn xem bản đồ")
    st.markdown("""
    *   **Di chuột vào các bong bóng định vị** để xem tên chủ thể kinh tế (Xã, Tỉnh, Quốc gia).
    *   **Di chuột trực tiếp vào các đường liên kết** để đọc nội dung dòng tiền luân chuyển tương ứng.
    """)
    if scenario == "Khi có BIẾN (Khủng hoảng)":
        st.error("🔴 Đường Đỏ: Luồng tháo chạy vốn / Đóng băng suy thoái.")
        st.success("🟢 Đường Xanh Lá: Luồng dòng tiền co cụm phòng thủ an toàn.")
    else:
        st.info("🔵 Đường Xanh Dương: Luồng tiền tệ thông suốt bình thường.")

with col2:
    st.subheader("🗺️ Bản đồ Số hóa Hệ thống Kinh tế")
    # Render bản đồ tương tác trực tiếp lên trang web
    st_folium(m, width=900, height=650)
