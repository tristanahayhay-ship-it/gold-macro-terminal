import streamlit as st
import plotly.graph_objects as go

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Quả Cầu Trái Đất Chi Tiết")

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

st.title("🌌 Quả Cầu Trái Đất 3D Đầy Đủ Đường Sá & Địa Danh")
st.write("Hãy cuộn chuột phóng to (Zoom in) sát vào bất kỳ đâu để xem chi tiết tên đường phố và địa điểm.")

# Khởi tạo biểu đồ đồ họa Mapbox
fig = go.Figure()

# Thêm một lớp điểm mờ ẩn để giữ bản đồ sạch sẽ hoàn toàn không có hột tròn
fig.add_trace(go.Scattermapbox(
    lat=[16.0471],
    lon=[108.2068],
    mode='markers',
    marker=dict(size=0, opacity=0), 
    hoverinfo='none'
))

# Cấu hình hiển thị bản đồ nền xám tối đầy đủ nhãn đường sá toàn cầu
fig.update_layout(
    mapbox=dict(
        # Nguồn dữ liệu bản đồ tối tích hợp đầy đủ tên quốc gia, thành phố, đường sá
        style="https://cartocdn.com",
        center=dict(lat=16.0471, lon=108.2068), # Đặt tâm nhìn ban đầu tại Việt Nam
        zoom=4.5 # Mức độ thu phóng ban đầu vừa vặn tầm mắt
    ),
    paper_bgcolor='#1e1e24', # Đồng bộ màu nền bao quanh thành màu xám tối của bạn
    plot_bgcolor='#1e1e24',
    margin=dict(l=0, r=0, t=0, b=0), # Triệt tiêu lề thừa giúp bản đồ tràn viền sắc nét
    height=800
)

# Render đồ họa map lên giao diện Streamlit
st.plotly_chart(fig, use_container_width=True)
