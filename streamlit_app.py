import streamlit as st
import pydeck as pdk
import pandas as pd

# Cấu hình trang Streamlit chuẩn giao diện di động
st.set_page_config(page_title="Economic Cashflow Map", layout="centered")

# --- 1. KHỞI TẠO DỮ LIỆU BẢN ĐỒ KINH TẾ (Tọa độ giả lập) ---
# Các Vùng/Nút kinh tế (Từ lớn đến nhỏ)
nodes_data = [
    # TẦNG VĨ MÔ (Trung tâm)
    {"name": "Ngân hàng Trung ương", "lat": 21.0285, "lon": 105.8542, "type": "Macro", "size": 50000, "color":, "info": "Nguồn phát hành tiền & điều tiết lãi suất."},
    {"name": "Hệ thống Ngân hàng Thương mại", "lat": 21.0335, "lon": 105.8442, "type": "Macro", "size": 40000, "color":, "info": "Nơi điều phối vốn tín dụng."},
    
    # TẦNG TRUNG MÔ (Doanh nghiệp & Ngành nghề)
    {"name": "Khối Doanh nghiệp Sản xuất (B2B)", "lat": 21.0185, "lon": 105.8642, "type": "Meso", "size": 30000, "color":, "info": "Hấp thụ vốn, chi trả lương và sản xuất hàng hóa."},
    {"name": "Tập đoàn Bất động sản", "lat": 21.0085, "lon": 105.8342, "type": "Meso", "size": 25000, "color":, "info": "Kênh thâm dụng vốn lớn, rủi ro đóng băng dòng tiền cao."},
    
    # TẦNG VI MÔ (Hộ kinh doanh & Cá nhân)
    {"name": "Sàn TMĐT & Chuỗi Bán lẻ (B2C)", "lat": 21.0385, "lon": 105.8742, "type": "Micro", "size": 15000, "color":, "info": "Nơi dòng tiền quay vòng nhanh nhất từ người dân."},
    {"name": "Hộ kinh doanh nhỏ lẻ (Tiệm Cafe, Tạp hóa)", "lat": 21.0425, "lon": 105.8592, "type": "Micro", "size": 8000, "color":, "info": "Dòng tiền bán lẻ tiền mặt hàng ngày."},
    {"name": "Khu dân cư (Người lao động/Cá nhân)", "lat": 21.0205, "lon": 105.8142, "type": "Micro", "size": 12000, "color":, "info": "Cung cấp sức lao động, nhận lương và chi tiêu tiêu dùng."}
]
df_nodes = pd.DataFrame(nodes_data)

# Các luồng tiền chạy giữa các nút (Tuyến đường dòng tiền)
flows_data = [
    {"from": "Ngân hàng Trung ương", "to": "Hệ thống Ngân hàng Thương mại", "flow_speed": 5, "width": 8, "color": [255, 0, 0]},
    {"from": "Hệ thống Ngân hàng Thương mại", "to": "Khối Doanh nghiệp Sản xuất (B2B)", "flow_speed": 3, "width": 6, "color": [0, 0, 255]},
    {"from": "Khối Doanh nghiệp Sản xuất (B2B)", "to": "Khu dân cư (Người lao động/Cá nhân)", "flow_speed": 2, "width": 4, "color": [255, 165, 0]},
    {"from": "Khu dân cư (Người lao động/Cá nhân)", "to": "Sàn TMĐT & Chuỗi Bán lẻ (B2C)", "flow_speed": 4, "width": 5, "color": [0, 255, 0]},
    {"from": "Khu dân cư (Người lao động/Cá nhân)", "to": "Hộ kinh doanh nhỏ lẻ (Tiệm Cafe, Tạp hóa)", "flow_speed": 4, "width": 3, "color": [0, 255, 128]},
    {"from": "Hộ kinh doanh nhỏ lẻ (Tiệm Cafe, Tạp hóa)", "to": "Hệ thống Ngân hàng Thương mại", "flow_speed": 3, "width": 3, "color": [0, 128, 128]},
]

# Tạo tọa độ đường nối từ-đến cho luồng tiền
paths = []
for flow in flows_data:
    f_node = df_nodes[df_nodes['name'] == flow['from']].iloc[0]
    t_node = df_nodes[df_nodes['name'] == flow['to']].iloc[0]
    paths.append({
        "path": [[f_node['lon'], f_node['lat']], [t_node['lon'], t_node['lat']]],
        "color": flow['color'],
        "width": flow['width']
    })

# --- 2. CẤU HÌNH CÁC LỚP HIỂN THỊ (LAYERS) ---
# Lớp các Nút kinh tế (Hình tròn đổ bóng nổi)
layer_nodes = pdk.Layer(
    "ScatterplotLayer",
    df_nodes,
    get_position="[lon, lat]",
    get_color="color",
    get_radius="size",
    radius_scale=0.03,
    pickable=True,
)

# Lớp luồng tiền chạy (Đường nối động)
layer_flows = pdk.Layer(
    "PathLayer",
    paths,
    get_path="path",
    get_color="color",
    get_width="width",
    width_min_pixels=2,
    pickable=False,
)

# Khởi tạo bản đồ góc nhìn từ trên cao (Mô phỏng Hà Nội làm tâm vũ trụ kinh tế)
view_state = pdk.ViewState(
    latitude=21.0285,
    longitude=105.8542,
    zoom=12,
    pitch=45 # Nghiêng 45 độ tạo hiệu ứng 3D giống iOS
)

# --- 3. GIAO DIỆN STREAMLIT (Mô phỏng Giao diện iPhone) ---
st.title("🗺️ Bản Đồ Dòng Tiền Kinh Tế")
st.caption("Hãy phóng to/thu nhỏ (Zoom) để xem dòng chảy từ Vĩ mô đến Hộ kinh doanh cá thể.")

# Khung tìm kiếm giống Google Maps
search_query = st.text_input("🔍 Tìm kiếm nút kinh tế (Ví dụ: Tiệm Cafe, Ngân hàng...)", placeholder="Nhập tên nút tài chính...")

# Bộ lọc tầng kinh tế
category = st.multiselect("Lọc tầng kinh tế:", ["Macro (Vĩ mô)", "Meso (Trung mô)", "Micro (Vi mô)"], default=["Macro (Vĩ mô)", "Meso (Trung mô)", "Micro (Vi mô)"])

# Hiển thị Bản đồ với giao diện Dark Mode huyền bí của tài chính
r = pdk.Deck(
    layers=[layer_flows, layer_nodes],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Nền tối làm nổi bật dòng tiền sáng
    tooltip={"text": "{name}\nTầng: {type}\nĐặc điểm: {info}"}
)
st.pydeck_chart(r)

# Thẻ thông tin trượt Bottom Sheet (Giả lập bằng cột cố định phía dưới bản đồ)
st.subheader("📱 Bảng Thông Tin Chi Tiết (Bottom Sheet)")
if search_query:
    match = df_nodes[df_nodes['name'].str.contains(search_query, case=False)]
    if not match.empty:
        for idx, row in match.iterrows():
            with st.expander(f"🟢 {row['name']} - Xem dòng chảy"):
                st.write(f"**Phân loại:** Tầng {row['type']}")
                st.write(f"**Mô tả hoạt động:** {row['info']}")
                st.metric(label="Chỉ số sức khỏe dòng tiền (Cashflow Health)", value="92%", delta="+4.2% tuần này")
    else:
        st.warning("Không tìm thấy nút tài chính này trên sơ đồ bản đồ.")
else:
    st.info("Bấm chọn hoặc tìm kiếm một địa điểm kinh tế trên bản đồ để xem biến động số dư và hóa đơn.")
