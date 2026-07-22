# charts.py
import plotly.graph_objects as go
import numpy as np

def draw_google_maps_economic_engine(df_global, selected_country, line_color, locations_dict, edges_list):
    """
    Xây dựng một bản đồ số động (Mapbox), tích hợp luồng chảy vĩ mô và vi mô.
    Cho phép người dùng tương tác cuộn phóng giống hệt Google Maps.
    """
    fig = go.Figure()

    # TÌNH HUỐNG 1: CHẾ ĐỘ CAMERA Ở XA (BẢN ĐỒ TOÀN CẦU)
    if selected_country is None:
        # Vẽ các chấm tròn quốc gia và hầm vàng lên nền Mapbox
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='markers+text',
            text=df_global['NAME'],
            customdata=df_global['NAME'], # Dùng để bắt sự kiện click chuột
            marker=dict(size=np.log1p(df_global['Gold']) * 3 + 8, color='#FFD700', opacity=0.8),
            hovertemplate="<b>%{text}</b><br>Quy mô kinh tế cao<br><extra></extra>"
        ))

        # Kẻ các sợi dây mạch máu dòng tiền liên quốc gia hội tụ trực tiếp về Hoa Kỳ
        usa_lat, usa_lon = 37.09, -95.71
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=2, color=line_color), opacity=0.4, hoverinfo='none'
                ))
        
        # Thiết lập vị trí camera mặc định nhìn bao quát Trái Đất (Zoom level nhỏ)
        mapbox_config = dict(style="open-street-map", center=dict(lat=20.0, lon=0.0), zoom=1.2)

    # TÌNH HUỐNG 2: CHẾ ĐỘ CAMERA CẬN CẢNH (ZOOM IN VÀO ĐỊA ĐIỂM THỰC TẾ)
    else:
        # Tìm tọa độ gốc của nước được click để ghim camera tại chỗ
        target = df_global[df_global['NAME'] == selected_country].iloc
        c_lat, c_lon = target['LAT'], target['LON']

        # Lớp 1: Vẽ mạch máu dòng tiền vi mô kết nối xuyên suốt các địa điểm bằng sợi dây (Xanh/Đỏ)
        for edge in edges_list:
            lat0, lon0 = locations_dict[edge]
            lat1, lon1 = locations_dict[edge]
            fig.add_trace(go.Scattermapbox(
                lat=[lat0, lat1], lon=[lon0, lon1],
                mode='lines', line=dict(width=3.5, color=line_color), opacity=0.8, hoverinfo='none'
            ))

        # Lớp 2: Ghim các biểu tượng địa điểm đa ngành và các loại tài sản thực tế lên bản đồ vệ tinh đường phố
        node_lats = [v[0] for v in locations_dict.values()]
        node_lons = [v[1] for v in locations_dict.values()]
        node_labels = list(locations_dict.keys())

        fig.add_trace(go.Scattermapbox(
            lat=node_lats, lon=node_lons,
            mode='markers+text',
            text=node_labels,
            textposition="top center",
            marker=dict(size=14, color='#1A365D', symbol='circle'),
            hoverinfo='text'
        ))

        # Thiết lập camera PHÓNG TO SÁT VÀO CÁC ĐỊA ĐIỂM THÀNH PHỐ THỰC TẾ (Mô phỏng y hệt Google Maps)
        mapbox_config = dict(
            style="open-street-map", # Giao diện bản đồ số chi tiết đường sá, địa danh
            center=dict(lat=c_lat, lon=c_lon), # Khóa tâm camera tại tọa độ quốc gia chọn
            zoom=4.8 # Tiêu cự phóng to nhìn thấy rõ các tỉnh thành rải rác
        )

    # Đẩy layout cấu hình tối ưu tương thích tuyệt đối cho Python 3.14 trên Streamlit Cloud
    fig.update_layout(
        mapbox=mapbox_config,
        margin=dict(l=0, r=0, t=0, b=0), height=700, showlegend=False
    )
    return fig
