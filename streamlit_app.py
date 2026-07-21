import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Hệ Thống Kinh Tế Toàn Quốc")

# Ép giao diện tối toàn diện cho nền trang web màu xám đồng bộ với app của bạn
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e24;
    }
    h1, p, span, div, label {
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #b794f4 !important;
        font-size: 16px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #00eeff !important;
        border-bottom-color: #00eeff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🇻🇳 Hệ Thống Đồ Họa Kinh Tế Tích Hợp Toàn Quốc Việt Nam")
st.write("Mối liên hệ chặt chẽ từ vĩ mô Quốc gia đến các động lực phát triển Cấp Tỉnh và Cấp Xã.")

# Khởi tạo hệ thống Tab điều hướng liên kết tầng dữ liệu
tab_quoc_gia, tab_tinh, tab_xa = st.tabs(["🌐 1. Cấp Quốc Gia (Tổng GDP)", "🏢 2. Cấp Tỉnh (GRDP Địa Phương)", "🏡 3. Cấp Xã (Cơ Cấu Ngành)"])

# ==============================================================================
# TAB 1: CẤP QUỐC GIA (SƠ ĐỒ HƯỚNG TÂM ĐA TẦNG - SUNBURST)
# ==============================================================================
with tab_quoc_gia:
    st.subheader("Cơ Cấu Tổng Sản Phẩm Quốc Nội Việt Nam (GDP)")
    st.write("Bấm vào các phân khúc vòng tròn để phóng to, phân rã sâu vào các khối ngành chiến lược.")
    
    labels_qg = [
        "TỔNG GDP VIỆT NAM",
        "Khu vực III: Dịch Vụ", "Khu vực II: Công Nghiệp & Xây Dựng", "Khu vực I: Nông, Lâm & Thủy Sản", "Thuế Sản Phẩm Trừ Trợ Cấp",
        "Tài chính, Ngân hàng & Bảo hiểm", "Thương mại & Bán lẻ", "Du lịch & Lưu trú", "CNTT & Viễn thông",
        "Công nghiệp Chế biến, Chế tạo", "Sản xuất & Phân phối năng lượng", "Xây dựng hạ tầng quốc gia",
        "Nông nghiệp công nghệ cao", "Thủy hải sản xuất khẩu",
        "Khối Doanh nghiệp FDI", "Khối Tư nhân trong nước"
    ]
    parents_qg = [
        "",
        "TỔNG GDP VIỆT NAM", "TỔNG GDP VIỆT NAM", "TỔNG GDP VIỆT NAM", "TỔNG GDP VIỆT NAM",
        "Khu vực III: Dịch Vụ", "Khu vực III: Dịch Vụ", "Khu vực III: Dịch Vụ", "Khu vực III: Dịch Vụ",
        "Khu vực II: Công Nghiệp & Xây Dựng", "Khu vực II: Công Nghiệp & Xây Dựng", "Khu vực II: Công Nghiệp & Xây Dựng",
        "Khu vực I: Nông, Lâm & Thủy Sản", "Khu vực I: Nông, Lâm & Thủy Sản",
        "Công nghiệp Chế biến, Chế tạo", "Công nghiệp Chế biến, Chế tạo"
    ]
    values_qg = [430, 185, 160, 50, 35, 60, 55, 40, 30, 80, 40, 40, 30, 20, 50, 30]

    fig_qg = go.Figure(go.Sunburst(
        labels = labels_qg, parents = parents_qg, values = values_qg,
        branchvalues = "total", textinfo = "label+value+percent entry",
        marker = dict(colorscale = 'Thermal', line = dict(width = 1.5, color = '#1e1e24')),
        hovertemplate = '<b>%{label}</b><br>Quy mô: %{value} Tỷ USD<br>Tỷ trọng: %{percentEntry:.2%}<extra></extra>'
    ))
    fig_qg.update_layout(paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', font=dict(color="#ffffff"), margin=dict(l=10, r=10, t=20, b=10), height=600)
    st.plotly_chart(fig_qg, use_container_width=True)

# ==============================================================================
# TAB 2: CẤP TỈNH (SƠ ĐỒ KHỐI PHÂN CẤP TỶ TRỌNG - TREEMAP)
# ==============================================================================
with tab_tinh:
    st.subheader("Tổng Sản Phẩm Trên Địa Bàn Cấp Tỉnh (GRDP)")
    st.write("Mô phỏng cấu trúc kinh tế của một tỉnh/thành phố động lực đóng góp vào ngân sách Trung ương.")
    
    labels_tinh = [
        "GRDP ĐỊA PHƯƠNG",
        "Công Nghiệp & Xây Dựng Tỉnh", "Dịch Vụ & Thương Mại Tỉnh", "Nông, Lâm & Thủy Sản Tỉnh", "Thuế Sản Phẩm Địa Phương",
        "Khu Công Nghiệp & Chế Xuất", "Sản xuất năng lượng tái tạo", "Xây dựng khu đô thị",
        "Du lịch lữ hành & Lưu trú", "Dịch vụ Vận tải, Logistics", "Hệ thống Bán lẻ & Siêu thị",
        "Trồng trọt đặc sản xuất khẩu", "Nuôi trồng thủy sản công nghiệp"
    ]
    parents_tinh = [
        "",
        "GRDP ĐỊA PHƯƠNG", "GRDP ĐỊA PHƯƠNG", "GRDP ĐỊA PHƯƠNG", "GRDP ĐỊA PHƯƠNG",
        "Công Nghiệp & Xây Dựng Tỉnh", "Công Nghiệp & Xây Dựng Tỉnh", "Công Nghiệp & Xây Dựng Tỉnh",
        "Dịch Vụ & Thương Mại Tỉnh", "Dịch Vụ & Thương Mại Tỉnh", "Dịch Vụ & Thương Mại Tỉnh",
        "Nông, Lâm & Thủy Sản Tỉnh", "Nông, Lâm & Thủy Sản Tỉnh"
    ]
    values_tinh = [10000, 4500, 3800, 1100, 600, 2500, 1000, 1000, 1500, 1300, 1000, 600, 500]

    fig_tinh = go.Figure(go.Treemap(
        labels = labels_tinh, parents = parents_tinh, values = values_tinh,
        textinfo = "label+value+percent parent",
        marker = dict(colorscale = 'Electric', line = dict(width = 1.5, color = '#1e1e24')),
        hovertemplate = '<b>%{label}</b><br>Giá trị: %{value} Tỷ Đồng<br>Tỷ trọng nhóm: %{percentParent:.2%}<extra></extra>'
    ))
    fig_tinh.update_layout(paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', font=dict(color="#ffffff"), margin=dict(l=10, r=10, t=20, b=10), height=600)
    st.plotly_chart(fig_tinh, use_container_width=True)

# ==============================================================================
# TAB 3: CẤP XÃ (SƠ ĐỒ DÒNG CHẢY KINH TẾ TẾ BÀO - SANKEY DIAGRAM)
# ==============================================================================
with tab_xa:
    st.subheader("Dòng Chảy Kinh Tế Cơ Sở Cấp Xã")
    st.write("Mô hình phân rã chi tiết đến từng ngành nghề sinh kế thực tế của người dân vùng nông thôn/đô thị.")
    
    nodes_xa = [
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
    source_xa = 
    target_xa = 
    value_xa = 
    
    node_colors = ["#7e57c2", "#2d6a4f", "#e65100", "#0288d1", "#52b788", "#74c69d", "#f57c00", "#ffb74d", "#29b6f6", "#b3e5fc"]

    fig_xa = go.Figure(data=[go.Sankey(
        node = dict(pad = 20, thickness = 30, line = dict(color = "#ffffff", width = 0.5), label = nodes_xa, color = node_colors),
        link = dict(
            source = source_xa, target = target_xa, value = value_xa,
            color = [
                "rgba(45, 106, 79, 0.4)", "rgba(230, 81, 0, 0.4)", "rgba(2, 136, 209, 0.4)",
                "rgba(82, 183, 136, 0.3)", "rgba(116, 198, 157, 0.3)", "rgba(245, 124, 0, 0.3)",
                "rgba(255, 183, 77, 0.3)", "rgba(41, 182, 246, 0.3)", "rgba(179, 229, 252, 0.3)"
            ]
        )
    )])
    fig_xa.update_layout(paper_bgcolor='#1e1e24', plot_bgcolor='#1e1e24', font=dict(color="#ffffff"), margin=dict(l=20, r=20, t=20, b=20), height=600)
    st.plotly_chart(fig_xa, use_container_width=True)
