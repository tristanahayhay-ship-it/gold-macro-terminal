import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ==============================================================================
# 1. CẤU HÌNH GIAO DIỆN TERMINAL TẤM PHẲNG (TILE DASHBOARD DESIGN)
# ==============================================================================
st.set_page_config(
    page_title="Global Tile Map Terminal",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp { background-color: #eef2f5; color: #1e272e; }
    .terminal-card { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #dcdde1; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .status-badge { font-weight: bold; padding: 6px 12px; border-radius: 4px; font-size: 16px; color: white; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

st.title("🎛️ GLOBAL FINANCIAL TILE TERMINAL (GRID STYLE)")
st.subheader("Mạng lưới Tấm: Hệ thống ma trận ô vuông cố định (Khóa dịch chuyển tuyệt đối)")
st.markdown("---")

# ==============================================================================
# 2. SIDEBAR ĐIỀU KHIỂN DÒNG VỐN
# ==============================================================================
st.sidebar.header("🎛️ TỔNG TÀI KHOẢN VĨ MÔ")
market_phase = st.sidebar.selectbox(
    "Chọn Trạng thái Chỉ số Dòng tiền:",
    ["Đồng USD giảm - Tổng lực ĐẦU TƯ TOÀN CẦU CHẰNG CHỊT (MÀU XANH OUT)", 
     "Đồng USD tăng - Bán tháo rút dòng về Mỹ TRÚ ẨN (MÀU ĐỎ IN)"]
)

selected_agent = st.sidebar.radio(
    "Tiêu điểm Khối Thực thể chạy dây:",
    ["Tất cả chủ thể (Cá nhân & Tập đoàn)", "Chỉ hiện Nhà đầu tư Cá nhân (Retail)", "Chỉ hiện Khối Tập đoàn lớn (Corporate)"]
)

total_capital = st.sidebar.number_input("Tổng quy mô dòng vốn hệ thống vận chuyển (USD):", min_value=1000000, value=500000000, format="%d")

# Thiết lập tham số màu sắc tương phản theo trạng thái thị trường
if "MÀU XANH" in market_phase:
    flow_type, pulse_color, base_color, line_style, badge_bg, status_label = "INVESTMENT", "#00b894", "rgba(0, 184, 148, 0.2)", "solid", "#00b894", "XUNG LỰC ĐẦU TƯ TOÀN CẦU (RISK-ON)"
else:
    flow_type, pulse_color, base_color, line_style, badge_bg, status_label = "SAFE_HAVEN", "#d63031", "rgba(214, 48, 49, 0.2)", "dash", "#d63031", "KHỦNG HOẢNG THÁO CHẠY VỀ TRÚ ẨN (RISK-OFF)"

# ==============================================================================
# 3. TỌA ĐỘ MA TRẬN LƯỚI TẤM (X, Y) THAY THẾ CHO (LAT, LON) Địa Lý
# ==============================================================================
# Thiết lập hệ lưới phẳng 2D giả lập vị trí địa lý tương đối trên một tấm bảng điều khiển
us_tile = {"name": "Mỹ (Fed HQ)", "x": 1, "y": 3}

macro_tiles = {
    "Việt Nam": {"x": 7, "y": 1, "name_as": "Sàn HOSE / Đất nền vùng ven", "intensity": 95, "color_weight": "#fdcb6e"},
    "Trung Quốc": {"x": 6, "y": 3, "name_as": "Sàn Thâm Quyến / Thượng Hải", "intensity": 80, "color_weight": "#fdcb6e"},
    "Nhật Bản": {"x": 8, "y": 3, "name_as": "Sàn Nikkei / Yên JPY", "intensity": 75, "color_weight": "#e17055"},
    "Đức": {"x": 4, "y": 4, "name_as": "Thị trường Frankfurt", "intensity": 70, "color_weight": "#d63031"},
    "Anh": {"x": 3, "y": 4, "name_as": "Sàn LSE / Bảng Anh", "intensity": 65, "color_weight": "#d63031"},
    "Singapore": {"x": 7, "y": 2, "name_as": "Trung tâm Tài chính ĐNA", "intensity": 85, "color_weight": "#fdcb6e"},
    "Thụy Sĩ": {"x": 4, "y": 3, "name_as": "Vàng & Franc Thụy Sĩ", "intensity": 90, "color_weight": "#e17055"}
}

# ==============================================================================
# 4. ENGINE DỰNG BẢN ĐỒ TẤM KHÔNG GIAN PHẲNG TRÊN ĐỒ THỊ XY
# ==============================================================================
fig = go.Figure()

# 4.1. Vẽ Tấm gốc trung tâm: Nước Mỹ (Điểm neo Dòng tiền)
fig.add_trace(go.Scatter(
    x=[us_tile["x"]], y=[us_tile["y"]],
    mode="markers+text",
    marker=dict(size=45, color="#2c3e50", symbol="square", line=dict(color="#ffffff", width=2)),
    text="<b>🇺🇸 US</b>", textposition="center", textfont=dict(color="white", size=12),
    hoverinfo="text", hovertext=f"🏢 Trung tâm Thanh khoản vĩ mô<br>{us_tile['name']}"
))

# 4.2. Vẽ các Tấm Quốc gia Vệ tinh & Đường truyền tải luồng tín hiệu hình học
for country, data in macro_tiles.items():
    # Tính toán hệ số phân bổ dòng vốn động
    intensity_factor = 1.0
    if "Retail" in selected_agent:
        intensity_factor = 0.6 if country != "Việt Nam" else 1.2
    elif "Corporate" in selected_agent:
        intensity_factor = 1.3 if country != "Việt Nam" else 0.5
    
    current_intensity = data["intensity"] * intensity_factor
    allocated_fund = (total_capital * (current_intensity / 500))
    
    # Chuỗi thông tin tương tác trực quan
    tile_hover = f"🗺️ Quốc gia: {country}<br>🎯 Hạ tầng tài sản: {data['name_as']}<br>💰 Vốn phân bổ: {allocated_fund:,.0f} USD"
    
    # Vẽ đường truyền dẫn tín hiệu kết nối thẳng giữa các khối tấm hình học
    line_x = [us_tile["x"], data["x"]] if flow_type == "INVESTMENT" else [data["x"], us_tile["x"]]
    line_y = [us_tile["y"], data["y"]] if flow_type == "INVESTMENT" else [data["y"], us_tile["y"]]
    
    # Vẽ nét bóng nền đường truyền
    fig.add_trace(go.Scatter(x=line_x, y=line_y, mode="lines", line=dict(width=2, color=base_color), hoverinfo="none"))
    # Vẽ nét viền nhịp xung lực
    fig.add_trace(go.Scatter(x=line_x, y=line_y, mode="lines", line=dict(width=3, color=pulse_color, dash=line_style), hoverinfo="none"))
    
    # Vẽ Khối tấm vuông đại diện cho từng quốc gia (Theo màu sắc Đỏ - Cam - Vàng của ảnh mẫu)
    fig.add_trace(go.Scatter(
        x=[data["x"]], y=[data["y"]],
        mode="markers+text",
        marker=dict(size=40, color=data["color_weight"], symbol="square", line=dict(color="#ffffff", width=1.5)),
        text=f"<b>{country[:2].upper()}</b>", textposition="center", textfont=dict(color="#1e272e", size=11),
        hoverinfo="text", hovertext=tile_hover
    ))

# 4.3. Cấu hình khóa cứng toàn bộ trục tọa độ phẳng (Đã vá lỗi nạp dải biên độ rỗng)
fig.update_layout(
    showlegend=False,
    height=600,
    margin=dict(l=40, r=40, t=20, b=40),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f5f6fa", # Nền bảng lưới tấm phẳng sạch sẽ sáng sủa
    xaxis=dict(
        range=[0, 10], showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False,
        showticklabels=False, fixedrange=True
    ),
    yaxis=dict(
        range=[0, 6], showgrid=True, gridcolor="rgba(0,0,0,0.05)", zeroline=False,
        showticklabels=False, fixedrange=True
    )
)

# ==============================================================================
# 5. HIỂN THỊ BẢN ĐỒ TẤM LÊN TRÊN CÙNG MÀN HÌNH
# ==============================================================================
st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 6. KHU VỰC THÔNG TIN TERMINAL PHÍA DƯỚI
# ==============================================================================
col_text, col_stats = st.columns(2)

with col_text:
    st.markdown("### 🎚️ Trung tâm Phân tích Luồng Tín hiệu Tấm")
    st.markdown(f"Trạng thái ma trận: <span class='status-badge' style='background-color: {badge_bg};'>{status_label}</span>", unsafe_allow_html=True)
    st.markdown("<div class='terminal-card'>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Cơ chế tương tác lưới ma trận:")
    st.write("• **Khóa chuyển động hoàn hảo:** Bản đồ tấm đã cố định vị trí các quốc gia trên một lưới tọa độ 2D phẳng, loại bỏ hoàn toàn các lỗi lệch hướng hoặc lỗi đè màu của bản đồ địa lý cũ.")
    if flow_type == "INVESTMENT":
        st.write("🟢 **TÍN HIỆU PHÁT XẠ (Outflow):** Chuỗi liên kết hiển thị nét liền Xanh Lá, biểu thị dòng thanh khoản phát đi từ Tấm Nguồn Mỹ nạp đầy năng lượng cho các Khối Tấm Đỏ - Vàng.")
    else:
        st.write("🔴 **TÍN HIỆU HẤP THỤ (Inflow):** Chuỗi nét đứt Đỏ rực nhấp nháy, mô phỏng hành vi rút năng lượng phân bổ từ các Tấm Vệ tinh cuộn ngược tâm về Tấm Trú ẩn Mỹ.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_stats:
    st.markdown("### 🗜️ Tóm tắt Ma trận Điều phối Vốn liên quốc gia (Top 5 Trục lớn)")
    matrix_rows = []
    top_countries = ["Việt Nam", "Trung Quốc", "Thụy Sĩ", "Nhật Bản", "Đức"]
    
    for country in top_countries:
        intensity_factor = 1.0
        if "Retail" in selected_agent:
            intensity_factor = 0.6 if country != "Việt Nam" else 1.2
        elif "Corporate" in selected_agent:
            intensity_factor = 1.3 if country != "Việt Nam" else 0.5
            
        current_intensity = macro_tiles[country]["intensity"] * intensity_factor
        allocated_val = (total_capital * (current_intensity / 500))
        
        matrix_rows.append({
            "Trục kết nối ma trận": f"Mỹ ➔ {country}" if flow_type == "INVESTMENT" else f"{country} ➔ Mỹ",
            "Tín hiệu luồng tấm": "🟢 PHÁT XẠ ĐẦU TƯ" if flow_type == "INVESTMENT" else "🔴 RÚT VỀ TẤM NGUỒN",
            "Hạ tầng tiếp nhận tiêu biểu": macro_tiles[country]["name_as"],
            "Dòng vốn ước tính (USD)": f"${allocated_val:,.0f} USD"
        })
        
    df_matrix = pd.DataFrame(matrix_rows)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
