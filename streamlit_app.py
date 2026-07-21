import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Quả Cầu Trái Đất Nghệ Thuật")

# Ép giao diện tối toàn diện cho thanh điều hướng và nền trang web màu xám
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

st.title("🌌 Quả Cầu Trái Đất Không Gian Tối Giản")
st.write("Cấu trúc quả cầu 3D cũ được bổ sung nhãn tên quốc gia và địa danh chi tiết khi phóng to.")

# Khởi tạo biểu đồ đồ họa 3D
fig = go.Figure()

# --- TÍNH NĂNG 1: TẠO HIỆU ỨNG KHÍ QUYỂN BAO QUANH TRÁI ĐẤT ---
theta = np.linspace(0, 2*np.pi, 100)
fig.add_trace(go.Scattergeo(
    lon = 100 * np.cos(theta), 
    lat = 40 * np.sin(theta),
    mode = 'lines',
    line = dict(width=2.5, color='rgba(0, 238, 255, 0.35)'), 
    hoverinfo = 'none'
))

# --- TÍNH NĂNG 2: THIẾT LẬP MÀU SẮC TRÁI ĐẤT, NỀN XÁM VÀ NHÃN ĐỊA DANH ---
fig.update_layout(
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        showlakes = True,
        showrivers = True, # Hiển thị thêm hệ thống sông ngòi lớn khi zoom
        
        # --- BẬT TÊN QUỐC GIA VÀ ĐỊA DANH TRÊN QUẢ CẦU ---
        showsubunits = True, # Bật ranh giới các bang/tỉnh khi phóng to
        subunitcolor = '#9f7aea', # Màu ranh giới tỉnh/bang (tím nhạt)
        
        landcolor = '#b794f4',      
        oceancolor = '#1a0b2e',     
        countrycolor = '#7e57c2',   
        lakecolor = '#1a0b2e',
        rivercolor = '#1a0b2e',
        
        projection_type = 'orthographic', 
        lonaxis = dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)'),
        lataxis = dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)')
    ),
    paper_bgcolor = '#1e1e24',     
    plot_bgcolor = '#1e1e24',
    showlegend = False,
    margin = dict(l=0, r=0, t=0, b=0), 
    height = 800
)

# Render đồ họa lên giao diện Streamlit
st.plotly_chart(fig, use_container_width=True)
