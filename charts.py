# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    BẢN ĐỒ TIẾN HÓA LŨY TIẾN GOOGLE EARTH ECONOMICS.
    Sử dụng style nền tối giản không đường sá để bừng sáng mạng lưới tài sản tương quan USD.
    Tương thích tuyệt đối với Python 3.14.
    """
    fig = go.Figure()

    # Trích xuất dữ liệu tọa độ an toàn tuyệt đối chống lỗi Pandas
    target_list = df_global[df_global['NAME'] == target_country].to_dict('records')
    if target_list:
        c_lat = target_list[0]['LAT']
        c_lon = target_list[0]['LON']
    else:
        c_lat, c_lon = 14.0583, 108.2772
        
    usa_lat, usa_lon = 37.0902, -95.7129
    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

    # Tính toán độ mờ (Opacity) động tự nhiên theo nấc Zoom camera
    macro_opacity = max(0.0, min(1.0, (3.5 - zoom_level) / 2.0))
    op_vimo = max(0.0, min(1.0, (zoom_level - 2.0) / 1.2)) # Bừng sáng mượt mà từ zoom 2.0 trở lên

    # -------------------------------------------------------------------------
    # LỚP VĨ MÔ: 195 QUỐC GIA (Hiển thị ở tầng không gian vũ trụ xa)
    # -------------------------------------------------------------------------
    if macro_opacity > 0:
        macro_x, macro_y = [], []
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                macro_x.extend([row['LON'], usa_lon, None])
                macro_y.extend([row['LAT'], usa_lat, None])
                
        fig.add_trace(go.Scattermapbox(
            lat=macro_y, lon=macro_x, mode='lines',
            line=dict(width=1.5, color=line_color), opacity=macro_opacity * 0.3, hoverinfo='none'
        ))
        
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='text+markers', text=df_global['NAME'], textposition="top center",
            marker=dict(size=12, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=10, color='gray'), hoverinfo='none'
        ))

    # -------------------------------------------------------------------------
    # LỚP VI MÔ: MẠNG LƯỚI ĐẠI LỘ TIỀN TỆ ĐAN CHÉO TƯƠNG QUAN TRỰC TIẾP USD
    # -------------------------------------------------------------------------
    if op_vimo > 0:
        # Gộp tất cả chuỗi dây liên kết mạch máu kinh tế vào 1 trace duy nhất
        micro_x, micro_y = [], []
        for edge in edges:
            node_start, node_end = edge[0], edge[1]
            if node_start in locations and node_end in locations:
                lat0, lon0 = locations[node_start]
                lat1, lon1 = locations[node_end]
                micro_x.extend([lon0, lon1, None])
                micro_y.extend([lat0, lat1, None])
                
        fig.add_trace(go.Scattermapbox(
            lat=micro_y, lon=micro_x, mode='lines',
            line=dict(width=3.5, color=line_color), opacity=op_vimo * 0.75, hoverinfo='none'
        ))

        # LOGIC TỐI CAO: Dây kết nối liên mạch cắm xuyên đại dương từ Mỹ vào thẳng Cổng USD sở tại
        usd_gate_key = [k for k in locations.keys() if "CỔNG USD" in k or "GATEWAY" in k]
        if usd_gate_key:
            gate_lat, gate_lon = locations[usd_gate_key[0]]
            fig.add_trace(go.Scattermapbox(
                lat=[usa_lat, gate_lat], lon=[usa_lon, gate_lon],
                mode='lines', line=dict(width=2.5, color=line_color, dash='dash'), 
                opacity=op_vimo * 0.6, hoverinfo='none'
            ))

        # Ghim các bảng tên thực thể đa ngành đè lên tọa độ bản đồ nền phẳng sạch
        node_lats = [v[0] for v in locations.values()]
        node_lons = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons, mode='markers+text',
            text=node_labels, textposition="top right",
            marker=dict(size=14, color='#1A365D', symbol='circle', line=dict(color='white', width=1.5)),
            textfont=dict(size=11, color='#FFD700' if is_usd_strong else '#1A365D', weight='bold'), 
            opacity=op_vimo, hoverinfo='text'
        ))

    # ĐIỀU HƯỚNG CAMERA TỰ ĐỘNG THEO TIÊU CỰ THỜI GIAN THỰC ĐỒNG BỘ HOÀN HẢO
    current_center = dict(lat=20.0, lon=20.0) if zoom_level < 3.0 else dict(lat=c_lat, lon=c_lon)
    
    # GIẢI PHÁP VÁ LỖI PYTHON 3.14: 
    # Thay 'style="carto-positron"' bằng 'style="carto-darkmatter"' (Nền tối thẳm chuyên dụng) 
    # Hoặc 'style="carto-positron-nolabels"' để xóa sạch toàn bộ mạng lưới đường bộ, nhà cửa mặc định
    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter", # Nền tối sâu thẳm giúp mạng lưới huyết mạch kinh tế của bạn sáng rực lên
            center=current_center, 
            zoom=zoom_level
        ),
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
