# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    BẢN ĐỒ TIẾN HÓA LŨY TIẾN GOOGLE EARTH ECONOMICS.
    Sửa lỗi biến mất bằng cơ chế gộp Trace dữ liệu thông suốt 100%.
    """
    fig = go.Figure()

    # Trích xuất dữ liệu tọa độ an toàn tuyệt đối
    target_list = df_global[df_global['NAME'] == target_country].to_dict('records')
    c_lat, c_lon = (target_list[0]['LAT'], target_list[0]['LON']) if target_list else (14.0583, 108.2772)
    usa_lat, usa_lon = 37.0902, -95.7129

    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

    # 1. TÍNH TOÁN ĐỘ MỜ (OPACITY) ĐỘNG THEO NẤC ZOOM CỦA HỆ THỐNG GIÚP PHÂN RÃ TỰ NHIÊN
    macro_opacity = max(0.0, min(1.0, (3.5 - zoom_level) / 2.0))
    op_vimo = max(0.0, min(1.0, (zoom_level - 2.5) / 1.0)) # Bừng sáng từ zoom 2.5 trở lên

    # -------------------------------------------------------------------------
    # LỚP VĨ MÔ: 195 QUỐC GIA (Hiển thị ở tầng khí quyển xa)
    # -------------------------------------------------------------------------
    if macro_opacity > 0:
        # Gộp toàn bộ dây vĩ mô của 195 nước vào 1 Trace duy nhất để chống quá tải đồ họa
        macro_x, macro_y = [], []
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                macro_x.extend([row['LON'], usa_lon, None])
                macro_y.extend([row['LAT'], usa_lat, None])
                
        fig.add_trace(go.Scattermapbox(
            lat=macro_y, lon=macro_x, mode='lines',
            line=dict(width=1.5, color=line_color), opacity=macro_opacity * 0.3, hoverinfo='none'
        ))
        
        # Ghim bong bóng vàng vĩ mô toàn cầu
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='text+markers', text=df_global['NAME'], textposition="top center",
            marker=dict(size=12, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=10, color='gray'), hoverinfo='none'
        ))

    # -------------------------------------------------------------------------
    # LỚP VI MÔ: SƠ ĐỒ ĐA NGÀNH RẢI RÁC ĐỊA LÝ (BỪNG SÁNG KHI ZOOM SÂU >= 2.5)
    # -------------------------------------------------------------------------
    if op_vimo > 0:
        # BIỆN PHÁP SỬA LỖI CỐT LÕI: Gộp toàn bộ sợi dây liên kết mạch máu vi mô vào duy nhất 1 Trace
        micro_x, micro_y = [], []
        for edge in edges:
            node_start, node_end = edge[0], edge[1]
            if node_start in locations and node_end in locations:
                lat0, lon0 = locations[node_start]
                lat1, lon1 = locations[node_end]
                micro_x.extend([lon0, lon1, None])
                micro_y.extend([lat0, lat1, None])
                
        fig.add_trace(go.Scattermapbox(
            lat=micro_y, lon=micro_x, mode='lines+markers',
            line=dict(width=3.5, color=line_color), opacity=op_vimo * 0.8, hoverinfo='none'
        ))

        # LOGIC TỐI CAO: Kéo mạch máu liên lục địa từ Hoa Kỳ cắm thẳng vào Cổng USD sở tại trên bản đồ
        usd_gate_key = [k for k in locations.keys() if "CỔNG USD" in k]
        if usd_gate_key:
            gate_lat, gate_lon = locations[usd_gate_key[0]]
            fig.add_trace(go.Scattermapbox(
                lat=[usa_lat, gate_lat], lon=[usa_lon, gate_lon],
                mode='lines', line=dict(width=2.5, color=line_color, dash='dash'), 
                opacity=op_vimo * 0.6, hoverinfo='none'
            ))

        # Gộp toàn bộ các hộp nút ghim thực thể đa ngành (Hầm vàng, Nhà máy, Tập đoàn) vào 1 lớp duy nhất
        node_lats = [v[0] for v in locations.values()]
        node_lons = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons, mode='markers+text',
            text=node_labels, textposition="top right",
            marker=dict(size=14, color='#1A365D', symbol='circle', line=dict(color='white', width=1.5)),
            textfont=dict(size=11, color='#1A365D', weight='bold'), opacity=op_vimo, hoverinfo='text'
        ))

    # ĐIỀU HƯỚNG CAMERA TỰ ĐỘNG THEO TIÊU CỰ THỜI GIAN THỰC ĐỒNG BỘ HOÀN HẢO
    current_center = dict(lat=20.0, lon=20.0) if zoom_level < 3.0 else dict(lat=c_lat, lon=c_lon)
    
    fig.update_layout(
        mapbox=dict(style="open-street-map", center=current_center, zoom=zoom_level),
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
