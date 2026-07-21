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
st.sidebar.markdown("### 📊 Chỉ báo Vĩ mô Hiện tại")
if "Risk-On" in market_phase:
    st.sidebar.success("• Lãi suất: Thấp (Nới lỏng)")
    st.sidebar.success("• Lạm phát: Vừa phải (Tốt)")
    st.sidebar.success("• Địa chính trị: Ổn định")
    st.sidebar.success("• Tâm lý: Tham lam (FOMO)")
    bg_color = "#E8F8F5"
    line_color = "#1ABC9C"
else:
    st.sidebar.error("• Lãi suất: Cao (Thắt chặt)")
    st.sidebar.error("• Lạm phát: Phi mã / Thiểu phát")
    st.sidebar.error("• Địa chính trị: Căng thẳng")
    st.sidebar.error("• Tâm lý: Sơ hãi (FUD)")
    bg_color = "#FDEDEC"
    line_color = "#E74C3C"

# 3. Định nghĩa dữ liệu Sơ đồ Sankey (Dòng chảy tiền)
# Gán nhãn cho các nút (Nodes) trong sơ đồ
labels = [
    "HỆ THỐNG VĨ MÔ",                   # 0
    "Kinh tế Tăng trưởng (Risk-On)",     # 1
    "Kinh tế Suy thoái (Risk-Off)",      # 2
    "Khối Doanh nghiệp",                # 3
    "Khối Cá nhân",                     # 4
    "Khối Định chế Tài chính",           # 5
    "Chính phủ & Ngân hàng TW",          # 6
    "Cổ phiếu Tăng trưởng & Đầu cơ",     # 7
    "Bất động sản Đầu cơ / Vùng ven",    # 8
    "Thị trường Crypto (Tài sản mới)",   # 9
    "Vàng vật chất & Vàng tài khoản",    # 10
    "Tiền mặt & Đồng tiền mạnh (USD)",   # 11
    "Trái phiếu CP & Ngành phòng thủ"    # 12
]

# Khởi tạo danh mục dòng chảy (nguồn -> đích -> khối lượng)
sources = []
targets = []
values = []

if "Risk-On" in market_phase:
    # Tuyến đường của dòng tiền Tăng trưởng
    sources += [0, 1, 1, 3, 3, 4, 4]
    targets += [1, 3, 4, 7, 8, 8, 9]
    values  += [100, 50, 50, 30, 20, 25, 25] # Tỷ trọng mô phỏng
else:
    # Tuyến đường của dòng tiền Phòng thủ
    sources += [0, 2, 2, 5, 5, 6, 6]
    targets += [2, 5, 6, 10, 11, 11, 12]
    values  += [100, 60, 40, 35, 25, 15, 25]

# Tạo biểu đồ Sankey bằng Plotly
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
      color = line_color + "44" # Thêm alpha channel để làm mờ đường nối
  ))])

fig.update_layout(title_text="<b>SƠ ĐỒ TRỰC QUAN DÒNG CHẢY CỦA TIỀN</b>", font_size=13, height=500)

# 4. Hiển thị khu vực nội dung chính
col1, col2 = st.columns([2, 1])

with col1:
    # Render biểu đồ dòng tiền lên ứng dụng
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"### ℹ️ Chi tiết trạng thái")
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

# Bảng thông tin tra cứu nhanh danh mục tài sản dưới chân trang
st.markdown("### 🗂️ Chi tiết các Nhóm Tài sản phân bổ")
t1, t2, t3 = st.columns(3)
with t1:
    st.info("**Nhóm 1: Cổ phiếu & Sản xuất**\n- Mã công nghệ, bán lẻ, chứng khoán\n- Vốn lưu động mở rộng xưởng\n- Cổ phiếu Penny mạo hiểm")
with t2:
    st.success("**Nhóm 2: Tài sản trú ẩn cứng**\n- Vàng miếng SJC, Vàng nhẫn 9999\n- Quỹ ETF Vàng thế giới\n- Đồng đô la Mỹ (USD)")
with t3:
    st.warning("**Nhóm 3: Thu nhập cố định & Phòng thủ**\n- Trái phiếu Chính phủ dài hạn\n- Gửi tiết kiệm ngân hàng\n- Cổ phiếu Thiết yếu (Điện, Nước)")
