import streamlit as st
import plotly.graph_objects as go

# 1. Cấu hình giao diện Streamlit ép nền đen tuyệt đối (Ultra Dark Mode)
st.set_page_config(layout="wide", page_title="Cyber Global Map Terminal")

st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    iframe { background-color: #000000 !important; }
    header, footer, [data-testid="stSidebar"] { display: none !important; }
    div.block-container { padding: 0rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

fig = go.Figure()

# 2. Tạo lớp bản đồ phẳng 2D đồ họa sống động màu Cyberpunk/Neon (Hỗ trợ cuộn chuột Zoom phóng to tự do)
fig.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='#000000', 
    geo=dict(
        showland=True,
        landcolor='#05131a',       # Đất liền màu xanh Teal thẫm bóng đêm cực sang
        showlakes=False,
        showcountries=True,
        countrycolor='#006688',    # Đường biên giới các nước phát sáng màu xanh biển
        showocean=True,
        oceancolor='#000000',      # Đại dương màu đen huyền bí làm nổi bật lục địa
        projection_type='equirectangular', # Bản đồ PHẲNG ĐỨNG chính diện 2D, không nghiêng vẹo
        showframe=False,
        coastlinecolor='#00aaff',  # Đường bờ biển phát sáng dải màu xanh Neon rõ nét
        coastlinewidth=1.2,
        center=dict(lon=10.0, lat=25.0), # Đặt trung tâm camera cân bằng thế giới
        lonaxis=dict(range=[-140, 160]),
        lataxis=dict(range=[-10, 65])
    )
)

# 3. Hiển thị duy nhất màn hình bản đồ tương tác (Hỗ trợ kéo thả và cuộn chuột Zoom tự do)
st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': False})
