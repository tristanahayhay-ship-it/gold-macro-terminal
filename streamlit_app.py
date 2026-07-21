import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG STREAMLIT ---
st.set_page_config(layout="wide", page_title="Gold Macro Terminal", page_icon="🌐")

# --- KHỞI TẠO DỮ LIỆU GIẢ LẬP KINH TẾ 195 QUỐC GIA (LOGIC THỰC TẾ) ---
@st.cache_data
def load_macro_data():
    # Danh sách các quốc gia đại diện tiêu biểu cho các nhóm kinh tế chính toàn cầu
    countries = [
        {"iso": "USA", "name": "Hoa Kỳ", "type": "Core", "gdp": 27000, "gold": 8133},
        {"iso": "CHN", "name": "Trung Quốc", "type": "Emerging", "gdp": 18000, "gold": 2250},
        {"iso": "DEU", "name": "Đức", "type": "Developed", "gdp": 4500, "gold": 3350},
        {"iso": "JPN", "name": "Nhật Bản", "type": "Developed", "gdp": 4200, "gold": 846},
        {"iso": "IND", "name": "Ấn Độ", "type": "Emerging", "gdp": 3700, "gold": 800},
        {"iso": "GBR", "name": "Anh Quốc", "type": "Developed", "gdp": 3300, "gold": 310},
        {"iso": "FRA", "name": "Pháp", "type": "Developed", "gdp": 3000, "gold": 2436},
        {"iso": "RUS", "name": "Nga", "type": "Resource", "gdp": 2000, "gold": 2330},
        {"iso": "VNM", "name": "Việt Nam", "type": "Emerging", "gdp": 430, "gold": 10},
        {"iso": "AUS", "name": "Úc", "type": "Resource", "gdp": 1700, "gold": 80},
        {"iso": "SAU", "name": "Ả Rập Xê Út", "type": "Resource", "gdp": 1100, "gold": 323},
        {"iso": "BRA", "name": "Brazil", "type": "Emerging", "gdp": 2100, "gold": 130},
        {"iso": "SGP", "name": "Singapore", "type": "Developed", "gdp": 500, "gold": 230},
        {"iso": "CHE", "name": "Thụy Sĩ", "type": "Developed", "gdp": 800, "gold": 1040},
    ]
    # Tọa độ địa lý trung tâm phục vụ vẽ dòng chảy (Dây liên kết vĩ mô)
    coords = {
        "USA": [37.0902, -95.7129], "CHN": [35.8617, 104.1954], "DEU": [51.1657, 10.4515],
        "JPN": [36.2048, 138.2529], "IND": [20.5937, 78.9629], "GBR": [55.3781, -3.4360],
        "FRA": [46.2276, 2.2137], "RUS": [61.5240, 105.3188], "VNM": [14.0583, 108.2772],
        "AUS": [-25.2744, 133.7751], "SAU": [23.8859, 45.0792], "BRA": [-14.2350, -51.9253],
        "SGP": [1.3521, 103.8198], "CHE": [46.8182, 8.2275]
    }
    df = pd.DataFrame(countries)
    df['lat'] = df['iso'].map(lambda x: coords.get(x, [0,0])[0])
    df['lon'] = df['iso'].map(lambda x: coords.get(x, [0,0])[1])
    return df

df_macro = load_macro_data()

# --- GIAO DIỆN DIỀU KHIỂN CHÍNH ---
st.title("🌐 GOLD MACRO TERMINAL - HỆ THỐNG DÒNG CHẢY KINH TẾ TOÀN CẦU")
st.subheader("Bản đồ Động lực học Tiền tệ & Tài sản Trú ẩn theo Biến động của USD")

# Khung điều hướng trạng thái USD toàn cầu
usd_status = st.radio(
    "CHỌN TRẠNG THÁI CHỈ SỐ USD (DXY):",
    ("USD MẠNH LÊN (Thắt chặt định lượng / Tăng lãi suất)", "USD YẾU ĐI (Nới lỏng định lượng / Bơm tiền)"),
    horizontal=True
)
is_usd_strong = "MẠNH" in usd_status

# --- GIẢI THÍCH BẢN CHẤT LOGIC DÒNG TIỀN THEO TIÊU CHÍ ---
st.markdown("### 📊 Tóm Tắt Bản Chất Dòng Chảy Tiền Tệ Hệ Thống")
if is_usd_strong:
    st.error("🚨 **KHI USD MẠNH LÊN:** Tiền chảy ngược từ 195 nước về trung tâm **Hoa Kỳ (Trái phiếu Chính phủ Mỹ / Tiền mặt)**. Doanh nghiệp và quốc gia thiếu thanh khoản USD rơi vào thế phòng thủ, co hẹp sản xuất. Tài sản rủi ro (Chứng khoán, Crypto, Bất động sản vĩ mô) và Hàng hóa bị bán tháo để giữ USD.")
else:
    st.success("💰 **KHI USD YẾU ĐI:** Tiền từ Hoa Kỳ bung tỏa chảy mạnh ra **toàn cầu**, đổ vào các nước đang phát triển (Emerging Markets) tìm kiếm lợi nhuận cao. Khi lạm phát USD tăng mạnh, dòng tiền lớn dịch chuyển trú ẩn vào **VÀNG (Gold)**, Hàng hóa chiến lược và các tài sản vật chất cứng.")

# --- PHÂN TÁCH GIAO DIỆN: VĨ MÔ (BẢN ĐỒ) & VI MÔ (HỆ THỐNG MẠNG LƯỚI NỘI BỘ) ---
tab1, tab2 = st.tabs(["🌍 CẤP TOÀN CẦU & LIÊN QUỐC GIA (Macro View)", "🔎 CHI TIẾT NỘI BỘ QUỐC GIA (Micro View - Zoom In)"])

with tab1:
    st.markdown("#### Bản đồ Tương quan 195 Quốc gia & Dòng chảy Hệ thống về Mỹ")
    
    # Định hình màu sắc quốc gia dựa trên trạng thái dòng tiền
    if is_usd_strong:
        df_macro['Sức mạnh kinh tế'] = df_macro['type'].map({"Core": 100, "Developed": 70, "Emerging": 30, "Resource": 40})
        line_color = "red"  # Dòng tiền co rút về Mỹ hiển thị cảnh báo đỏ
        node_text = "Dòng tiền Co rút quay về Mỹ"
    else:
        df_macro['Sức mạnh kinh tế'] = df_macro['type'].map({"Core": 50, "Developed": 75, "Emerging": 95, "Resource": 85})
        line_color = "green"  # Dòng tiền bung tỏa đi đầu tư hiển thị màu xanh
        node_text = "Dòng tiền Đổ ra Thế giới & Trú ẩn Vàng"

    # Khởi tạo sơ đồ bản đồ
    fig_map = go.Figure()

    # 1. Vẽ nền màu sắc 195 nước thể hiện sức mạnh/phân bổ
    fig_map.add_trace(go.Choropleth(
        locations=df_macro['iso'],
        z=df_macro['Sức mạnh kinh tế'],
        colorscale="Viridis" if not is_usd_strong else "YlOrRd",
        showscale=False,
        hoverinfo="none"
    ))

    # 2. Vẽ các điểm nút Quốc gia hiển thị trữ lượng Vàng thực tế
    fig_map.add_trace(go.Scattergeo(
        lon=df_macro['lon'],
        lat=df_macro['lat'],
        text=df_macro['name'] + "<br>Trữ lượng vàng: " + df_macro['gold'].astype(str) + " Tấn",
        mode='markers+text',
        marker=dict(
            size=np.log(df_macro['gold'] + 10) * 3,
            color='gold',
            line=dict(width=1, color='black')
        ),
        name="Quốc gia / Trữ lượng Vàng"
    ))

    # 3. Vẽ Sợi dây liên kết thể hiện dòng chảy tiền tệ vĩ mô kết nối toàn cầu đến Mỹ (USA)
    usa_lat, usa_lon = 37.0902, -95.7129
    for idx, row in df_macro.iterrows():
        if row['iso'] != 'USA':
            fig_map.add_trace(go.Scattergeo(
                lon=[row['lon'], usa_lon],
                lat=[row['lat'], usa_lat],
                mode='lines',
                line=dict(width=2, color=line_color),
                opacity=0.6,
                hoverinfo='none',
                showlegend=False
            ))

    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600
    )
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.markdown("#### Cơ cấu Vi mô: Từ Chính phủ Trung ương ➡️ Tập đoàn ➡️ Doanh nghiệp ➡️ Nhà đầu tư cá nhân")
    selected_country = st.selectbox("Chọn quốc gia bạn muốn kiểm tra bộ máy vi mô nội bộ:", df_macro['name'].unique())
    
    st.write(f"Đang phân tích mạng lưới luân chuyển tiền tệ của: **{selected_country}**")

    # Xây dựng tọa độ sơ đồ mạng lưới nút liên kết nội bộ theo thứ tự phân cấp
    # Trục Y thể hiện các cấp độ cấu trúc thực tế từ trên xuống dưới
    nodes = {
        "Chính phủ / Ngân hàng Trung ương": [0.5, 0.9],
        "Các Tập đoàn Đa quốc gia": [0.2, 0.6],
        "Hệ thống Ngân hàng Thương mại": [0.8, 0.6],
        "Doanh nghiệp Sản xuất / SME": [0.2, 0.3],
        "Thị trường Tài sản nội địa (BĐS, CK)": [0.5, 0.3],
        "Nhà đầu tư cá nhân nhỏ lẻ": [0.5, 0.05]
    }

    # Định nghĩa dòng tiền chảy vào loại tài sản nào ở cấp độ vi mô
    flow_color = "red" if is_usd_strong else "green"
    
    fig_micro = go.Figure()

    # Vẽ các dây mạng lưới liên kết dòng tiền giữa các cấp bậc
    edges = [
        ("Chính phủ / Ngân hàng Trung ương", "Các Tập đoàn Đa quốc gia"),
        ("Chính phủ / Ngân hàng Trung ương", "Hệ thống Ngân hàng Thương mại"),
        ("Hệ thống Ngân hàng Thương mại", "Doanh nghiệp Sản xuất / SME"),
        ("Hệ thống Ngân hàng Thương mại", "Thị trường Tài sản nội địa (BĐS, CK)"),
        ("Các Tập đoàn Đa quốc gia", "Thị trường Tài sản nội địa (BĐS, CK)"),
        ("Doanh nghiệp Sản xuất / SME", "Nhà đầu tư cá nhân nhỏ lẻ"),
        ("Thị trường Tài sản nội địa (BĐS, CK)", "Nhà đầu tư cá nhân nhỏ lẻ"),
    ]

    for edge in edges:
        p1, p2 = nodes[edge[0]], nodes[edge[1]]
        fig_micro.add_trace(go.Scatter(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]],
            mode='lines+markers',
            line=dict(color=flow_color, width=3),
            opacity=0.7,
            showlegend=False
        ))

    # Vẽ các nút đại diện cho từng cấp bộ máy
    x_nodes = [v[0] for v in nodes.values()]
    y_nodes = [v[1] for v in nodes.values()]
    labels = list(nodes.keys())

    fig_micro.add_trace(go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        text=labels,
        textposition="top center",
        marker=dict(size=24, color='darkblue', symbol='square'),
        name="Cấp độ tổ chức"
    ))

    fig_micro.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=40, r=40, t=40, b=40),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_micro, use_container_width=True)

    # Hiển thị bảng phân bổ danh mục tài sản chi tiết cho Nhà đầu tư theo tiêu chí
    st.markdown("### Đâu là nơi trú ẩn an toàn cho tài sản?")
    
    if is_usd_strong:
        st.warning("⚠️ **DANH MỤC PHÒNG THỦ (USD MẠNH):** Nhà đầu tư thu hẹp sản xuất kinh doanh vĩ mô, rút tiền khỏi tài sản rủi ro để đưa vào:")
        st.code("1. Tiền mặt USD (Gửi tiết kiệm lãi suất cao)\n2. Trái phiếu Chính phủ ngắn hạn\n3. Tránh nợ vay (Tập đoàn giảm đòn bẩy)")
    else:
        st.success("🚀 **DANH MỤC TẤN CÔNG & TRÚ ẨN LẠM PHÁT (USD YẾU):** Dòng tiền từ các định chế lớn bung xõa mạnh vào các kênh:")
        st.code("1. VÀNG VẬT CHẤT (Tài sản tối hậu khi tiền giấy mất giá)\n2. Cổ phiếu tăng trưởng / Bất động sản phân khúc lõi\n3. Thị trường hàng hóa (Commodities: Dầu thô, Đồng)")
