# streamlit_app.py
import streamlit as st
import data_loader as dl
import charts as cr

st.set_page_config(page_title="Hệ Thống Dòng Tiền Toàn Cầu 195 Quốc Gia", layout="wide")

st.title("🌐 BẢN ĐỒ LUỒNG VỐN VÀ MẠNG LƯỚI KINH TẾ TOÀN CẦU")
st.caption("Hệ thống mô phỏng dòng chảy tiền tệ tương tác vật lý 100% trên biểu đồ từ cấp Toàn cầu đến Nhà đầu tư vi mô.")

# Quản lý trạng thái Click của người dùng qua bộ nhớ đệm Session State
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# 1. Bộ điều khiển trạng thái USD nằm trực tiếp trên giao diện chính
st.markdown("### 🕹️ CHỌN TRẠNG THÁI CHỈ SỐ ĐỒNG ĐÔ LA MỸ (USD / DXY)")
usd_mode = st.segmented_control(
    "Trạng thái USD hiện tại:",
    options=["USD MẠNH LÊN (Hút thanh khoản 📈)", "USD YẾU ĐI (Bung xõa đầu tư 📉)"],
    default="USD MẠNH LÊN (Hút thanh khoản 📈)"
)
is_usd_strong = "MẠNH" in usd_mode
line_color = "#FF4B4B" if is_usd_strong else "#00D46A"

# Load cơ sở dữ liệu vĩ mô
df_global = dl.load_economic_database()

# 2. Xử lý hiển thị đồ họa tương tác dựa trên trạng thái thu phóng bản đồ
if st.session_state.selected_country is None:
    st.markdown("### 🗺️ CHẾ ĐỘ TOÀN CẦU: CLICK CHỌN MỘT QUỐC GIA ĐỂ ZOOM IN VI MÔ")
    
    fig = cr.draw_global_map(df_global, line_color)
    
    # Bắt sự kiện click hai chiều thế hệ mới thông qua on_select="rerun"
    selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
    
    if selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
        point_data = selected_points["selection"]["points"]
        if len(point_data) > 0 and "customdata" in point_data[0]:
            st.session_state.selected_country = point_data[0]["customdata"]
            st.rerun()
else:
    country = st.session_state.selected_country
    st.markdown(f"### 🔬 CHẾ ĐỘ VI MÔ: BỘ MÁY KINH TẾ TRONG NƯỚC ({country.upper()})")
    
    if st.button("⬅️ QUAY LẠI BẢN ĐỒ TOÀN CẦU"):
        st.session_state.selected_country = None
        st.rerun()
        
    nodes, edges = dl.get_micro_hierarchy(country)
    fig_micro = cr.draw_micro_network(nodes, edges, line_color)
    st.plotly_chart(fig_micro, use_container_width=True)

# 3. Khối hiển thị ma trận bản chất kinh tế đồng bộ theo trạng thái đồ thị
st.markdown("---")
st.markdown("### 🧱 LUỒNG CHẢY LOGIC VÀ ĐIỂM TRÚ ẨN CỦA TÀI SẢN CHI TIẾT")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌍 Bản Chất Luồng Tiền Vĩ Mô")
    if is_usd_strong:
        st.error("❌ **USD MẠNH:** Thanh khoản bị hút mạnh về Hoa Kỳ. Các sợi dây chuyển sang **MÀU ĐỎ**, các quốc gia bị rút ròng tài sản vốn.")
    else:
        st.success("✅ **USD YẾU:** Tiền rẻ bung xõa qua chuỗi dây **MÀU XANH** đổ dồn vào **VÀNG VẬT CHẤT** để bảo chứng tài sản chống mất giá.")

with col_right:
    current_view = st.session_state.selected_country if st.session_state.selected_country else "Toàn cầu"
    st.markdown(f"#### 🎯 Hành Vi Thực Tế Tại Cấp Độ: {current_view}")
    if is_usd_strong:
        st.warning("🛡️ **Phòng thủ vĩ mô:** Doanh nghiệp ngừng dùng đòn bẩy vay nợ USD. Nhà đầu tư rút tiền khỏi chứng khoán gửi tiết kiệm lãi suất cao.")
    else:
        st.info("🚀 **Tấn công tài sản:** Doanh nghiệp mở rộng sản xuất với chi phí vốn thấp. Nhà đầu tư gom mạnh Cổ phiếu tăng trưởng và Bất động sản lõi.")
