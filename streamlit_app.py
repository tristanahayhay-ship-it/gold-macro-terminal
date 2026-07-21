import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# 1. Cấu hình giao diện Streamlit Darkmode đồng bộ nền đen hoàn toàn
st.set_page_config(layout="wide", page_title="Macro Money Network Matrix")

st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, p, span, div, label { color: #ffffff !important; }
    div[data-baseweb="select"] { background-color: #111111 !important; color: #ffffff !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 Hệ Thống Ma Trận Dòng Chảy Tiền Tệ & Tài Sản Toàn Cầu")
st.caption("Mô phỏng mạng lưới kinh tế phân cấp: Kết nối Xuyên lục địa (Mỹ - Trung Quốc) và mạng lưới 4 cấp chi tiết bên trong nội địa.")

# 2. Tạo kiến trúc Đồ thị phân tầng bằng NetworkX
G = nx.DiGraph()

# Định nghĩa danh sách các nút và tọa độ phẳng cố định để khi phóng to không bao giờ bị lệch vị trí
# Tọa độ cấu trúc theo dạng: Cụm Mỹ ở trục X âm (-), Cụm Trung Quốc ở trục X dương (+)
nodes_data = {
    # ==================== CỤM ĐIỂM A: MỸ (USA CLUSTER) ====================
    "US_SuperNode": {"label": "🇺🇸 ĐẦU NÃO VĨ MÔ MỸ", "x": -5, "y": 0, "type": "country_hub", "color": "#1f77b4", "size": 40},
    # Sơ đồ nội địa Mỹ (Cấp Xã -> Huyện -> Tỉnh)
    "US_Commune_Xa": {"label": "Hộ dân & Trang trại (Xã tại Mỹ)", "x": -7, "y": -2, "type": "local", "color": "#00d2ff", "size": 18},
    "US_District_Huyen": {"label": "Cụm Công nghiệp (Huyện tại Mỹ)", "x": -6, "y": -1, "type": "local", "color": "#00d2ff", "size": 22},
    "US_Province_Tinh": {"label": "Thị trường Đô thị (Tỉnh tại Mỹ)", "x": -6, "y": 1, "type": "local", "color": "#00d2ff", "size": 26},
    "US_Federal_Central": {"label": "Cục Dự trữ Liên bang (FED)", "x": -5, "y": 2, "type": "local", "color": "#ffaa00", "size": 30},

    # ==================== CỤM ĐIỂM B: TRUNG QUỐC (CHINA CLUSTER) ====================
    "CN_SuperNode": {"label": "🇨🇳 ĐẦU NÃO VĨ MÔ TRUNG QUỐC", "x": 5, "y": 0, "type": "country_hub", "color": "#de2110", "size": 40},
    # Sơ đồ nội địa Trung Quốc (Cấp Xã -> Huyện -> Tỉnh)
    "CN_Commune_Xa": {"label": "Hộ nông dân & Tiểu thương (Xã tại TQ)", "x": 7, "y": -2, "type": "local", "color": "#e74c3c", "size": 18},
    "CN_District_Huyen": {"label": "Công xưởng sản xuất (Huyện tại TQ)", "x": 6, "y": -1, "type": "local", "color": "#e74c3c", "size": 22},
    "CN_Province_Tinh": {"label": "Đặc khu kinh tế (Tỉnh tại TQ)", "x": 6, "y": 1, "type": "local", "color": "#e74c3c", "size": 26},
    "CN_PBOC_Central": {"label": "Ngân hàng Trung ương (PBOC)", "x": 5, "y": 2, "type": "local", "color": "#ffaa00", "size": 30}
}

for node, attrs in nodes_data.items():
    G.add_node(node, **attrs)

# 3. Định nghĩa các sợi dây liên kết dòng tiền (Edges)
# Trạng thái màu sắc: strong_in (Xanh lá), strong_out (Đỏ), neutral (Vàng)
edges_data = [
    # ================= SỢI DÂY KẾT NỐI KINH TẾ VĨ MÔ XUYÊN QUỐC GIA (MỸ <-> TRUNG QUỐC) =================
    ("US_SuperNode", "CN_SuperNode", {"status": "strong_out", "color": "#ff0000", "desc": "Mỹ rút dòng vốn đầu tư / Tăng thuế nhập khẩu thắt chặt thương mại với TQ"}),
    ("CN_SuperNode", "US_SuperNode", {"status": "strong_in", "color": "#00ff00", "desc": "Trung Quốc đẩy mạnh xuất khẩu hàng hóa công nghiệp thu Đô-la Mỹ"}),
    ("CN_PBOC_Central", "US_Federal_Central", {"status": "neutral", "color": "#ffff00", "desc": "PBOC luân chuyển dòng ngoại hối mua Trái phiếu Chính phủ Mỹ"}),

    # ================= SỢI DÂY NỘI ĐỊA BÊN TRONG NƯỚC MỸ (ĐIỂM A) =================
    ("US_Commune_Xa", "US_District_Huyen", {"status": "neutral", "color": "#ffff00", "desc": "Lao động nông thôn Mỹ chuyển dịch về các cụm công nghiệp huyện"}),
    ("US_District_Huyen", "US_Province_Tinh", {"status": "strong_in", "color": "#00ff00", "desc": "Hàng hóa từ huyện gom lên phân phối tại đô thị lớn cấp Tỉnh"}),
    ("US_Province_Tinh", "US_SuperNode", {"status": "strong_in", "color": "#00ff00", "desc": "Dòng thặng dư tài chính đổ về các sàn giao dịch Wall Street vĩ mô"}),
    ("US_Federal_Central", "US_SuperNode", {"status": "strong_out", "color": "#ff0000", "desc": "FED tăng lãi suất điều hành, thắt chặt dòng tiền rút khỏi thị trường"}),

    # ================= SỢI DÂY NỘI ĐỊA BÊN TRONG TRUNG QUỐC (ĐIỂM B) =================
    ("CN_Commune_Xa", "CN_District_Huyen", {"status": "strong_in", "color": "#00ff00", "desc": "Tiền lương từ khu công nghiệp Huyện gửi về kinh tế hộ gia đình ở Xã"}),
    ("CN_District_Huyen", "CN_Province_Tinh", {"status": "strong_in", "color": "#00ff00", "desc": "Nhà máy công xưởng Huyện xuất xưởng hàng hóa ra Đặc khu Tỉnh"}),
    ("CN_Province_Tinh", "CN_SuperNode", {"status": "strong_in", "color": "#00ff00", "desc": "Tỉnh kết chuyển thặng dư sản xuất về đầu não kinh tế quốc gia Bắc Kinh"}),
    ("CN_PBOC_Central", "CN_Province_Tinh", {"status": "neutral", "color": "#ffff00", "desc": "PBOC điều tiết cung tiền kích thích tăng trưởng bất động sản các Tỉnh"})
]

for u, v, attrs in edges_data:
    G.add_edge(u, v, **attrs)

# 4. Tạo bộ lọc hiển thị thông minh trên Sidebar để giả lập cơ chế Zoom hệ thống
st.sidebar.header("🎛️ BỘ ĐIỀU KHIỂN MA TRẬN KINH TẾ")
view_mode = st.sidebar.radio(
    "Chọn chế độ quan sát hệ thống:",
    ["1. Toàn cảnh vĩ mô (Mỹ ↔ Trung Quốc)", "2. Phóng to Điểm A (Xem sơ đồ nội địa Mỹ)", "3. Phóng to Điểm B (Xem sơ đồ nội địa Trung Quốc)", "4. Gộp tổng thể toàn mạng lưới"]
)

# 5. Xử lý logic lọc nút và sợi dây theo chế độ hiển thị được chọn
visible_nodes = []
visible_edges = []

if view_mode == "1. Toàn cảnh vĩ mô (Mỹ ↔ Trung Quốc)":
    # Chỉ hiển thị 2 siêu nút và các sợi dây xuyên biên giới kết nối 2 nước
    visible_nodes = ["US_SuperNode", "CN_SuperNode"]
    visible_edges = [e for e in edges_data if (e[0] == "US_SuperNode" and e[1] == "CN_SuperNode") or (e[0] == "CN_SuperNode" and e[1] == "US_SuperNode")]
    axis_range_x = [-8, 8]
    axis_range_y = [-4, 4]

elif view_mode == "2. Phóng to Điểm A (Xem sơ đồ nội địa Mỹ)":
    # Ẩn Trung Quốc, hiển thị toàn bộ sơ đồ 4 cấp chi tiết bên trong Mỹ
    visible_nodes = [n for n in nodes_data if "US_" in n]
    visible_edges = [e for e in edges_data if "US_" in e[0] and "US_" in e[1]]
    axis_range_x = [-8.5, -3.5]
    axis_range_y = [-3, 3]

elif view_mode == "3. Phóng to Điểm B (Xem sơ đồ nội địa Trung Quốc)":
    # Ẩn Mỹ, hiển thị toàn bộ sơ đồ 4 cấp chi tiết bên trong Trung Quốc
    visible_nodes = [n for n in nodes_data if "CN_" in n]
    visible_edges = [e for e in edges_data if "CN_" in e[0] and "CN_" in e[1]]
    axis_range_x = [3.5, 8.5]
    axis_range_y = [-3, 3]

else: # Gộp tổng thể toàn mạng lưới
    visible_nodes = list(nodes_data.keys())
    visible_edges = edges_data
    axis_range_x = [-9, 9]
    axis_range_y = [-4, 4]

# 6. DỰNG ĐỒ HỌA MẠNG LƯỚI TƯƠNG TÁC BẰNG PLOTLY GO
edge_traces = []

# Vẽ các sợi dây liên kết đổi màu theo đúng quy ước trạng thái dữ liệu của bạn
for edge in visible_edges:
    u, v, attrs = edge[0], edge[1], edge[2]
    x0, y0 = nodes_data[u]["x"], nodes_data[u]["y"]
    x1, y1 = nodes_data[v]["x"], nodes_data[v]["y"]
    
    # Tạo đường dây vẽ riêng biệt kèm mũi tên hướng dòng chảy bóng mờ
    edge_trace = go.Scatter(
        x=[x0, x1, None], y=[y0, y1, None],
        line=dict(width=3, color=attrs["color"]),
        hoverinfo='text',
        text=[f"Dòng chảy: {attrs['desc']}"],
        mode='lines'
    )
    edge_traces.append(edge_trace)

# Vẽ các điểm nút (Thực thể hệ thống kinh tế)
node_x = []
node_y = []
node_text = []
node_colors = []
node_sizes = []

for node in visible_nodes:
    node_x.append(nodes_data[node]["x"])
    node_y.append(nodes_data[node]["y"])
    node_text.append(nodes_data[node]["label"])
    node_colors.append(nodes_data[node]["color"])
    node_sizes.append(nodes_data[node]["size"])

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    text=node_text,
    textposition="top center",
    marker=dict(
        size=node_sizes,
        color=node_colors,
        line=dict(width=2, color='#ffffff')
    )
)

# 7. Thiết lập giao diện màn hình trung tâm điều khiển (Dark UI Layout)
layout = go.Layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=10),
    paper_bgcolor='#000000', # Nền đen sâu tuyệt đối
    plot_bgcolor='#000000',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=axis_range_x),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=axis_range_y),
    clickmode='event+select'
)

# 8. Gom tất cả thành phần đồ họa mạng lưới và hiển thị lên web Streamlit
fig = go.Figure(data=edge_traces + [node_trace], layout=layout)

# Cấu hình tính năng zoom tương tác kéo chuột tự do của Plotly
st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
