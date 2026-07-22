# streamlit_app.py
import streamlit as st
import data_loader as dl
import charts as cr

st.set_page_config(page_title="Hệ Thống Dòng Tiền Mapbox Toàn Cầu", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ BẢN ĐỒ KINH TẾ SỐ ĐA NGÀNH TOÀN CẦU (GOOGLE MAPS STYLE)")
st.caption("Hệ thống đồng bộ hơn 195 quốc gia. Kéo thanh trượt Zoom để phóng sát camera nhìn thấy cấu trúc vi mô đa ngành tại chỗ.")

# 1. TRUNG TÂM ĐIỀU KHIỂN TRỰC TIẾP TRÊN TRANG CHÍNH
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns()

with col_ctrl1:
    usd_mode = st.segmented_control(
        "🕹️ Trạng thái chỉ số USD (DXY):",
        options=["USD MẠNH LÊN (Màu Đỏ) 📈", "USD YẾU ĐI (Màu Xanh) 📉"],
        default="USD MẠNH LÊN (Màu Đỏ) 📈"
    )
    is_usd_strong = "MẠNH" in usd_mode
    line_color = "#FF4B4B" if is_usd_strong else "#00D46A"

# Tải cơ sở dữ liệu vĩ mô bao phủ toàn cầu
df_global = dl.load_economic_database()
name_list = df_global['NAME'].tolist()

with col_ctrl2:
    # SỬA LỖI VALUEERROR: Sử dụng cơ chế tìm kiếm index an toàn chống sập ứng dụng
    default_index = name_list.index("Việt Nam") if "Việt Nam" in name_list else 0
    target_country = st.selectbox("🔍 Chọn quốc gia mục tiêu điều hướng:", name_list, index=default_index)

with col_ctrl3:
    zoom_slider = st.slider("🔍 Độ cao Camera (Google Maps Zoom):", min_value=1.0, max_value=6.0, value=1.2, step=0.2,
                            help="Zoom từ 1.0 -> 3.0: Nhìn luồng vốn vĩ mô 195 nước. Zoom từ 3.5 -> 6.0: Thấy rõ địa điểm kinh tế vi mô trong nước.")

# Kích hoạt trạng thái thông báo động dựa trên độ cao ống kính camera
if zoom_slider >= 3.5:
    st.success(f"🔬 KÍNH HIỂN VI ĐÃ KÍCH HOẠT: Đang nhìn cận cảnh cấu trúc vi mô đa ngành rải rác ngay trên nền địa lý đất nước {target_country.upper()}")
else:
    st.info("🌍 CHẾ ĐỘ TOÀN CẦU: Bản đồ đang bao quát mạng lưới luồng vốn liên quốc gia của hơn 195 nước đổ về Mỹ.")

# 2. DỰNG BẢN ĐỒ SỐ ĐỒNG BỘ 100% THEO ĐỘ THU PHÓNG TẠI CHỖ
fig = cr.draw_real_google_maps_engine(df_global, target_country, zoom_slider, line_color)
st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# MA TRẬN BẢN CHẤT LOGIC KINH TẾ ĐỒNG BỘ THEO TIÊU CHÍ ĐỊA ĐIỂM
# =============================================================================
st.markdown("---")
st.markdown("### 🧱 MA TRẬN ĐIỂM ĐẾN DÒNG TIỀN VÀ BẢN CHẤT CỦA CÁC LOẠI TÀI SẢN CHI TIẾT")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### 🌍 Luồng Vốn Quốc Tế (Vĩ mô toàn cầu)")
    if is_usd_strong:
        st.error("❌ **USD MẠNH:** Lực hút thanh khoản kéo dòng tiền xuyên quốc gia dọc theo các sợi dây màu **ĐỎ** rút ròng về tài sản neo giữ tại Mỹ. Các nước sở tại bị ép thắt chặt tiền tệ.")
    else:
        st.success("✅ **USD YẾU:** Tiền rẻ bung xõa qua chuỗi mạch máu màu **XANH** tràn vào các nước có nền tảng sản xuất tốt và đổ mạnh vào **VÀNG VẬT CHẤT** tại các hầm dự trữ quốc gia.")

with col_right:
    st.markdown(f"#### 🎯 Hoạt Động Đa Ngành Vi Mô Tại: {target_country}")
    if is_usd_strong:
        st.warning("🛡 Honor tài sản phòng thủ: Các Tập đoàn đa ngành dừng giải ngân, gom tiền mặt gửi vào NHTW. Quỹ đầu tư rủi ro bán tháo cổ phiếu tăng trưởng về tiền mặt phòng thủ.")
    else:
        st.info("🚀 Thúc đẩy tài sản tấn công: Chi phí dòng vốn rẻ kích hoạt các Tập đoàn thâu tóm quỹ đất xây Bất động sản phân khúc lõi. Người dân rút tiền tiết kiệm mua Vàng vật chất trú ẩn lạm phát.")
