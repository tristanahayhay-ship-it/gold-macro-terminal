# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_real_google_maps_engine(df_global, target_country_name, zoom_value, line_color):
    """
    Dựng bản đồ số thực tế bao phủ toàn bộ hơn 195 quốc gia.
    Tự động hiển thị vi mô đa ngành tại chỗ khi camera Zoom sát.
    """
    fig = go.Figure()

    # Tìm quốc gia đích để điều hướng camera
    target_row = df_global[df_global['NAME'] == target_country_name].iloc
    c_lat, c_lon = target_row['LAT'], target_row['LON']

    # 1. LỚP ĐỒ HỌA VĨ MÔ (Hiển thị khi ở tầm nhìn xa: Zoom thấp)
    if zoom_value < 3.5:
        # Hiển thị các bong bóng hầm vàng bảo chứng tài sản của tất cả các quốc gia thế giới
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='markers+text',
            text=df_global['NAME'],
            marker=dict(size=np.log1p(df_global['Gold']) * 2.5 + 4, color='#FFD700', opacity=0.7),
            hovertemplate="<b>%{text}</b><br>Trữ lượng vàng thực tế<extra></extra>"
        ))

        # Kẻ sợi dây mạch máu dòng tiền vĩ mô từ khắp 195 quốc gia quy tụ về Mỹ
        usa_lat, usa_lon = 37.0902, -95.7129
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=1.5, color=line_color), opacity=0.3, hoverinfo='none'
                ))

    # 2. LỚP ĐỒ HỌA VI MÔ (Tự động kích hoạt bừng sáng đè lên bản đồ khi Zoom sát vào đất nước)
    else:
        # Gọi thuật toán sinh tọa độ đa ngành rải rác xung quanh nước được chọn
        locations, edges = dl.generate_dynamic_micro_hierarchy(target_country_name, c_lat, c_lon)

        # Vẽ chuỗi sợi dây mạch máu kết nối đa ngành (Xanh/Đỏ tùy trạng thái USD) tại các địa điểm thực tế
        for edge in edges:
            lat0, lon0 = locations[edge]
            lat1, lon1 = locations[edge]
            fig.add_trace(go.Scattermapbox(
                lat=[lat0, lat1], lon=[lon0, lon1],
                mode='lines', line=dict(width=3.5, color=line_color), opacity=0.9, hoverinfo='none'
            ))

        # Ghim các điểm nút đại diện cho Tập đoàn, Nhà đầu tư và các loại tài sản thực tế
        node_lats = [v for v in locations.values()]
        node_lons = [v for v in locations.values()]
        node_labels = list(locations.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons,
            mode='markers+text',
            text=node_labels,
            textposition="top center",
            marker=dict(size=14, color='#1A365D', symbol='circle'),
            hoverinfo='text'
        ))

    # CẤU HÌNH CAMERA ĐIỀU PHỐI ĐỘ CAO THEO ĐÚNG ĐỘ ZOOM NGƯỜI DÙNG CHỌN (STYLE GOOGLE MAPS)
    fig.update_layout(
        mapbox=dict(
            style="open-street-map", # Hiện chi tiết đường sá, địa danh thực tế thế giới
            center=dict(lat=c_lat, lon=c_lon),
            zoom=zoom_value # Nhận giá trị Zoom trực tiếp từ thanh trượt vật lý
        ),
        margin=dict(l=0, r=0, t=0, b=0), height=700, showlegend=False
    )
    return fig
