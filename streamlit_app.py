# streamlit_app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CẤU HÌNH GIAO DIỆN KHÔNG GIAN SỐ HỌC VÔ CỰC
st.set_page_config(page_title="Vũ Trụ Mạch Máu Tiền Tệ Vô Cực", layout="wide")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 100%; padding-top: 1rem; }
    h1, h3 { text-align: center; color: #FFFFFF; }
    body { background-color: #050505; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ BẢN ĐỒ MA TRẬN MẠCH MÁU TIỀN TỆ ĐA NGÀNH TƯƠNG QUAN USD")
st.caption("Xóa bỏ hoàn toàn thế giới vật lý thô sơ. Hệ thống tự động sinh hàng ngàn đại lộ dòng chảy tiền tệ đan chéo dày đặc khi phóng to.")

# TRUNG TÂM ĐIỀU KHIỂN LUỒNG NĂNG LƯỢNG
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    usd_mode = st.segmented_control(
        "🕹️ Trạng thái Trọng Lực USD (DXY):",
        options=["USD MẠNH LÊN (Màu Đỏ) 📈", "USD YẾU ĐI (Màu Xanh) 📉"],
        default="USD MẠNH LÊN (Màu Đỏ) 📈"
    )
    is_usd_strong = "MẠNH" in usd_mode
    line_color = "#FF3333" if is_usd_strong else "#00FF66" # Đỏ rực thắt chặt / Xanh neon bung xõa

# 2. ĐỒNG BỘ 195 QUỐC GIA THỰC TẾ TRÊN HỆ TRỤC TỌA ĐỘ VŨ TRỤ (MỸ LÀM TÂM 0,0)
@st.cache_data
def load_infinite_financial_database():
    df_iso = px.data.gapminder().query("year == 2007")[['iso_alpha', 'country']].drop_duplicates()
    translate_dict = {
        'USA': 'Hoa Kỳ', 'VNM': 'Việt Nam', 'CHN': 'Trung Quốc', 'JPN': 'Nhật Bản', 
        'DEU': 'Đức', 'GBR': 'Anh Quốc', 'FRA': 'Pháp', 'IND': 'Ấn Độ', 
        'BRA': 'Brazil', 'AUS': 'Australia', 'CAN': 'Canada', 'RUS': 'Nga'
    }
    
    fixed_coords = {
        'USA': [0.0, 0.0], # Hoa Kỳ là tâm hố đen vũ trụ tiền tệ
        'VNM': [55.0, 30.0], 'CHN': [40.0, 35.0], 'JPN': [50.0, 45.0], 'DEU': [-35.0, 40.0], 
        'GBR': [-45.0, 50.0], 'FRA': [-38.0, 35.0], 'IND': [30.0, 15.0], 'BRA': [-45.0, -40.0], 
        'AUS': [65.0, -50.0], 'CAN': [-25.0, -55.0], 'RUS': [20.0, 60.0]
    }
    
    countries_factory = []
    for _, row in df_iso.iterrows():
        code = row['iso_alpha']
        vietnamese_name = translate_dict.get(code, row['country'])
        
        if code in fixed_coords:
            x, y = fixed_coords[code]
        else:
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(35, 90)
            x, y = rad * np.cos(ang), rad * np.sin(ang)
            
        countries_factory.append({
            'CODE': code, 'NAME': vietnamese_name, 'Gold': np.random.randint(5, 500) if code != 'USA' else 8133, 'X': x, 'Y': y
        })
    return pd.DataFrame(countries_factory)

df_global = load_infinite_financial_database()
name_list = df_global['NAME'].tolist()

with col_ctrl2:
    default_index = name_list.index("Việt Nam") if "Việt Nam" in name_list else 0
    target_country = st.selectbox("🔍 Chọn tâm điểm quốc gia điều hướng:", name_list, index=default_index)

with col_ctrl3:
    # THANH TRƯỢT ZOOM TIẾN HÓA VÔ CẤP ĐA TẦNG DỮ LIỆU
    zoom_slider = st.slider(
        "🔍 Tiêu cự Kính hiển vi (Zoom Level):", 
        min_value=1.0, max_value=10.0, value=1.0, step=0.1
    )

# 3. THUẬT TOÁN FRACTAL TỰ ĐỘNG SINH MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ CHẰNG CHỊT
fig = go.Figure()

target_row = df_global[df_global['NAME'] == target_country].to_dict('records')[0]
t_x, t_y = target_row['X'], target_row['Y']
usa_x, usa_y = 0.0, 0.0

# Tính toán tỷ lệ hiển thị lũy tiến
macro_opacity = max(0.0, min(1.0, (4.0 - zoom_slider) / 3.0))
micro_opacity = max(0.0, min(1.0, (zoom_slider - 1.5) / 3.5))

# --- TẦNG 1: KHÍ QUYỂN (MẠNG LƯỚI VĨ MÔ 195 NƯỚC QUY TỤ VỀ MỸ) ---
if macro_opacity > 0:
    edge_macro_x, edge_macro_y = [], []
    for _, row in df_global.iterrows():
        if row['CODE'] != 'USA':
            edge_macro_x.extend([row['X'], usa_x, None])
            edge_macro_y.extend([row['Y'], usa_y, None])
            
    fig.add_trace(go.Scatter(
        x=edge_macro_x, y=edge_macro_y, mode='lines',
        line=dict(width=1.0, color=line_color), opacity=macro_opacity * 0.2, hoverinfo='none'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_global['X'], y=df_global['Y'], mode='markers+text',
        text=df_global['NAME'], textposition="top center",
        marker=dict(size=np.log1p(df_global['Gold']) * 2 + 4, color='#FFD700', opacity=macro_opacity),
        textfont=dict(size=9, color='#888888'), hoverinfo='none'
    ))

# --- TẦNG 2: MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ DÀY ĐẶC (BỪNG SÁNG VÔ CỰC KHI ZOOM SÂU) ---
if micro_opacity > 0:
    # 🌟 ĐỘT PHÁ THUẬT TOÁN: Tự động sinh ngẫu nhiên hàng trăm nút tài sản, ngành nghề phụ trợ 
    # rải rác xung quanh quốc gia để tạo độ dày đặc, đan chéo chằng chịt thực sự của nền kinh tế
    np.random.seed(42) # Cố định hạt giống để lưới không bị nhảy hình khi kéo slider
    num_nodes = 45     # Sinh ra 45 điểm nút thực thể đa ngành đan cài chéo mạch
    
    sub_nodes = {}
    categories = ["🏭 Nhà Máy SME", "🏙️ BĐS Phân Khúc Lõi", "🔌 Tổ Hợp Công Nghệ", "🛢️ Năng Lượng Lõi", "📈 Chứng Khoán Tăng Trưởng", "👥 Hộ Dân Cư / Nhà Đầu Tư"]
    
    # Khởi tạo các điểm thực thể hạt nhân chính
    sub_nodes["🌐 [GATEWAY] Cổng Thanh Khoản USD Quốc Tế"] = [t_x + 2.0, t_y + 2.0]
    sub_nodes["🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn"] = [t_x, t_y]
    sub_nodes["👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Quốc Gia"] = [t_x + 0.8, t_y - 0.8]
    
    # Tự động sinh hàng chục thực thể ngành dọc chằng chịt rải rác xung quanh
    for i in range(num_nodes):
        cat = np.random.choice(categories)
        off_x = np.random.uniform(-4.0, 4.0)
        off_y = np.random.uniform(-4.0, 4.0)
        sub_nodes[f"{cat} [Mã Sector-{100+i}]"] = [t_x + off_x, t_y + off_y]
        
    # THUẬT TOÁN MA TRẬN DÂY: Tự động kẻ hàng trăm đường kết nối chéo liên hoàn, đan xen chằng chịt quy tụ về NHTW và USD
    micro_x, micro_y = [], []
    node_keys = list(sub_nodes.keys())
    
    # Kết nối lõi xương sống
    micro_x.extend([sub_nodes[node_keys[0]][0], sub_nodes[node_keys[1]][0], None])
    micro_y.extend([sub_nodes[node_keys[0]][1], sub_nodes[node_keys[1]][1], None])
    micro_x.extend([sub_nodes[node_keys[1]][0], sub_nodes[node_keys[2]][0], None])
    micro_y.extend([sub_nodes[node_keys[1]][1], sub_nodes[node_keys[2]][1], None])
    
    # Thuật toán liên kết chéo (Cross-industry Matrix Strands)
    for i in range(3, len(node_keys)):
        # Mỗi ngành nghề phụ phụ sẽ kéo dây nối chằng chịt về NHTW
        micro_x.extend([sub_nodes[node_keys[i]][0], sub_nodes[node_keys[1]][0], None])
        micro_y.extend([sub_nodes[node_keys[i]][1], sub_nodes[node_keys[1]][1], None])
        
        # Tạo kết nối đan chéo sang 2 ngành nghề ngẫu nhiên khác bên cạnh để tạo độ dày đặc như mạng nhện
        for _ in range(2):
            random_partner = np.random.choice(node_keys)
            micro_x.extend([sub_nodes[node_keys[i]][0], sub_nodes[random_partner][0], None])
            micro_y.extend([sub_nodes[node_keys[i]][1], sub_nodes[random_partner][1], None])

    # Vẽ toàn bộ bó sợi mạch máu tiền tệ dày đặc vào 1 lớp trace duy nhất để tối ưu phần cứng
    fig.add_trace(go.Scatter(
        x=micro_x, y=micro_y, mode='lines',
        line=dict(width=1.5, color=line_color),
        opacity=micro_opacity * 0.7, hoverinfo='none'
    ))
    
    # KÉO TUYẾN ĐẠI LỘ TỐI CAO: Chạy thẳng từ Mỹ (0,0) đâm xuyên không gian cắm vào cổng Gateway USD sở tại
    gate_x, gate_y = sub_nodes["🌐 [GATEWAY] Cổng Thanh Khoản USD Quốc Tế"]
    fig.add_trace(go.Scatter(
        x=[usa_x, gate_x], y=[usa_y, gate_y], mode='lines',
        line=dict(width=2.5, color=line_color, dash='dash'),
        opacity=micro_opacity * 0.6, hoverinfo='none'
    ))
    
    # Ghim các biểu tượng điểm thắt bừng sáng và bảng tên đa ngành
    node_x_coords = [v[0] for v in sub_nodes.values()]
    node_y_coords = [v[1] for v in sub_nodes.values()]
    
    fig.add_trace(go.Scatter(
        x=node_x_coords, y=node_y_coords, mode='markers+text',
        text=node_keys, textposition="top center",
        marker=dict(size=8, color='#00FFCC', symbol='circle', line=dict(color='white', width=1)),
        textfont=dict(size=9, color='#00FFCC'),
        opacity=micro_opacity, hoverinfo='text'
    ))

# 4. ĐIỀU CHỈNH ỐNG KÍNH CAMERA THEO NẤC SLIDER
if zoom_slider < 3.0:
    x_range = [-115, 115]
    y_range = [-95, 95]
else:
    factor = 1.0 / (zoom_slider - 1.9)
    x_range = [t_x - 30 * factor, t_x + 30 * factor]
    y_range = [t_y - 25 * factor, t_y + 25 * factor]

# LAYOUT KHÔNG GIAN SỐ VÔ CỰC - NỀN ĐEN SÂU THẲM - CHỈ CÓ MẠNG LƯỚI ĐƯỜNG TIỀN
fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=x_range),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=y_range),
    margin=dict(l=0, r=0, t=0, b=0), height=750,
    plot_bgcolor='#050505', # Nền vũ trụ tối sâu thẳm giúp mạng lưới huyết mạch đường xá bằng tiền rực sáng neon
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# 5. KHỐI MA TRẬN PHÂN TÍCH LOGIC KINH TẾ (ĐỒNG BỘ 100%)
st.markdown("---")
st.markdown("### 🧱 MA TRẬN BẢN CHẤT KINH TẾ VÀ ĐIỂM TRÚ ẨN CỦA CÁC LOẠI TÀI SẢN CHI TIẾT XUYÊN SUỐT CÁC CẤP")
col_l, col_r = st.columns(2)
with col_l:
    st.markdown("#### 🌍 Luồng Vốn Quốc Tế (Vĩ mô toàn cầu)")
    if is_usd_strong: st.error("🚨 **USD MẠNH:** Lực hút kéo dòng tiền 195 nước chạy dọc theo chuỗi mạch máu màu **ĐỎ** rút ròng về tài sản gửi tại Mỹ.")
    else: st.success("🌊 **USD YẾU:** Tiền rẻ bung xõa qua mạch máu màu **XANH** đổ dồn vào **VÀNG VẬT CHẤT** chống lạm phát mất giá tiền giấy.")
with col_r:
    st.markdown(f"#### 🎯 Hoạt Động Đa Ngành Vi Mô Tại: {target_country}")
    if is_usd_strong: st.warning("🛡️ **Tài sản phòng thủ lên ngôi:** Các tập đoàn đa ngành ngừng vay nợ USD để tránh lỗ tỷ giá. Người dân rút tiền khỏi chứng khoán gửi tiết kiệm lãi suất cao.")
