import streamlit as st
import plotly.graph_objects as go

# 1. Cấu hình giao diện Streamlit ép nền đen tuyệt đối (Ultra Dark Mode)
st.set_page_config(layout="wide", page_title="Cyber Global Money Flow Terminal")

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

# 2. Cơ sở dữ liệu tọa độ địa lý chuẩn [Kinh độ, Vĩ độ]
global_locations = {
    # === ĐIỂM A: NỘI ĐỊA MỸ (Cấu trúc phân cấp 4 tầng) ===
    "US_Xa_Commune": [-100.0, 35.0],          
    "US_Huyen_District": [-92.0, 38.0],       
    "US_Tinh_Province": [-84.0, 40.0],        
    "US_NewYork_WallStreet": [-74.0060, 40.7128], 

    # === ĐIỂM B: NỘI ĐỊA TRUNG QUỐC (Cấu trúc phân cấp 4 tầng) ===
    "CN_Xa_Commune": [100.0, 25.0],           
    "CN_Huyen_District": [108.0, 28.0],       
    "CN_Tinh_Province": [114.0, 31.0],        
    "CN_Beijing_Central": [116.4074, 39.9042], 

    # === CỤM NỘI ĐỊA VIỆT NAM (Kết nối trung gian) ===
    "VN_Xa_CoSo": [105.5000, 16.0000],         
    "VN_Huyen_Hub": [106.3000, 18.5000],       
    "VN_Tinh_Center": [107.5000, 20.0000],     
    "VN_HaNoi_Central": [105.8542, 21.0285],   

    # === KHỐI LIÊN LỤC ĐỊA TRUNG CHUYỂN ===
    "Singapore_Global_Hub": [103.8198, 1.3521] 
}

# 3. Danh sách dòng chảy kết nối mạng lưới đa tầng
global_flows = [
    # ================= MẠCH LIÊN KẾT XUYÊN LỤC ĐỊA (MỸ ↔ TRUNG QUỐC) =================
    {"from": "US_NewYork_WallStreet", "to": "CN_Beijing_Central", "status": "strong_out", "desc": "Mỹ rút ròng dòng vốn đầu tư vĩ mô khỏi thị trường Trung Quốc"},
    {"from": "CN_Beijing_Central", "to": "US_NewYork_WallStreet", "status": "strong_in", "desc": "Trung Quốc đẩy mạnh xuất khẩu hàng hóa công nghiệp thu Đô-la Mỹ"},
    {"from": "Singapore_Global_Hub", "to": "VN_HaNoi_Central", "status": "strong_in", "desc": "Dòng vốn ngoại FDI quốc tế bơm thẳng về đầu não Việt Nam"},
    {"from": "VN_HaNoi_Central", "to": "US_NewYork_WallStreet", "status": "neutral", "desc": "Việt Nam xuất khẩu linh kiện công nghệ sang thị trường Mỹ"},

    # ================= MẠCH NỘI ĐỊA BÊN TRONG MỸ (ĐIỂM A) =================
    {"from": "US_Xa_Commune", "to": "US_Huyen_District", "status": "neutral", "desc": "[MỸ - XÃ ➔ HUYỆN] Nông sản thô đổ về cụm công nghiệp huyện chế biến"},
    {"from": "US_Huyen_District", "to": "US_Tinh_Province", "status": "strong_in", "desc": "[MỸ - HUYỆN ➔ TỈNH] Thành phẩm gom lên phân phối tại đô thị cấp Tỉnh"},
    {"from": "US_Tinh_Province", "to": "US_NewYork_WallStreet", "status": "strong_in", "desc": "[MỸ - TỈNH ➔ QUỐC GIA] Dòng thặng dư tài chính kết chuyển về Wall Street"},

    # ================= MẠCH NỘI ĐỊA BÊN TRONG TRUNG QUỐC (ĐIỂM B) =================
    {"from": "CN_Xa_Commune", "to": "CN_Huyen_District", "status": "strong_in", "desc": "[TQ - XÃ ➔ HUYỆN] Tiền lương sản xuất chuyển về hộ gia đình ở Xã"},
    {"from": "CN_Huyen_District", "to": "CN_Tinh_Province", "status": "strong_in", "desc": "[TQ - HUYỆN ➔ TỈNH] Hàng hóa công xưởng Huyện đẩy ra Đặc khu cấp Tỉnh"},
    {"from": "CN_Tinh_Province", "to": "CN_Beijing_Central", "status": "strong_in", "desc": "[TQ - TỈNH ➔ QUỐC GIA] Tỉnh nộp thuế sản xuất về trung ương Bắc Kinh"},

    # ================= MẠCH NỘI ĐỊA BÊN TRONG VIỆT NAM =================
    {"from": "VN_Xa_CoSo", "to": "VN_Huyen_Hub", "status": "neutral", "desc": "[VN - XÃ ➔ HUYỆN] Người dân gửi tiền tích lũy lên hệ thống tín dụng Huyện"},
    {"from": "VN_Huyen_Hub", "to": "VN_Tinh_Center", "status": "strong_in", "desc": "[VN - HUYỆN ➔ TỈNH] Doanh nghiệp nộp thuế sản xuất địa phương về Tỉnh"},
    {"from": "VN_Tinh_Center", "to": "VN_HaNoi_Central", "status": "strong_out", "desc": "[VN - TỈNH ➔ QUỐC GIA] Tỉnh kết chuyển ngân sách về Kho bạc Trung ương"}
]

# 4. Định nghĩa bảng màu phát sáng dạ quang chuẩn Cyberpunk
color_map = {
    "strong_in": "#00FF66",   
    "strong_out": "#FF0033",  
    "neutral": "#FFFF00"     
}

fig = go.Figure()

# 5. ĐỒ HỌA ĐƯỜNG DÂY DÒNG CHẢY TIỀN TỆ
for flow in global_flows:
    lon0, lat0 = global_locations[flow["from"]]
    lon1, lat1 = global_locations[flow["to"]]
    flow_color = color_map.get(flow["status"], "#FFFFFF")
    
    is_global = "WallStreet" in flow["from"] or "Central" in flow["from"] or "Hub" in flow["from"]
    line_width = 4 if is_global else 2
    
    fig.add_trace(go.Scattergeo(
        lon=[lon0, lon1],
        lat=[lat0, lat1],
        mode='lines+markers',
        line=dict(width=line_width, color=flow_color),
        marker=dict(size=4, color=flow_color),
        hoverinfo='text',
        text=flow["desc"],
        opacity=0.85
    ))

# 6. ĐỒ HỌA ĐIỂM NÚT QUỐC GIA PHÂN CẤP SỐNG ĐỘNG
node_lons = []
node_lats = []
node_texts = []
node_colors = []
node_sizes = []

for name, coords in global_locations.items():
    node_lons.append(coords[0])
    node_lats.append(coords[1])
    node_texts.append(name.replace("_", " "))
    
    if any(k in name for k in ["Central", "Street", "Hub"]) and "Huyen" not in name:
        node_colors.append("#FF6600") 
        node_sizes.append(14)
    else:
        node_colors.append("#00FFFF") 
        node_sizes.append(8)

fig.add_trace(go.Scattergeo(
    lon=node_lons,
    lat=node_lats,
    mode='markers',
    marker=dict(
        size=node_sizes,
        color=node_colors,
        line=dict(width=1, color='#FFFFFF'),
        symbol='circle'
    ),
    hoverinfo='text',
    text=node_texts
))

# 7. THIẾT KẾ BẢN ĐỒ THẾ GIỚI PHẲNG MÀU CYBERPUNK
fig.update_layout(
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='#000000', 
    geo=dict(
        showland=True,
        landcolor='#05131a',       
        showlakes=False,
        showcountries=True,
        countrycolor='#006688',    
        showocean=True,
        oceancolor='#000000',      
        projection_type='equirectangular', 
        showframe=False,
        coastlinecolor='#00aaff',  
        coastlinewidth=1.2,
        center=dict(lon=10.0, lat=25.0), 
        lonaxis=dict(range=[-140, 160]),
        lataxis=dict(range=[-10, 65])
    )
)

# 8. Hiển thị đồ họa tương tác cao cấp lên giao diện web
st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': False})
