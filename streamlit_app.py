import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# 1. Cấu hình trang giao diện Web (Đặt ở đầu file)
st.set_page_config(
    page_title="Mô phỏng Dòng chảy Tiền tệ 3 Tầng",
    page_icon="📊",
    layout="wide"
)

# Tiêu đề chính ứng dụng
st.title("📊 Mô phỏng Dòng chảy Tiền tệ từ Vi mô đến Vĩ mô")
st.markdown("Ứng dụng hiển thị trực quan cách dòng tiền luân chuyển giữa các tầng kinh tế.")

# 2. Thanh bên (Sidebar) để cấu hình kịch bản nền kinh tế
st.sidebar.header("⚙️ Cấu hình kịch bản")
scenario = st.sidebar.selectbox(
    "Chọn trạng thái hệ thống:",
    options=["Bình thường", "Khi có BIẾN (Khủng hoảng)"]
)

# 3. Khởi tạo đồ thị NetworkX
G = nx.DiGraph()

# Khai báo các nút hệ thống
nodes = {
    "QUOC_TE": "🌐 QUỐC TẾ\n(FDI, FII, IMF)",
    "QUOC_GIA": "🏛️ QUỐC GIA\n(NHTW & Chính phủ)",
    "TINH_CHINH_QUYEN": "🏢 CẤP TỈNH\n(Chính quyền & Kho bạc)",
    "TINH_DOANH_NGHIEP": "🏭 DN LỚN / KCN\n(Sản xuất, Xuất khẩu)",
    "XA_CHINH_QUYEN": "🔰 CHÍNH QUYỀN XÃ\n(Ngân sách xã)",
    "XA_DAN_CU": "🏡 HỘ GIA ĐÌNH\n(Lao động, Tiêu dùng)"
}

for key, label in nodes.items():
    G.add_node(key, label=label)

# Cố định tọa độ phân tầng Y-axis từ Vĩ mô xuống Vi mô
pos = {
    "QUOC_TE":           (0, 4),
    "QUOC_GIA":          (0, 3),
    "TINH_CHINH_QUYEN":  (-2, 2),
    "TINH_DOANH_NGHIEP": (2, 2),
    "XA_CHINH_QUYEN":    (-2, 1),
    "XA_DAN_CU":         (2, 1)
}

# 4. Thiết lập luồng dữ liệu dòng tiền theo kịch bản người dùng chọn
edges = []
description_text = ""

if scenario == "Bình thường":
    description_text = """
    **Bản chất luân chuyển**: Dòng tiền vận hành thông suốt hai chiều. Tiền thuế/phí thu từ vi mô chuyển dần 
    lên trên để tái đầu tư vĩ mô. Thu nhập từ xuất khẩu và dòng vốn FDI chảy mạnh vào doanh nghiệp, sau đó 
    luân chuyển qua tiền lương để thúc đẩy tiêu dùng nội địa tại các hộ gia đình ở xã.
    """
    edges = [
        ("QUOC_TE", "TINH_DOANH_NGHIEP", "Bơm vốn đầu tư FDI", "NORMAL"),
        ("TINH_DOANH_NGHIEP", "QUOC_GIA", "Nộp Thuế xuất nhập khẩu", "NORMAL"),
        ("QUOC_GIA", "TINH_CHINH_QUYEN", "Phân bổ ngân sách tỉnh", "NORMAL"),
        ("TINH_CHINH_QUYEN", "XA_CHINH_QUYEN", "Hỗ trợ phát triển nông thôn", "NORMAL"),
        ("TINH_DOANH_NGHIEP", "XA_DAN_CU", "Trả lương công nhân & Thu mua", "NORMAL"),
        ("XA_DAN_CU", "TINH_DOANH_NGHIEP", "Tiêu dùng hàng hóa dịch vụ", "NORMAL"),
        ("XA_DAN_CU", "XA_CHINH_QUYEN", "Nộp phí, thuế địa phương", "NORMAL"),
        ("XA_CHINH_QUYEN", "TINH_CHINH_QUYEN", "Nộp nghĩa vụ ngân sách trên", "NORMAL")
    ]
else:
    description_text = """
    **Bản chất luân chuyển**: Kích hoạt cơ chế phòng thủ. Dòng tiền tháo chạy từ dưới lên trên và ra ngoài biên giới. 
    Các kênh đầu tư rủi ro (BĐS, dịch vụ phi thiết yếu) bị rút rỗng. Tiền mặt cô đọng trong két sắt hộ gia đình 
    hoặc chảy vào hệ thống an toàn cấp quốc gia (USD, Vàng, Trái phiếu chính phủ).
    """
    edges = [
        ("QUOC_GIA", "QUOC_TE", "💸 Vốn ngoại tháo chạy\n(Capital Flight)", "XA_RA"),
        ("QUOC_TE", "QUOC_GIA", "📊 Hỗ trợ tài chính vĩ mô", "DO_VAO"),
        ("TINH_DOANH_NGHIEP", "QUOC_GIA", "📊 Đổi lấy USD / Vàng\n(Trú ẩn an toàn)", "DO_VAO"),
        ("QUOC_GIA", "TINH_CHINH_QUYEN", "📊 Bơm vốn Đầu tư công vĩ mô", "DO_VAO"),
        ("TINH_DOANH_NGHIEP", "TINH_CHINH_QUYEN", "💸 Thất thu thuế DN\n(Đóng băng sản xuất)", "XA_RA"),
        ("TINH_CHINH_QUYEN", "XA_CHINH_QUYEN", "📊 Ngân sách cứu trợ khẩn cấp", "DO_VAO"),
        ("XA_DAN_CU", "QUOC_GIA", "📊 Gửi tiết kiệm Ngân hàng lớn\n/ Trú ẩn tài sản", "DO_VAO"),
        ("XA_DAN_CU", "TINH_DOANH_NGHIEP", "💸 Cắt giảm tối đa chi tiêu", "XA_RA")
    ]

# Áp dụng các cạnh (dòng tiền) vào đồ thị
for u, v, label, flow_type in edges:
    G.add_edge(u, v, label=label, type=flow_type)

# 5. Khởi tạo không gian vẽ Matplotlib
fig, ax = plt.subplots(figsize=(15, 10))

# Thiết lập màu sắc đồ thị dựa trên kịch bản
if scenario == "Bình thường":
    edge_colors = ['#1f77b4' for u, v in G.edges()] # Tất cả màu xanh dương ổn định
else:
    edge_colors = ['#2ca02c' if G[u][v]['type'] == 'DO_VAO' else '#d62728' for u, v in G.edges()] # Xanh lá (Đổ vào) / Đỏ (Xả ra)

# Tiến hành vẽ các khối chức năng (Nodes)
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=3800, node_color="#f8f9fa", edgecolors="#495057", linewidths=1.5)

# Đóng nhãn văn bản cho các khối
node_labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=10, font_weight="bold")

# Vẽ các mũi tên luân chuyển tiền tệ (Edges)
nx.draw_networkx_edges(G, pos, ax=ax, arrowstyle="->", arrowsize=22, edge_color=edge_colors, 
                       width=2.5, connectionstyle="arc3,rad=0.15")

# Đóng nhãn mô tả trên từng mũi tên
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_size=9, label_pos=0.5, rotate=False)

# Tối ưu hóa vùng hiển thị đồ thị
ax.axis('off')
plt.tight_layout()

# 6. Đưa dữ liệu hiển thị lên giao diện Web Streamlit
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📝 Phân tích kịch bản")
    st.info(description_text)
    
    st.subheader("💡 Chú giải ký hiệu")
    if scenario == "Bình thường":
        st.write("🔵 **Mũi tên Xanh dương**: Luồng vận hành kinh tế thông suốt hai chiều.")
    else:
        st.write("🟢 **Mũi tên Xanh lá (Đổ vào)**: Dòng tiền co cụm phòng thủ vào kênh an toàn.")
        st.write("🔴 **Mũi tên Đỏ (Xả ra)**: Khu vực bị tháo chạy vốn hoặc đóng băng thanh khoản.")

with col2:
    st.subheader("🗺️ Sơ đồ dòng chảy tiền tệ trực quan")
    st.pyplot(fig, clear_figure=True) # Render hình ảnh đồ thị động lên web
