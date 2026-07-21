import streamlit as st
import plotly.graph_objects as go

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Bản Đồ Thành Phố Chi Tiết")

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

st.title("🗺️ Bản Đồ Tương Tác Đường Sá & Địa Danh")
st.write("Hãy dùng cuộn chuột để phóng to (Zoom in) xem chi tiết tên quốc gia, các tỉnh thành, địa điểm công cộng và mạng lưới đường sá.")

# Thiết lập biểu đồ bản đồ dạng Mapbox nền tối trực quan
fig = go.Figure()

# Thêm một lớp điểm mờ ẩn để định vị điểm nhìn ban đầu tại Việt Nam
fig.add_trace(go.Scattermapbox(
    lat=[21.0285],
    lon=[105.8542],
    mode='markers',
    marker=dict(size=0, opacity=0), # Ẩn hoàn toàn điểm chấm để giữ bản đồ sạch sẽ
    hoverinfo='none'
))

# Cấu hình phong cách bản đồ có tên địa danh và đường giao thông chi tiết
fig.update_layout(
    mapbox=dict(
        # Sử dụng máy chủ dữ liệu CartoDB Dark Matter chứa nhãn đường sá đầy đủ không cần mã token
        style="https://cartocdn.com",
        center=dict(lat=16.0471, lon=108.2068), # Đặt trung tâm nhìn ban đầu tại Việt Nam
        zoom=4.8 # Mức độ thu phóng vừa phải để nhìn bao quát lúc đầu
    ),
    paper_bgcolor='#1e1e24', # Đồng bộ màu nền rìa bản đồ thành màu xám tối
    plot_bgcolor='#1e1e24',
    margin=dict(l=0, r=0, t=0, b=0), # Triệt tiêu lề thừa, giúp bản đồ tràn viền sắc nét
    height=800
)

# Render đồ họa map lên giao diện Streamlit
st.plotly_chart(fig, use_container_width=True)
