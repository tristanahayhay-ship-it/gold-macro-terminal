# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """Xây dựng bản đồ Google Earth kinh tế học vô cấp, phân rã theo độ mờ liên tục"""
    fig = go.Figure()

    # BÓC TÁCH KHUNG DỮ LIỆU CHUẨN AN TOÀN CHỐNG LỖI PANDAS TYPEERROR
    target_list = df_global[df_global['NAME'] == target_country].to_dict('records')
    if target_list:
        c_lat = target_list[0]['LAT']
        c_lon = target_list[0]['LON']
    else:
        c_lat, c_lon = 14.0583, 108.2772
        
    usa_lat, usa_lon = 37.0902, -95.7129
    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

    # 计算TẦNG VĨ MÔ (Mờ dần khi Zoom sát xuống đất)
    macro_opacity = max(0.0, min(1.0, (3.5 - zoom_level) / 2.0))

    if macro_opacity > 0:
        # Kẻ luồng vốn liên quốc gia đổ về Mỹ
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=1.5, color=line_color), 
                    opacity=macro_opacity * 0.3, hoverinfo='none'
                ))
        
        # Ghim bong bóng vàng vĩ mô thế giới
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='text+markers', text=df_global['NAME'],
            textposition="top center",
            marker=dict(size=12, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=10, color='gray'), hoverinfo='none'
        ))

    # CẤU TRÚC VI MÔ ĐA TẦNG TIẾN HÓA LŨY TIẾN THEO GOOGLE EARTH (ZOOM >= 2.0)
    if zoom_level >= 2.0:
        nodes_t2 = {k: v for k, v in locations.items() if "CỔNG USD" in k or "NHTW" in k}
        nodes_t3 = {k: v for k, v in locations.items() if "TẬP ĐOÀN" in k or "TRÚ ẨN" in k}
        nodes_t4 = {k: v for k, v in locations.items() if "SME" in k or "TẤN CÔNG" in k or "NHÀ ĐẦU TƯ" in k}

        # Tính toán Opacity lũy tiến mượt mà
        op_t2 = max(0.0, min(1.0, (zoom_level - 2.0) / 1.0))
        op_t3 = max(0.0, min(1.0, (zoom_level - 3.2) / 1.0))
        op_t4 = max(0.0, min(1.0, (zoom_level - 4.2) / 1.0))

        # Kẻ chuỗi sợi dây mạch máu kết nối đa ngành nội địa tại chỗ
        for edge in edges:
            node_start, node_end = edge[0], edge[1]
            lat0, lon0 = locations[node_start]
            lat1, lon1 = locations[node_end]
            
            current_edge_opacity = op_t2
            if any(x in node_start or x in node_end for x in ["SME", "TẤN CÔNG", "NHÀ ĐẦU TƯ"]):
                current_edge_opacity = op_t4
            elif any(x in node_start or x in node_end for x in ["TẬP ĐOÀN", "TRÚ ẨN"]):
                current_edge_opacity = op_t3

            if current_edge_opacity > 0:
                fig.add_trace(go.Scattermapbox(
                    lat=[lat0, lat1], lon=[lon0, lon1],
                    mode='lines', line=dict(width=3.5, color=line_color), 
                    opacity=current_edge_opacity * 0.8, hoverinfo='none'
                ))

        # LOGIC TỐI CAO: Dây kết nối liên mạch cắm xuyên đại dương từ Hoa Kỳ vào thẳng Cổng USD sở tại
        if op_t2 > 0:
            usd_gate_key = [k for k in locations.keys() if "CỔNG USD" in k]
            if usd_gate_key:
                gate_lat, gate_lon = locations[usd_gate_key[0]]
                fig.add_trace(go.Scattermapbox(
                    lat=[usa_lat, gate_lat], lon=[usa_lon, gate_lon],
                    mode='lines', line=dict(width=2, color=line_color, dash='dash'), 
                    opacity=op_t2 * 0.5, hoverinfo='none'
                ))

        # Ghim bảng tên các thực thể kinh tế lên bản đồ vệ tinh/đường phố
        if op_t2 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_t2.values()], lon=[v[1] for v in nodes_t2.values()],
                mode='markers+text', text=list(nodes_t2.keys()), textposition="top right",
                marker=dict(size=15, color='#E67E22', symbol='circle'), opacity=op_t2,
                textfont=dict(size=11, color='#D35400', weight='bold'), hoverinfo='text'
            ))
        if op_t3 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_t3.values()], lon=[v[1] for v in nodes_t3.values()],
                mode='markers+text', text=list(nodes_t3.keys()), textposition="top center",
                marker=dict(size=14, color='#2980B9', symbol='circle'), opacity=op_t3,
                textfont=dict(size=11, color='#2471A3', weight='bold'), hoverinfo='text'
            ))
        if op_t4 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_t4.values()], lon=[v[1] for v in nodes_t4.values()],
                mode='markers+text', text=list(nodes_t4.keys()), textposition="bottom center",
                marker=dict(size=13, color='#27AE60', symbol='circle'), opacity=op_t4,
                textfont=dict(size=11, color='#1E8449', weight='bold'), hoverinfo='text'
            ))

    # ĐIỀU HƯỚNG CAMERA ĐỘC LẬP TỰ NHIÊN TẠI CHỖ
    current_center = dict(lat=20.0, lon=20.0) if zoom_level < 3.0 else dict(lat=c_lat, lon=c_lon)

    fig.update_layout(
        mapbox=dict(style="open-street-map", center=current_center, zoom=zoom_level),
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
