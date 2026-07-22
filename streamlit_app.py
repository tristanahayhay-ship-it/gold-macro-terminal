# streamlit_app.py
import streamlit as st
import data_loader as dl
import charts as cr

st.set_page_config(page_title="Hệ Thống Dòng Tiền Mapbox Toàn Cầu", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ BẢN ĐỒ KINH TẾ SỐ ĐA NGÀNH TOÀN CẦU (GOOGLE MAPS STYLE)")
st.caption("Mô phỏng luồng tiền tương tác vật lý. Khi Zoom sát vào đất nước sẽ tự động hiển thị vị trí các tài sản phòng thủ/đầu tư đa ngành.")

# Khởi tạo trạng thái bộ nhớ đệm
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# BỘ ĐIỀU KHIỂN TRẠNG THÁI USD
st.markdown("### 🕹️ TRẠNG THÁI CHỈ SỐ ĐỒNG ĐÔ LA MỸ (USD / DXY)")
usd_mode = st.segmented_control(
    "Trạng thái USD hiện tại:",
    options=["USD MẠNH LÊN (Hút thanh khoản 📈)", "USD YẾU ĐI (Bung xõa đầu tư 📉)"],
    default="USD MẠNH LÊN (Hút thanh khoản 📈)"
)
is_usd_strong = "MẠNH" in usd_mode
line_color = "#FF4B4B" if is_usd_strong else "#00D46A"

# Tải cơ sở dữ liệu vĩ mô
df_global = dl.load_economic_database()

# Nút thu nhỏ camera điều phối
if st.session_state.selected_country is not None:
    if st.button("⬅️ THU NHỎ CAMERA (QUAY LẠI TOÀN CẦU)"):
        st.session_state.selected_country = None
        st.rerun()

# Chuẩn bị dữ liệu vi mô dựa trên trạng thái camera hiện tại
locations_dict, edges_list = {}, []
if st.session_state.selected_country is not None:
    target = df_global[df_global['NAME'] == st.session_state.selected_country].iloc[0]
    locations_dict, edges_list = dl.get_google_maps_hierarchy(st.session_state.selected_country, target['LAT'], target['LON'])

# DỰNG BẢN ĐỒ SỐ HỢP NHẤT MAPBOX TRỰC TIẾP
fig = cr.draw_google_maps_economic_engine(df_global, st.session_state.selected_country, line_color, locations_dict, edges_list)

# Đón nhận hành vi Click chuột của người dùng ngay trên bản đồ nền Mapbox
selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

if st.session_state.selected_country is None and selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
    point_data = selected_points["selection"]["points"]
    if len(point_data) > 0 and "customdata" in point_data:
        st.session_state.selected_country = point_data[0]["customdata"]
        st.rerun()

# =============================================================================
# MA TRẬN BẢN CHẤT LOGIC KINH TẾ THEO CẤP ĐỘ ĐỊA ĐIỂM THỰC TẾ
# =============================================================================
st.markdown("---")
st.markdown("### 🧱 MA TRẬN ĐIỂM ĐẾN DÒNG TIỀN VÀ BẢN CHẤT CỦA CÁC LOẠI TÀI SẢN CHI TIẾT")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌍 Luồng Vốn Quốc Tế (Tương quan USD)")
    if is_usd_strong:
        st.error("❌ **USD MẠNH:** Lực hút thanh khoản kéo dòng tiền xuyên quốc gia dọc theo các sợi dây màu **ĐỎ** rút ròng về tài sản neo giữ tại Mỹ. Các nước sở tại bị ép thắt chặt tiền tệ.")
    else:
        st.success("✅ **USD YẾU:** Tiền rẻ bung xõa qua chuỗi mạch máu màu **XANH** tràn vào các nước có nền tảng sản xuất tốt và đổ mạnh vào **VÀNG VẬT CHẤT** tại các hầm dự trữ quốc gia.")

with col_right:
    view_name = st.session_state.selected_country if st.session_state.selected_country else "Toàn cầu"
    st.markdown(f"#### 🎯 Hoạt Động Đa Ngành Vi Mô Tại: {view_name}")
    if is_usd_strong:
        st.warning("🛡️ **Tài sản Phòng thủ lên ngôi:** Các Tập đoàn lớn dừng giải ngân dự án, ưu tiên gom tiền mặt gửi tiết kiệm lãi suất cao tại NHTW. Doanh nghiệp SME co cụm cắt giảm đòn bẩy vay USD.")
    else:
        st.info("🚀 **Tài sản Tấn công bùng nổ:** Dòng vốn rẻ kích hoạt các Quỹ đầu tư đẩy tiền mạnh vào **Cổ phiếu tăng trưởng**, các Tập đoàn thâu tóm quỹ đất xây **Bất động sản phân khúc lõi** đô thị.")
