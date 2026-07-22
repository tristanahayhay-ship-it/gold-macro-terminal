# streamlit_app.py
import streamlit as st
import data_loader as dl
import charts as cr
import pandas as pd

st.set_page_config(page_title="Hệ Thống Dòng Tiền Mapbox Toàn Cầu", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ BẢN ĐỒ KINH TẾ SỐ ĐA NGÀNH TOÀN CẦU (GOOGLE MAPS STYLE)")
st.caption("Hệ thống đồng bộ toàn thế giới. Kéo thanh trượt Zoom để phóng sát camera nhìn thấy cấu trúc vi mô đa ngành tại chỗ.")

# 1. TRUNG TÂM ĐIỀU KHIỂN TRÊN TRANG CHÍNH
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    usd_mode = st.segmented_control(
        "🕹️ Chọn Trạng thái Đồng Đô la Mỹ (USD):",
        options=["USD MẠNH LÊN (Màu Đỏ) 📈", "USD YẾU ĐI (Màu Xanh) 📉"],
        default="USD MẠNH LÊN (Màu Đỏ) 📈"
    )
    is_usd_strong = "MẠNH" in usd_mode
    line_color = "#FF4B4B" if is_usd_strong else "#00D46A"

df_global = dl.load_economic_database()
name_list = df_global['NAME'].tolist()

with col_ctrl2:
    default_index = name_list.index("Việt Nam") if "Việt Nam" in name_list else 0
    target_country = st.selectbox("🔍 Chọn quốc gia mục tiêu ống kính:", name_list, index=default_index)

with col_ctrl3:
    zoom_slider = st.slider(
        "🔍 Tiêu cự Camera (Google Maps Zoom Level):", 
        min_value=1.0, max_value=6.5, value=1.2, step=0.1,
        help="Nấc 1.0-3.4: Tầng Khí Quyển vĩ mô. Nấc 3.5-4.5: Tầng Mặt Đất Đa Ngành. Nấc 4.6-6.5: Tầng Sinh Vật Nhà Đầu Tư."
    )

if zoom_slider >= 4.6:
    st.success(f"🦠 TẦNG SINH VẬT: Đang phóng sát vào đường phố hiển thị túi tiền Nhà đầu tư cá nhân và chuỗi Doanh nghiệp tại {target_country}.")
elif zoom_slider >= 3.5:
    st.warning(f"⛰️ TẦNG MẶT ĐẤT: Đang hiển thị ranh giới địa lý các Tập đoàn công nghiệp, công nghệ lớn của {target_country}.")
elif zoom_slider >= 2.1:
    st.info(f"☁️ TẦNG MÂY: Khởi động bừng sáng cổng kết nối ngoại hối USD và Ngân hàng Trung ương.")
else:
    st.info("🌌 TẦNG KHÍ QUYỂN VĨ MÔ: Bản đồ bao quát 195 quốc gia kết nối mạch máu dòng chảy liên quốc gia về Mỹ.")

# 2. RENDERING BẢN ĐỒ SỐ HỢP NHẤT
fig = cr.draw_unified_mapbox_engine(df_global, target_country, zoom_slider, line_color)
st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# MA TRẬN BẢN CHẤT KINH TẾ ĐỒNG BỘ CHẶT CHẼ
# =============================================================================
st.markdown("---")
st.markdown("### 🧱 MA TRẬN BẢN CHẤT KINH TẾ VÀ ĐIỂM TRÚ ẨN CỦA CÁC LOẠI TÀI SẢN CHI TIẾT XUYÊN SUỐT CÁC CẤP")

if is_usd_strong:
    st.error("🚨 HỆ THỐNG CO CỤM PHÒNG THỦ TOÀN DIỆN (KHI USD MẠNH / LỰC HÚT VỐN VỀ MỸ)")
    matrix_data = {
        "Phân Cấp Bộ Máy Đa Ngành": ["Cấp 1: Toàn Cầu (195 Nước)", "Cấp 2: Ngân Hàng Trung Ương", "Cấp 3: Tập Đoàn Đa Ngành Lớn", "Cấp 4: Doanh Nghiệp Sản Xuất (SME)", "Cấp 5: Người Dân & Nhà Đầu Tư"],
        "Bản Chất Dòng Tiền Đi Đâu?": [
            "Thanh khoản bị hút cạn từ 195 nước, dòng tiền tháo chạy dọc theo chuỗi mạch máu dây màu ĐỎ hướng ngược về tâm dịch tài sản Hoa Kỳ.",
            "Dòng vốn ngoại tệ USD chảy mạnh ra khỏi kho dự trữ quốc gia. NHTW buộc phải bán USD can thiệp bảo vệ tỷ giá hoặc nâng lãi suất nội tệ lên cao.",
            "Dòng vốn tín dụng mạo hiểm quốc tế bị đóng van. Tập đoàn lớn thu hẹp kế hoạch mở rộng quy mô, dừng các dự án thâu tóm M&A.",
            "Dòng vốn lưu động trong chuỗi cung ứng bị thắt nghẹt do sức mua thị trường sụt giảm mạnh và chi phí nhập khẩu máy móc tính bằng USD tăng cao.",
            "Dòng tiền nhàn rỗi hoảng loạn tháo chạy hoàn toàn khỏi các kênh đầu cơ rủi ro cao (chứng khoán, bất động sản vùng ven) để đưa về thế thủ."
        ],
        "Tiêu Vào Đâu & Đầu Tư Vào Tài Sản Gì?": [
            "**Đầu tư vào**: Trái phiếu Chính phủ Mỹ ngắn hạn, các tài khoản thanh toán tiền mặt định danh USD để hưởng lợi suất đỉnh cao.",
            "**Tiêu vào**: Nghiệp vụ thị trường mở, bù đắp cán cân thanh toán quốc gia bị thiếu hụt do dòng vốn ngoại tháo lui.",
            "**Đầu tư vào**: Tất toán trước hạn toàn bộ các khoản vay nợ trái phiếu bằng ngoại tệ USD (Deleveraging) để chặn đứng rủi ro lỗ tỷ giá.",
            "**Tiêu vào**: Duy trì chi phí vận hành bộ máy tối thiểu, gửi tiền mặt dự phòng vào tài khoản tiết kiệm của hệ thống ngân hàng nhà nước.",
            "**Đầu tư vào**: Nắm giữ tiền mặt phòng thủ tối đa, gửi tiết kiệm dài hạn hưởng mức lãi suất cao kỷ lục, mua bảo hiểm an toàn."
        ]
    }
else:
    st.success("🚀 HỆ THỐNG BUNG XÕA TẤN CÔNG & TRÚ ẨN LẠM PHÁT (KHI USD YẾU / TIỀN RẺ TRÀN RA THẾ GIỚI)")
    matrix_data = {
        "Phân Cấp Bộ Máy Đa Ngành": ["Cấp 1: Toàn Cầu (195 Nước)", "Cấp 2: Ngân Hàng Trung Ương", "Cấp 3: Tập Đoàn Đa Quốc Gia", "Cấp 4: Doanh Nghiệp Sản Xuất (SME)", "Cấp 5: Người Dân & Nhà Đầu Tư"],
        "Bản Chất Dòng Tiền Đi Đâu?": [
            "Dòng tiền rẻ từ Mỹ tràn ra khắp mạng lưới 195 nước (Chuỗi mạch máu dây màu XANH) đi săn tìm tỷ suất sinh lời cao tại các nước mới nổi.",
            "Áp lực tỷ giá hạ nhiệt, kho dự trữ ngoại hối an toàn. NHTW lập tức hạ lãi suất cơ bản, bơm thanh khoản dồi dào kích thích tăng trưởng nội địa.",
            "Nguồn vốn vay giá rẻ dồi dào giải tỏa áp lực tài chính. Các tập đoàn đa ngành bung tiền mở rộng các dự án hạ tầng lớn.",
            "Dòng tiền luân chuyển mượt mà thông suốt trong chuỗi cung ứng nhờ chi phí sử dụng vốn cực thấp và sức mua tiêu dùng phục hồi mạnh mẽ.",
            "Dòng vốn trong dân tăng vọt do lãi suất gửi tiết kiệm quá thấp, kích hoạt tâm lý lo sợ tiền giấy bốc hơi giá trị do áp lực lạm phát vĩ mô."
        ],
        "Tiêu Vào Đâu & Đầu Tư Vào Tài Sản Gì?": [
            "**Đầu tư vào**: Thị trường hàng hóa vĩ mô (Dầu thô, Đồng), đặc biệt dòng tiền chảy mạnh về các nước có hầm dự trữ **VÀNG VẬT CHẤT** lớn.",
            "**Tiêu vào**: Gom mua tích trữ thêm ngoại tệ USD giá rẻ vào kho dự trữ chiến lược, đẩy mạnh giải ngân vốn đầu tư công phát triển quốc gia.",
            "**Đầu tư vào**: Thâu tóm dự án chiến lược (M&A), xây dựng chuỗi nhà máy đa quốc gia, mở rộng chuỗi cung ứng ngành lõi.",
            "**Tiêu vào**: Gia tăng nhập khẩu nguyên vật liệu thiết bị giá rẻ, tối đa hóa công suất, gia tăng hàng tồn kho để chiếm lĩnh thị phần toàn diện.",
            "**Đầu tư vào**: **VÀNG VẬT CHẤT** (tấm khiên bảo chứng tài sản tối hậu), **Cổ phiếu tăng trưởng** công nghệ, và **Bất động sản phân khúc lõi** trung tâm."
        ]
    }

st.table(pd.DataFrame(matrix_data))
