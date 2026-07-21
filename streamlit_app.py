import streamlit as st
import plotly.graph_objects as go

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Sơ Đồ Kinh Tế Cấp Xã")

# Ép giao diện tối toàn diện cho nền trang web màu xám đồng bộ với app của bạn
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e24;
    }
    h1, p, span, div {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Sơ Đồ Cấu Trúc & Dòng Chảy Kinh Tế Cấp Xã")
st.write("Mô phỏng trực quan cơ cấu các ngành kinh tế trọng điểm và các nguồn thu/chi ngân sách địa phương.")

# Tạo dữ liệu sơ đồ dòng chảy kinh tế (Sankey Diagram)
# Định nghĩa các nút (Nodes) trong sơ đồ kinh tế
nodes = [
    "Tổng Kinh Tế Xã",          # 0
    "Nông - Lâm - Thủy Sản",    # 1
    "Công Nghiệp - Xây Dựng",   # 2
    "Thương Mại - Dịch Vụ",     # 3
    "Trồng Trọt",               # 4
    "Chăn Nuôi",                # 5
    "Sản Xuất Tiểu Thủ Công",   # 6
    "Xây Dựng Dân Dụng",        # 7
    "Chợ Lẻ & Tạp Hóa",         # 8
    "Dịch Vụ Vận Tải/Mạng"      # 9
]

# Định nghĩa các luồng chảy giá trị (Nguồn -> Đích -> Giá trị mô phỏng)
source = [0, 0, 0, 1, 1, 2, 2, 3, 3]  # Vị trí nút bắt đầu
target = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Vị trí nút kết thúc
value =  [30, 45, 25, 18, 12, 25, 20, 15, 10] # Tỷ trọng giá trị tương ứng (%)

# Thiết lập màu sắc sắc nét hiển thị nổi bật trên nền xám tối
node_colors = [
    "#7e57c2", # Tổng kinh tế (Tím đậm)
    "#2d6a4f", # Nông nghiệp (Xanh lá)
    "#e65100", # Công nghiệp (Cam)
    "#0288d1", # Dịch vụ (Xanh dương)
    "#52b788", "#74c69d", # Chi tiết nông nghiệp
    "#f57c00", # Chi tiết công nghiệp
    "#ffb74d", # Chi tiết xây dựng
    "#29b6f6", "#b3e5fc"  # Chi tiết dịch vụ
]

# Tạo sơ đồ đồ họa tương tác cao cấp
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,
      thickness = 30,
      line = dict(color = "#ffffff", width = 0.5),
      label = nodes,
      color = node_colors
    ),
    link = dict(
      source = source,
      target = target,
      value = value,
      # Màu sắc luồng chảy có độ trong suốt (opacity) để nhìn nghệ thuật hơn
      color = [
          "rgba(45, 106, 79, 0.4)", "rgba(230, 81, 0, 0.4)", "rgba(2, 136, 209, 0.4)",
          "rgba(82, 183, 136, 0.3)", "rgba(116, 198, 157, 0.3)",
          "rgba(245, 124, 0, 0.3)", "rgba(255, 183, 77, 0.3)",
          "rgba(41, 182, 246, 0.3)", "rgba(179, 229, 252, 0.3)"
      ]
  )])

# Cấu hình phông nền xám tối đồng bộ theo thiết kế của bạn
fig.update_layout(
    title_text="Mô hình phân rã tỷ trọng ngân sách các ngành kinh tế xã",
    title_font=dict(size=16, color="#ffffff"),
    paper_bgcolor='#1e1e24',
    plot_bgcolor='#1e1e24',
    font=dict(size=12, color="#ffffff"), # Đổi toàn bộ chữ sơ đồ sang màu trắng
    margin=dict(l=20, r=20, t=50, b=20),
    height=600
)

# Render sơ đồ lên Streamlit
st.plotly_chart(fig, use_container_width=True)
