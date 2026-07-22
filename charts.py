# charts.py
import plotly.graph_objects as go
import numpy as np

def draw_unified_economic_map(df_global, selected_country, is_usd_strong, line_color):
    """
    Vẽ một BẢN ĐỒ KINH TẾ CHUNG DUY NHẤT. Tự động chuyển đổi hiển thị luồng vốn vĩ mô
    hoặc mạng lưới vi mô trực tiếp tại chỗ dựa trên việc Zoom camera.
    """
    fig = go.Figure()

    # Lớp nền 1: Bản đồ nhiệt thể hiện sức mạnh GDP kinh tế của 195 quốc gia
    fig.add_trace(go.Choropleth(
        locations=df_global['CODE'], z=df_global['GDP'], text=df_global['NAME'],
        colorscale='Viridis', colorbar_title="Sức mạnh GDP",
        marker_line_color='#2c3e50', marker_line_width=0.8, hoverinfo="text+z"
    ))

    # Lớp nền 2: Các hầm dự trữ Vàng thế giới (Chứa thuộc tính click customdata)
    fig.add_trace(go.Scattergeo(
        lon=df_global['LON'], lat=df_global['LAT'],
        text=df_global['NAME'] + "<br>Trữ lượng vàng: " + df_global['Gold'].astype(str) + " tấn",
        customdata=df_global['NAME'],
        mode='markers',
        marker=dict(size=np.log1p(df_global['Gold']) * 4 + 6, color='#FFD700', line=dict(color='#000', width=1)),
        hoverinfo='text', name='Hầm dự trữ Vàng'
    ))

    # TÌNH HUỐNG 1: CHẾ ĐỘ THU NHỎ TOÀN CẦU (Bản đồ luồng vốn liên quốc gia)
    if selected_country is None:
        usa_coords = [37.09, -95.71]
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattergeo(
                    lon=[row['LON'], usa_coords[1]], lat=[row['LAT'], usa_coords[0]],
                    mode='lines', line=dict(width=1.8, color=line_color), opacity=0.4, hoverinfo='none'
                ))
        
        # Cấu hình camera ở xa nhìn bao quát toàn bộ Trái Đất
        geo_layout = dict(showframe=False, showcoastlines=True, projection_type='natural earth')

    # TÌNH HUỐNG 2: CHẾ ĐỘ PHÓNG TO (Hiện mạng lưới vi mô trực tiếp trên bề mặt quốc gia đó)
    else:
        # Tìm tọa độ tâm địa lý của nước được click chọn
        target = df_global[df_global['NAME'] == selected_country].iloc[0]
        c_lat, c_lon = target['LAT'], target['LON']

        # Khởi tạo tọa độ địa lý thực tế rải rác xung quanh nước đó cho 5 cấp bộ máy kinh tế
        nodes = {
            "1. TOÀN CẦU (USD)": [c_lat + 4.0, c_lon],
            f"2. NHTW / CP {selected_country}": [c_lat + 1.5, c_lon],
            "3. Tập Đoàn Đa Quốc Gia": [c_lat - 1.0, c_lon - 2.0],
            "4. Doanh Nghiệp Core (SME)": [c_lat - 1.0, c_lon + 2.0],
            "5. Nhà Đầu Tư Cá Nhân": [c_lat - 3.5, c_lon]
        }
        
        edges = [
            ("1. TOÀN CẦU (USD)", f"2. NHTW / CP {selected_country}"),
            (f"2. NHTW / CP {selected_country}", "3. Tập Đoàn Đa Quốc Gia"),
            (f"2. NHTW / CP {selected_country}", "4. Doanh Nghiệp Core (SME)"),
            ("3. Tập Đoàn Đa Quốc Gia", "5. Nhà Đầu Tư Cá Nhân"),
            ("4. Doanh Nghiệp Core (SME)", "5. Nhà Đầu Tư Cá Nhân")
        ]

        # Vẽ chuỗi sợi dây vi mô kết nối luân chuyển tiền tệ (Xanh/Đỏ) ngay trên đất nước
        for edge in edges:
            lat0, lon0 = nodes[edge[0]]
            lat1, lon1 = nodes[edge[1]]
            fig.add_trace(go.Scattergeo(
                lon=[lon0, lon1], lat=[lat0, lat1],
                mode='lines', line=dict(width=3.5, color=line_color), opacity=0.9, hoverinfo='none'
            ))

        # Vẽ các điểm nút bộ máy kinh tế đè lên bản đồ địa lý quốc gia
        node_lats = [v[0] for v in nodes.values()]
        node_lons = [v[1] for v in nodes.values()]
        
        fig.add_trace(go.Scattergeo(
            lon=node_lons, lat=node_lats,
            mode='markers+text', text=list(nodes.keys()), textposition="top center",
            marker=dict(size=14, color='#1A365D', symbol='square', line=dict(color='white', width=1.5)),
            hoverinfo='text'
        ))

        # Cấu hình camera PHÓNG TO SÁT VÀO QUỐC GIA (Không đổi trang, giữ nguyên bản đồ địa lý)
        geo_layout = dict(
            showframe=False, showcoastlines=True,
            showland=True, landcolor="#F4F6F9",
            showcountries=True, countrycolor="gray",
            projection_type='natural earth',
            center=dict(lat=c_lat, lon=c_lon), # Ghim tâm bản đồ vào nước chọn
            projection_scale=6.5               # Phóng đại tiêu cự camera bản đồ lên 6.5 lần
        )

    # Đẩy cấu hình layout chuẩn tương thích tuyệt đối Python 3.14
    fig.update_layout(
        geo=geo_layout,
        margin=dict(l=0, r=0, t=0, b=0), height=650, showlegend=False
    )
    return fig
