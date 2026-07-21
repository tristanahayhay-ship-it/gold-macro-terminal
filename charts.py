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

    # Lớp 2: Điểm định vị bong bóng trữ lượng Vàng (Chứa customdata để bắt sự kiện Click)
    fig_global.add_trace(go.Scattergeo(
        lon=df_global['LON'], lat=df_global['LAT'],
        text=df_global['NAME'] + "<br>Trữ lượng vàng: " + df_global['Gold'].astype(str) + " tấn",
        customdata=df_global['NAME'],
        mode='markers',
        marker=dict(size=np.log1p(df_global['Gold']) * 4 + 5, color='#FFD700', line=dict(color='#000', width=1)),
        hoverinfo='text', name='Hầm dự trữ Vàng'
    ))

    # Lớp 3: Sợi dây luồng tiền vĩ mô kết nối toàn bộ hệ thống quốc tế về Mỹ
    usa_coords = [37.09, -95.71]
    for _, row in df_global.iterrows():
        if row['CODE'] != 'USA':
            fig_global.add_trace(go.Scattergeo(
                lon=[row['LON'], usa_coords], lat=[row['LAT'], usa_coords],
                mode='lines', line=dict(width=1.8, color=line_color), opacity=0.5, hoverinfo='none'
            ))

    # SỬA LỖI TẠI ĐÂY: Thay 'rgba(0,0,0,0)' bằng màu chuẩn '#FFFFFF' (hoặc bỏ hẳn backgroundcolor)
    fig_global.update_layout(
        geo=dict(
            showframe=False, 
            showcoastlines=True, 
            projection_type='natural earth', 
            backgroundcolor='#FFFFFF'  # Đã sửa thành màu trắng hợp lệ
        ),
        margin=dict(l=0, r=0, t=0, b=0), 
        height=650, 
        showlegend=False
    )
    return fig_global

def draw_micro_network(nodes, edges, line_color):
    """Vẽ sơ đồ mạng lưới bộ máy vi mô kết nối bằng chuỗi dây liên kết mạch máu"""
    fig_micro = go.Figure()

    # Tạo tọa độ dòng chảy cho sợi dây vi mô
    edge_x, edge_y = [], []
    for edge in edges:
        x0, y0 = nodes[edge[0]] # SỬA LỖI LOGIC: Đảm bảo bóc tách đúng phần tử tuple của edge
        x1, y1 = nodes[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig_micro.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=3, color=line_color), mode='lines', hoverinfo='none'))

    # Tạo các hộp khối đại diện cho từng cấp vận hành bộ máy
    node_x = [v[0] for v in nodes.values()] # SỬA LỖI LOGIC: Bóc tách chính xác X và Y từ mảng tọa độ
    node_y = [v[1] for v in nodes.values()]
    
    fig_micro.add_trace(go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=list(nodes.keys()), textposition="top center",
        marker=dict(size=30, color='#1A365D', symbol='square-dot', line=dict(color='white', width=2)),
        hoverinfo='text'
    ))

    fig_micro.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=40, r=40, t=40, b=40), height=550, plot_bgcolor='rgba(0,0,0,0)', showlegend=False
    )
    return fig_micro
