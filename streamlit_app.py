import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Quả Cầu Trái Đất Nghệ Thuật")

# --- ÉP GIAO DIỆN TỐI TOÀN DIỆN CHO TRANG WEB ---
st.markdown(
    """
    <style>
    /* Đổi nền trang web sang màu xám tối */
    .stApp {
        background-color: #1e1e24;
    }
    /* Đổi màu chữ tiêu đề và văn bản sang màu trắng sáng */
    h1, p, span, div {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌌 Quả Cầu Trái Đất Không Gian Tối Giản")
st.write("Mô phỏng quả địa cầu tương tác 3D mượt mà trên giao diện nền tối.")

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

# --- TÍNH NĂNG 2: THIẾT LẬP MÀU SẮC TRÁI ĐẤT VÀ NỀN TRANG MÀU XÁM ---
fig.update_layout(
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = '#b794f4',      
        oceancolor = '#1a0b2e',     
        countrycolor = '#7e57c2',   
        lakecolor = '#1a0b2e',
        projection_type = 'orthographic', 
        lonaxis = dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)'),
        lataxis = dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)')
    ),
    paper_bgcolor = '#1e1e24',     # Màu xám tối cho nền biểu đồ
    plot_bgcolor = '#1e1e24',
    showlegend = False,
    margin = dict(l=0, r=0, t=0, b=0), 
    height = 800
)

# Render đồ họa lên giao diện Streamlit
st.plotly_chart(fig, use_container_width=True)
