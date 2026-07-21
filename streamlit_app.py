import streamlit as st
import plotly.graph_objects as go

# 1. Cấu hình trang Dashboard
st.set_page_config(
    page_title="Gold Macro Terminal",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện Tiêu đề chính
st.title("🪙 GOLD MACRO TERMINAL")
st.subheader("Hệ thống Mô phỏng Chu kỳ Vĩ mô & Luân chuyển Dòng tiền")
st.markdown("---")

# 2. Thanh Sidebar điều khiển bối cảnh thị trường
st.sidebar.header("🎛️ BỘ ĐIỀU KHIỂN VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "Chọn Giai đoạn Chu kỳ Kinh tế:",
    ["1. Kinh tế Tăng trưởng (Risk-On)", "2. Kinh tế Suy thoái / Bất ổn (Risk-Off)"]
)

# Hiển thị các chỉ báo vĩ mô tương ứng ở Sidebar
if "Risk-On" in market_phase:
    st.sidebar.success("• Lãi suất: Thấp (Nới lỏng)")
    st.sidebar.success("• Lạm phát: Vừa phải (Tốt)")
    st.sidebar.success("• Địa chính trị: Ổn định")
    st.sidebar.success("• Tâm lý: Tham lam (FOMO)")
    bg_color = "#E8F8F5"
    line_color = "#1ABC9C"
    link_color = "rgba(26, 188, 156, 0.2)"
else:
    st.sidebar.error("• Lãi suất: Cao (Thắt chặt)")
    st.sidebar.error("• Lạm phát: Phi mã / Thiểu phát")
    st.sidebar.error("• Địa chính trị: Căng thẳng")
    st.sidebar.error("• Tâm lý: Sợ hãi (FUD)")
    bg_color = "#FDEDEC"
    line_color = "#E74C3C"
    link_color = "rgba(231, 76, 60, 0.2)"

# 3. Định nghĩa dữ liệu Sơ đồ Sankey (Dòng chảy tiền)
labels = [
    "HỆ THỐNG VĨ MÔ",                   # 0
    "Khối Doanh nghiệp",                # 1
    "Khối Cá nhân",                     # 2
    "Khối Định chế Tài chính",           # 3
    "Chính phủ & Ngân hàng TW",          # 4
    "Cổ phiếu Tăng trưởng & Đầu cơ",     # 5
    "Bất động sản Đầu cơ / Vùng ven",    # 6
    "Thị trường Crypto (Tài sản mới)",   # 7
    "Vàng vật chất & Vàng tài khoản",    # 8
    "Tiền mặt & Đồng tiền mạnh (USD)",   # 9
    "Trái phiếu CP & Ngành phòng thủ"    # 10
]

if "Risk-On" in market_phase:
    sources = [0, 0, 1, 1, 2, 2, 2]
    targets = [1, 2, 5, 6, 5, 6, 7]
    values  = [50, 50, 30, 20, 20, 20, 10]
else:
    sources = [0, 0, 3, 3, 3, 4, 4]
    targets = [3, 4, 8, 9, 10, 9, 10]
    values  = [60, 40, 30, 20, 10, 25, 15]

# Tạo biểu đồ Sankey bằng Plotly (Đã đóng ngoặc chuẩn xác)
fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = labels,
        color = line_color
    ),
    link = dict(
        source = sources,
        target = targets,
        value = values,
        color = link_color
    )
)])

fig.update_layout(title_text="<b>SƠ ĐỒ TRỰC QUAN DÒNG CHẢY CỦA TIỀN</b>", font_size=13, height=500)

# 4. Hiển thị khu vực nội dung chính
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ℹ️ Chi tiết trạng thái")
    if "Risk-On" in market_phase:
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:15px; border-radius:10px; border-left:5px solid {line_color}; color:#111;">
            <b>Hành vi dòng tiền Tấn công:</b><br/>
            - <b>Khối Doanh nghiệp:</b> Vay vốn mở rộng quy mô, tăng chi phí sản xuất, tuyển dụng nhân sự hàng loạt.<br/>
            - <b>Khối Cá nhân:</b> Rút tiết kiệm, dùng đòn bẩy tài chính cao (Margin) lao vào thị trường để tối đa hóa lợi nhuận.<br/>
            - <b>Điểm đến:</b> Chứng khoán tăng trưởng, Đất nền vùng ven, Bitcoin & Altcoins.
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:15px; border-radius:10px; border-left:5px solid {line_color}; color:#111;">
            <b>Hành vi dòng tiền Trú ẩn:</b><br/>
            - <b>Khối Định chế:</b> Hạ tỷ trọng cổ phiếu rủi ro cao, chốt lời hoặc cắt lỗ để cơ cấu sang tài sản an toàn.<br/>
            - <b>Chính phủ & Ngân hàng:</b> Tăng lãi suất để hút bớt tiền mặt lưu thông, siết tín dụng để hạ nhiệt lạm phát.<br/>
            - <b>Điểm đến:</b> Vàng miếng SJC, tích trữ đồng USD, gửi tiết kiệm ngân hàng, Trái phiếu Chính phủ.
            </div>
            """, unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("### 🗂️ Chi tiết các Nhóm Tài sản phân bổ")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("**Nhóm 1: Cổ phiếu & Sản xuất**\n- Mã công nghệ, bán lẻ, chứng khoán\n- Vốn lưu động mở rộng xưởng\n- Cổ phiếu Penny mạo hiểm")
with t2:
    st.success("**Nhóm 2: Tài sản trú ẩn cứng**\n- Vàng miếng SJC, Vàng nhẫn 9999\n- Quỹ ETF Vàng thế giới\n- Đồng đô la Mỹ (USD)")
with t3:
    st.warning("**Nhóm 3: Thu nhập cố định & Phòng thủ**\n- Trái phiếu Chính phủ dài hạn\n- Gửi tiết kiệm ngân hàng\n- Cổ phiếu Thiết yếu (Điện, Nước)")
