import streamlit as st
import data_loader as dl
import charts as cr

# 1. CẤU HÌNH GIAO DIỆN TRỰC QUAN TOÀN MÀN HÌNH
st.set_page_config(page_title="Hệ Thống Dòng Tiền Toàn Cầu 195 Quốc Gia", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 BẢN ĐỒ LUỒNG VỐN VÀ MẠNG LƯỚI KINH TẾ TOÀN CẦU")
st.caption("Hệ thống mô phỏng dòng chảy tiền tệ tương tác vật lý 100% trên biểu đồ địa lý từ cấp Toàn cầu đến Đối tượng vi mô.")

# Khởi tạo trạng thái bộ nhớ đệm để lưu vết hành vi click của người dùng
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# ĐIỀU KHIỂN TRẠNG THÁI USD NGAY TRÊN ĐẦU MÀN HÌNH CHÍNH
st.markdown("### 🕹️ CHỌN TRẠNG THÁI CHỈ SỐ ĐỒNG ĐÔ LA MỸ (USD / DXY)")
usd_mode = st.segmented_control(
    "Trạng thái USD hiện tại:",
    options=["USD MẠNH LÊN (Hút thanh khoản 📈)", "USD YẾU ĐI (Bung xõa đầu tư 📉)"],
    default="USD MẠNH LÊN (Hút thanh khoản 📈)"
)
is_usd_strong = "MẠNH" in usd_mode
line_color = "#FF4B4B" if is_usd_strong else "#00D46A"

# Load cơ sở dữ liệu vĩ mô từ tệp data_loader
df_global = dl.load_economic_database()

# =============================================================================
# CHẾ ĐỘ 1: BẢN ĐỒ TOÀN CẦU (THU NHỎ)
# =============================================================================
if st.session_state.selected_country is None:
    st.markdown("### 🗺️ CHẾ ĐỘ TOÀN CẦU: CLICK CHỌN MỘT QUỐC GIA ĐỂ ZOOM IN ĐỊA LÝ VI MÔ")
    
    fig = cr.draw_global_map(df_global, line_color)
    
    # Bắt sự kiện click tương tác hai chiều
    selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
    
    if selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
        point_data = selected_points["selection"]["points"]
        if len(point_data) > 0 and "customdata" in point_data[0]:
            st.session_state.selected_country = point_data[0]["customdata"]
            st.rerun()

# =============================================================================
# CHẾ ĐỘ 2: BẢN ĐỒ PHÓNG TO ĐỊA LÝ VI MÔ (XỬ LÝ ĐÚNG LỀ CÚ PHÁP CHUẨN)
# =============================================================================
else:
    country = st.session_state.selected_country
    st.markdown(f"### 🔬 CHẾ ĐỘ VI MÔ: BỘ MÁY KINH TẾ TRÊN BẢN ĐỒ ĐỊA LÝ ({country.upper()})")
    
    if st.button("⬅️ QUAY LẠI BẢN ĐỒ TOÀN CẦU"):
        st.session_state.selected_country = None
        st.rerun()
        
    # Lấy tọa độ trung tâm của quốc gia được chọn từ database nền
    target_country = df_global[df_global['NAME'] == country].iloc[0]
    c_lat, c_lon = target_country['LAT'], target_country['LON']
        
    # Gọi cấu trúc phân cấp địa lý thực tế
    nodes, edges = dl.get_geographic_hierarchy(country, c_lat, c_lon)
    
    # Vẽ mạng lưới vi mô lồng thẳng lên bản đồ địa lý đã Zoom sát
    fig_micro = cr.draw_geographic_micro_network(df_global, country, nodes, edges, line_color, c_lat, c_lon)
    st.plotly_chart(fig_micro, use_container_width=True)

# =============================================================================
# 3. KHỐI LOGIC BẢN CHẤT KINH TẾ (ĐỒNG BỘ HOÀN TOÀN THEO ĐỒ THỊ)
# =============================================================================
st.markdown("---")
st.markdown("### 🧱 LUỒNG CHẢY LOGIC VÀ ĐIỂM TRÚ ẨN CỦA TÀI SẢN CHI TIẾT")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌍 Bản Chất Luồng Tiền Vĩ Mô")
    if is_usd_strong:
        st.error("""
        * **Dòng tiền thế giới:** Bị hút ngược về tâm dịch thanh khoản là Hoa Kỳ do lãi suất USD quá cao. 
        * **Hiện tượng đồ thị:** Các sợi dây chuyển sang **MÀU ĐỎ** thể hiện tín hiệu co cụm, rút ròng tài sản rủi ro.
        * **Hành vi Quốc gia:** Các nước cạn kiệt dự trữ ngoại hối, buộc phải thắt chặt tiền tệ phòng thủ.
        """)
    else:
        st.success("""
        * **Dòng tiền thế giới:** Tiền rẻ từ Mỹ tràn ra 195 quốc gia (Mạng lưới sợi dây **MÀU XANH**).
        * **Xu hướng trú ẩn tài sản:** Tiền ồ ạt chảy mạnh vào **VÀNG VẬT CHẤT** như một tấm khiên chống lạm phát tối hậu khi tiền giấy mất giá.
        * **Hành vi Quốc gia:** Nới lỏng chính sách, kích thích sản xuất kinh doanh toàn diện.
        """)

with col_right:
    current_view = st.session_state.selected_country if st.session_state.selected_country else "Toàn cầu"
    st.markdown(f"#### 🎯 Hành Vi Thực Tế Tại Cấp Độ: {current_view}")
    if is_usd_strong:
        st.warning("""
        * **Cấp Tập đoàn / Doanh nghiệp:** Cắt giảm tối đa đòn bẩy tài chính, ngừng mở rộng quy mô, tất toán nợ gốc vay bằng USD để chặn đứng rủi ro lỗ tỷ giá.
        * **Cấp Nhà đầu tư cá nhân:** Tháo chạy khỏi chứng khoán, đóng trạng thái bất động sản đầu cơ. Đưa dòng tiền an toàn vào tài khoản tiết kiệm định danh cao.
        """)
    else:
        st.info("""
        * **Cấp Tập đoàn / Doanh nghiệp:** Bung vốn lớn chiếm lĩnh thị phần, vay nợ giá rẻ để đầu tư máy móc, tối ưu hóa năng suất khi chi phí dòng vốn thấp.
        * **Cấp Nhà đầu tư cá nhân:** Dòng vốn nhàn rỗi tấn công mạnh vào **Cổ phiếu tăng trưởng** và **Bất động sản phân khúc lõi** đô thị lớn để tối đa hóa biên lợi nhuận.
        """)
