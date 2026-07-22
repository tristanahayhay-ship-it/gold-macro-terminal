# streamlit_app.py
import streamlit as st
import data_loader as dl
import charts as cr

st.set_page_config(page_title="Hệ Thống Dòng Tiền Toàn Cầu 195 Quốc Gia", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 BẢN ĐỒ LUỒNG VỐN VÀ MẠNG LƯỚI KINH TẾ TOÀN CẦU")
st.caption("Hệ thống mô phỏng dòng chảy tiền tệ tương tác Zoom tại chỗ 100% trên một bản đồ địa lý duy nhất.")

# Quản lý trạng thái Zoom của người dùng qua bộ nhớ đệm Session State
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

# Nút quay lại toàn cầu (Chỉ hiển thị khi camera đang ở trạng thái phóng to vi mô)
if st.session_state.selected_country is not None:
    if st.button("⬅️ THU NHỎ CAMERA (QUAY LẠI BẢN ĐỒ TOÀN CẦU)"):
        st.session_state.selected_country = None
        st.rerun()

# HIỂN THỊ BẢN ĐỒ CHUNG DUY NHẤT (TỰ ZOOM VÀ HIỆN MẠNG LƯỚI NỘI TẠI KHI CLICK)
fig = cr.draw_unified_economic_map(df_global, st.session_state.selected_country, is_usd_strong, line_color)

# Lắng nghe hành vi nhấp chuột của người dùng trực tiếp trên bản đồ thế giới
selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

if st.session_state.selected_country is None and selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
    point_data = selected_points["selection"]["points"]
    if len(point_data) > 0 and "customdata" in point_data:
        st.session_state.selected_country = point_data[0]["customdata"]
        st.rerun()

# =============================================================================
# KHỐI PHÂN TÍCH MA TRẬN BẢN CHẤT LOGIC KINH TẾ (ĐỒNG BỘ CHẶT CHẼ)
# =============================================================================
st.markdown("---")
st.markdown("### 🧱 LUỒNG CHẢY LOGIC VÀ ĐIỂM TRÚ ẨN CỦA TÀI SẢN CHI TIẾT")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌍 Bản Chất Luồng Tiền Vĩ Mô")
    if is_usd_strong:
        st.error("❌ **USD MẠNH:** Thanh khoản bị hút mạnh về Hoa Kỳ. Các sợi dây chuyển sang **MÀU ĐỎ**, các quốc gia bị rút ròng tài sản vốn.")
    else:
        st.success("✅ **USD YẾU:** Tiền rẻ bung xõa qua chuỗi dây **MÀU XANH** đổ dồn vào **VÀNG VẬT CHẤT** để bảo chứng tài sản chống lạm phát.")

with col_right:
    current_view = st.session_state.selected_country if st.session_state.selected_country else "Toàn cầu"
    st.markdown(f"#### 🎯 Hành Vi Thực Tế Tại Cấp Độ: {current_view}")
    if is_usd_strong:
        st.warning("🛡️ **Phòng thủ vĩ mô:** Doanh nghiệp ngừng dùng đòn bẩy vay nợ USD. Nhà đầu tư rút tiền khỏi chứng khoán gửi tiết kiệm lãi suất cao.")
    else:
        st.info("🚀 **Tấn công tài sản:** Doanh nghiệp mở rộng sản xuất với chi phí vốn thấp. Nhà đầu tư gom mạnh Cổ phiếu tăng trưởng và Bất động sản lõi.")
