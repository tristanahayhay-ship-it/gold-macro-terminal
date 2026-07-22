# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    Hợp nhất vĩ mô và vi mô. Sửa lỗi ẩn đồ họa khi Zoom to.
    Bảo toàn mạng lưới liên kết dây dẫn đè trực tiếp lên Google Maps.
    """
    fig = go.Figure()

    # Tìm tọa độ quốc gia mục tiêu để điều phối tiêu cự
    target_row = df_global[df_global['NAME'] == target_country].iloc
    c_lat, c_lon = target_row['LAT'], target_row['LON']
    usa_lat, usa_lon = 37.0902, -95.7129

    # -------------------------------------------------------------------------
    # LỚP VĨ MÔ 195 QUỐC GIA (Luôn vẽ làm nền, không lo bị xám màn hình khi Zoom)
    # -------------------------------------------------------------------------
    fig.add_trace(go.Scattermapbox(
        lat=df_global['LAT'], lon=df_global['LON'],
        mode='markers',
        marker=dict(size=12, color='#FFD700', opacity=0.6 if zoom_level < 3.5 else 0.2),
        hoverinfo='none'
    ))

    # -------------------------------------------------------------------------
    # CHẾ ĐỘ 1: GÓC NHÌN VĨ MÔ TOÀN CẦU (Zoom < 3.5)
    # -------------------------------------------------------------------------
    if zoom_level < 3.5:
        # Kẻ dây luồng vốn vĩ mô từ 195 nước kết nối trực tiếp về tâm dịch Mỹ
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=1.5, color=line_color), opacity=0.3, hoverinfo='none'
                ))
        
        # Hiện tên quốc gia và bong bóng hầm vàng
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='text+markers', text=df_global['NAME'],
            textposition="top center",
            marker=dict(size=14, color='#FF4B4B' if line_color=="#FF4B4B" else "#00D46A"),
            hovertemplate="<b>%{text}</b><br>Đã đồng bộ mạch máu dòng tiền vĩ mô<extra></extra>"
        ))
        
        mapbox_config = dict(style="open-street-map", center=dict(lat=20.0, lon=20.0), zoom=zoom_level)

    # -------------------------------------------------------------------------
    # CHẾ ĐỘ 2: GÓC NHÌN VI MÔ CHI TIẾT ĐA NGÀNH (Zoom >= 3.5) -> BỪNG SÁNG TẠI CHỖ
    # -------------------------------------------------------------------------
    else:
        # Tải cấu trúc địa điểm đa ngành thực tế rải rác địa lý của nước đó
        locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)
        
        # Lấy tọa độ nút Cổng USD quốc tế để làm điểm tiếp nhận dòng vốn xuyên đại dương
        usd_gate_key = [k for k in locations.keys() if "CỔNG USD" in k]
        if usd_gate_key:
            gate_lat, gate_lon = locations[usd_gate_key[0]]
            # LOGIC TỐI CAO: Kẻ sợi dây xuyên mạch liên mạch nối trực tiếp từ Hoa Kỳ cắm thẳng vào Cổng USD nội địa
            fig.add_trace(go.Scattermapbox(
                lat=[usa_lat, gate_lat], lon=[usa_lon, gate_lon],
                mode='lines', line=dict(width=3, color=line_color, dash='dash'), opacity=0.7, hoverinfo='none'
            ))

        # Kẻ chuỗi sợi dây mạch máu nội bộ (Xanh/Đỏ) kết nối xuyên suốt qua các tỉnh thành đa ngành
        for edge in edges:
            lat0, lon0 = locations[edge]
            lat1, lon1 = locations[edge]
            fig.add_trace(go.Scattermapbox(
                lat=[lat0, lat1], lon=[lon0, lon1],
                mode='lines+markers', 
                line=dict(width=4, color=line_color), 
                opacity=0.9, hoverinfo='none'
            ))

        # Ghim các bảng tên thực thể đa ngành (NHTW, Tập đoàn, Doanh nghiệp, Hầm vàng) đè lên vị trí địa lý Google Maps
        node_lats = [v for v in locations.values()]
        node_lons = [v for v in locations.values()]
        node_labels = list(locations.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons,
            mode='markers+text',
            text=node_labels,
            textposition="top right",
            marker=dict(size=16, color='#1A365D', symbol='circle'),
            textfont=dict(size=11, color='black', weight='bold'),
            hoverinfo='text'
        ))

        # Điều khiển ống kính phóng sát vào tọa độ thực tế của quốc gia
        mapbox_config = dict(style="open-street-map", center=dict(lat=c_lat, lon=c_lon), zoom=zoom_level)

    # Cấu hình Layout tối ưu hóa cho Python 3.14 trên Streamlit Cloud
    fig.update_layout(
        mapbox=mapbox_config,
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
