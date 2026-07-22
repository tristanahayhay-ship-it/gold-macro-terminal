# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    Hợp nhất 100% vĩ mô và vi mô vào chung một bản đồ số Mapbox.
    Mô phỏng trải nghiệm vô cấp như Google Maps, tự bung xõa cấu trúc đa ngành khi Zoom sát.
    """
    fig = go.Figure()

    # Định vị tọa độ tâm điểm của quốc gia đích để điều khiển camera
    target_row = df_global[df_global['NAME'] == target_country].iloc[0]
    c_lat, c_lon = target_row['LAT'], target_row['LON']

    # -------------------------------------------------------------------------
    # TÌNH HUỐNG A: ZOOM TẦM XA (ZOOM OUT < 3.5) -> BẢN ĐỒ LUỒNG VỐN THẾ GIỚI
    # -------------------------------------------------------------------------
    if zoom_level < 3.5:
        # Lớp vĩ mô 1: Thể hiện sức mạnh phát triển và dự trữ vàng của hơn 195 nước
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='markers+text',
            text=df_global['NAME'],
            marker=dict(size=np.log1p(df_global['Gold']) * 2.5 + 5, color='#FFD700', opacity=0.8),
            hovertemplate="<b>%{text}</b><br>Đã đồng bộ mạng lưới liên kết tài sản vĩ mô<extra></extra>"
        ))

        # Lớp vĩ mô 2: Mạng lưới khổng lồ sợi dây kết nối mạch máu quy tụ từ 195 nước về Hoa Kỳ
        usa_lat, usa_lon = 37.0902, -95.7129
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=1.5, color=line_color), opacity=0.3, hoverinfo='none'
                ))
                
        # Cấu hình camera nhìn bao quát Trái Đất
        mapbox_config = dict(style="open-street-map", center=dict(lat=22.0, lon=15.0), zoom=zoom_level)

    # -------------------------------------------------------------------------
    # TÌNH HUỐNG B: ZOOM CẬN CẢNH (ZOOM IN >= 3.5) -> SƠ ĐỒ ĐA NGÀNH NỘI TẠI TẠI CHỖ
    # -------------------------------------------------------------------------
    else:
        # Gọi cấu trúc địa điểm thực tế của nước đó rải rác theo tỉnh thành
        locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

        # Lớp vi mô 1: Sợi dây kết nối liên hoàn thắt chặt dòng chảy (Xanh/Đỏ) xuyên suốt các cấp địa điểm
        for edge in edges:
            lat0, lon0 = locations[edge[0]]
            lat1, lon1 = locations[edge[1]]
            fig.add_trace(go.Scattermapbox(
                lat=[lat0, lat1], lon=[lon0, lon1],
                mode='lines', line=dict(width=3.8, color=line_color), opacity=0.8, hoverinfo='none'
            ))

        # Lớp vi mô 2: Ghim biểu tượng hộp khối của các Tập đoàn đa ngành, Quỹ đầu tư, Hầm vàng lên bản đồ
        node_lats = [v[0] for v in locations.values()]
        node_lons = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons,
            mode='markers+text',
            text=node_labels,
            textposition="top center",
            marker=dict(size=14, color='#1A365D', symbol='circle', line=dict(color='white', width=2)),
            hoverinfo='text'
        ))

        # Cấu hình camera phóng sát xuống ranh giới địa lý thành phố thực tế
        mapbox_config = dict(style="open-street-map", center=dict(lat=c_lat, lon=c_lon), zoom=zoom_level)

    # Khóa Layout tương thích tuyệt đối cho môi trường vận hành Python 3.14
    fig.update_layout(
        mapbox=mapbox_config,
        margin=dict(l=0, r=0, t=0, b=0), height=700, showlegend=False
    )
    return fig
