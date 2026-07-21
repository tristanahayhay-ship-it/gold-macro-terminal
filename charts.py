# charts.py
import plotly.graph_objects as go
import numpy as np

def draw_global_map(df_global, line_color):
    """Vẽ bản đồ 195 nước kết hợp mạng lưới sợi dây vĩ mô hướng về Hoa Kỳ"""
    fig_global = go.Figure()

    # Lớp 1: Bản đồ nhiệt thể hiện sức mạnh GDP kinh tế
    fig_global.add_trace(go.Choropleth(
        locations=df_global['CODE'], z=df_global['GDP'], text=df_global['NAME'],
        colorscale='Viridis', colorbar_title="Sức mạnh GDP",
        marker_line_color='#2c3e50', marker_line_width=0.8, hoverinfo="text+z"
    ))

    # Lớp 2: Điểm định vị bong bóng trữ lượng Vàng
    fig_global.add_trace(go.Scattergeo(
        lon=df_global['LON'], lat=df_global['LAT'],
        text=df_global['NAME'] + "<br>Trữ lượng vàng: " + df_global['Gold'].astype(str) + " tấn",
        customdata=df_global['NAME'],
        mode='markers',
        marker=dict(size=np.log1p(df_global['Gold']) * 4 + 5, color='#FFD700', line=dict(color='#000', width=1)),
        hoverinfo='text', name='Hầm dự trữ Vàng'
    ))

    # Lớp 3: Sợi dây luồng tiền vĩ mô kết nối về Mỹ
    usa_coords = [37.09, -95.71]
    for _, row in df_global.iterrows():
        if row['CODE'] != 'USA':
            fig_global.add_trace(go.Scattergeo(
                lon=[row['LON'], usa_coords[1]], lat=[row['LAT'], usa_coords[0]],
                mode='lines', line=dict(width=1.8, color=line_color), opacity=0.5, hoverinfo='none'
            ))

    fig_global.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
        margin=dict(l=0, r=0, t=0, b=0), height=650, showlegend=False
    )
    return fig_global

def draw_geographic_micro_network(df_global, country_name, nodes, edges, line_color, c_lat, c_lon):
    """
    Vẽ mạng lưới vi mô 5 cấp bậc dòng tiền ĐÈ TRỰC TIẾP lên nền bản đồ địa lý
    và tự động phóng to (Zoom In) vào tọa độ của quốc gia đó.
    """
    fig_micro = go.Figure()

    # Lớp 1: Vẫn giữ nền bản đồ nhiệt thế giới phía dưới để làm nền địa lý thực tế
    fig_micro.add_trace(go.Choropleth(
        locations=df_global['CODE'], z=df_global['GDP'], text=df_global['NAME'],
        colorscale='Viridis', showscale=False, opacity=0.4,
        marker_line_color='lightgray', marker_line_width=0.5, hoverinfo="none"
    ))

    # Lớp 2: Vẽ các sợi dây liên kết mạch máu dòng tiền vi mô (Xanh/Đỏ) theo tọa độ kinh vĩ thực tế
    for edge in edges:
        lat0, lon0 = nodes[edge[0]]
        lat1, lon1 = nodes[edge[1]]
        fig_micro.add_trace(go.Scattergeo(
            lon=[lon0, lon1], lat=[lat0, lat1],
            mode='lines',
            line=dict(width=3, color=line_color),
            opacity=0.9, hoverinfo='none'
        ))

    # Lớp 3: Tạo các điểm nút bộ máy hiển thị tên thực thể địa lý
    node_lats = [v[0] for v in nodes.values()]
    node_lons = [v[1] for v in nodes.values()]
    node_labels = list(nodes.keys())

    fig_micro.add_trace(go.Scattergeo(
        lon=node_lons, lat=node_lats,
        mode='markers+text',
        text=node_labels,
        textposition="top center",
        marker=dict(size=14, color='#1A365D', symbol='square', line=dict(color='gold', width=1.5)),
        hoverinfo='text'
    ))

    # ĐIỀU CHỈNH CAMERA PHÓNG TO (ZOOM IN) VÀO KHU VỰC QUỐC GIA ĐÓ
    fig_micro.update_layout(
        geo=dict(
            showframe=False, showcoastlines=True,
            projection_type='natural earth',
            center=dict(lat=c_lat, lon=c_lon), # Đặt tâm camera tại nước được chọn
            projection_scale=6                 # Tăng tỷ lệ scale để tạo hiệu ứng Zoom sâu vào quốc gia
        ),
        margin=dict(l=0, r=0, t=0, b=0), height=650, showlegend=False
    )
    return fig_micro
