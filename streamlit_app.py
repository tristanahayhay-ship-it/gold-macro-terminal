import streamlit as st
import pydeck as pdk

# Cấu hình giao diện rộng toàn màn hình
st.set_page_config(layout="wide", page_title="Quả Cầu 3D Chi Tiết Đường Sá")

# Ép giao diện tối toàn diện cho nền trang web màu xám
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
st.write("Cấu trúc quả cầu 3D xoay tự do trên nền xám. Hãy cuộn chuột phóng to sát vào Việt Nam để xem chi tiết đường phố.")

# 1. Cấu hình góc nhìn ban đầu thành quả địa cầu 3D (Globe) tâm nhìn tại Việt Nam
view_state = pdk.ViewState(
    latitude=16.0471,
    longitude=108.2068,
    zoom=2.5,  # Góc nhìn bao quát ban đầu từ không gian
    pitch=0,
    bearing=0
)

# 2. Render quả cầu 3D tích hợp cơ sở dữ liệu đường phố chi tiết
r = pdk.Deck(
    layers=[], # Giữ sạch bề mặt bản đồ, không thêm hột tròn rối mắt
    initial_view_state=view_state,
    # Ép kiểu hiển thị phẳng thông thường thành Quả Cầu 3D Trái Đất (GLOBE)
    views=[pdk.View(type="GlobeView", controller=True)],
    # Sử dụng bản đồ nền xám đen chứa toàn bộ tên đường sá, địa danh chi tiết toàn cầu
    map_style="https://cartocdn.com",
    paper_bgcolor='#1e1e24' # Đồng bộ viền xung quanh màu xám
)

st.pydeck_chart(r)
