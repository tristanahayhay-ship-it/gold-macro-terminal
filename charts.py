# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    DỰNG BẢN ĐỒ KINH TẾ TIẾN HÓA LŨY TIẾN GOOGLE EARTH STYLE.
    Sửa lỗi cấu hình projection_scale gây sập trên Python 3.14.
    """
    fig = go.Figure()

    # Trích xuất dữ liệu tọa độ phẳng địa lý an toàn chống lỗi Pandas
    target_list = df_global[df_global['NAME'] == target_country].to_dict('records')
    if target_list and len(target_list) > 0:
        c_lat = target_list[0]['LAT']
        c_lon = target_list[0]['LON']
    else:
        c_lat, c_lon = 14.0583, 108.2772
        
    usa_lat, usa_lon = 37.0902, -95.7129
    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

    # Tính toán mật độ hiển thị (Opacity) động tự nhiên theo nấc trượt camera
    macro_opacity = max(0.0, min(1.0, (4.5 - zoom_level) / 3.5))
    op_vimo = max(0.0, min(1.0, (zoom_level - 1.5) / 2.5))

    # -------------------------------------------------------------------------
    # TẦNG VĨ MÔ: BẢN ĐỒ 195 NƯỚC ĐỊA LÝ THẾ GIỚI
    # -------------------------------------------------------------------------
    if macro_opacity > 0:
        # Kẻ chuỗi sợi dây luồng vốn từ 195 nước quy tụ về Hoa Kỳ
        macro_lon, macro_lat = [], []
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                macro_lon.extend([row['LON'], usa_lon, None])
                macro_lat.extend([row['LAT'], usa_lat, None])
                
        fig.add_trace(go.Scattergeo(
            lon=macro_lon, lat=macro_lat, mode='lines',
            line=dict(width=1.5, color=line_color), opacity=macro_opacity * 0.25, hoverinfo='none'
        ))
        
        # Hiển thị hầm vàng bảo chứng của các nước
        fig.add_trace(go.Scattergeo(
            lon=df_global['LON'], lat=df_global['LAT'],
            mode='markers+text', text=df_global['NAME'], textposition="top center",
            marker=dict(size=np.log1p(df_global['Gold']) * 2 + 5, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=9, color='#888888'), hoverinfo='none'
        ))

    # -------------------------------------------------------------------------
    # TẦNG VI MÔ: MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ ĐAN CHÉO NHAU CHẰNG CHỊT TẠI CHỖ
    # -------------------------------------------------------------------------
    if op_vimo > 0:
        # Gộp toàn bộ hệ thống đại lộ thanh khoản chằng chịt vào 1 Trace tổng lực để chống ẩn hình
        micro_lon, micro_lat = [], []
        for start, end in edges:
            if start in locations and end in locations:
                lat0, lon0 = locations[start]
                lat1, lon1 = locations[end]
                micro_lon.extend([lon0, lon1, None])
                micro_lat.extend([lat0, lat1, None])
                
        fig.add_trace(go.Scattergeo(
            lon=micro_lon, lat=micro_lat, mode='lines',
            line=dict(width=3.5, color=line_color), opacity=op_vimo * 0.8, hoverinfo='none'
        ))
        
        # SỢI DÂY TỐI CAO QUỐC TẾ: Kéo đường dây cắm thẳng từ Mỹ vào nút Gateway USD nội địa
        gate_key = [k for k in locations.keys() if "GATEWAY" in k or "CỔNG USD" in k]
        if gate_key:
            gate_lat, gate_lon = locations[gate_key[0]]
            fig.add_trace(go.Scattergeo(
                lon=[usa_lon, gate_lon], lat=[usa_lat, gate_lat], mode='lines',
                line=dict(width=2.5, color=line_color, dash='dash'),
                opacity=op_vimo * 0.6, hoverinfo='none'
            ))
            
        # Ghim các bảng tên thực thể đa ngành (Hầm vàng, Nhà máy, Tập đoàn) lên không gian ranh giới đất nước
        node_lats = [v[0] for v in locations.values()]
        node_lons = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())
        
        fig.add_trace(go.Scattergeo(
            lon=node_lons, lat=node_lats, mode='markers+text',
            text=node_labels, textposition="top right",
            marker=dict(size=10, color='#1A365D', symbol='circle', line=dict(color='white', width=1)),
            textfont=dict(size=11, color='#1A365D'), opacity=op_vimo, hoverinfo='text'
        ))

    # -------------------------------------------------------------------------
    # ⚙️ GIẢI QUYẾT TRIỆT ĐỂ LỖI PYTHON 3.14: ĐIỀU CHỈNH ỐNG KÍNH CAMERA BẰNG TRỤC AXIS
    # Loại bỏ hoàn toàn projection_scale. Thay bằng việc thắt chặt giới hạn khung nhìn lonaxis/lataxis.
    # -------------------------------------------------------------------------
    if zoom_level < 3.0:
        # Ở xa: Bản đồ nhìn bao quát toàn bộ địa lý thế giới nền xám tinh khiết
        geo_layout = dict(
            showframe=False, showcoastlines=True, showland=True, landcolor="#222222",
            countrycolor="#444444", showcountries=True, backgroundcolor="#111111",
            projection_type='natural earth'
        )
    else:
        # Khi Zoom sâu: Thu hẹp dải hiển thị địa lý, ép camera hạ độ cao nhìn sát dải đất nước được chọn
        span = 40.0 / (zoom_level - 1.5) # Khoảng cách hiển thị thu hẹp dần theo nấc slider
        geo_layout = dict(
            showframe=False, showcoastlines=True, showland=True, landcolor="#F8F9FA",
            countrycolor="lightgray", showcountries=True, backgroundcolor="#111111",
            projection_type='natural earth',
            center=dict(lat=c_lat, lon=c_lon),
            lonaxis=dict(range=[c_lon - span, c_lon + span]), # Giới hạn dải nhìn kinh độ
            lataxis=dict(range=[c_lat - span, c_lat + span])  # Giới hạn dải nhìn vĩ độ
        )

    # Đẩy cấu hình layout chuẩn, dọn sạch mọi nguy cơ lỗi định dạng
    fig.update_layout(
        geo=geo_layout,
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
