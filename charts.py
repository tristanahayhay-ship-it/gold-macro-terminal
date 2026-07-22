# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_mapbox_engine(df_global, target_country, zoom_level, line_color):
    """
    BẢN ĐỒ TIẾN HÓA LŨY TIẾN (GOOGLE EARTH ECONOMICS).
    Mật độ hiển thị của tài sản và sợi dây biến đổi liên tục theo độ cao camera (zoom_level).
    """
    fig = go.Figure()

    # Bóc tách tọa độ quốc gia mục tiêu an toàn
    target_data = df_global[df_global['NAME'] == target_country].to_dict('records')
    c_lat, c_lon = (target_data[0]['LAT'], target_data[0]['LON']) if target_data else (14.0583, 108.2772)
    usa_lat, usa_lon = 37.0902, -95.7129

    # Tải trước toàn bộ hệ thống dữ liệu vi mô đa ngành đa địa điểm
    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, c_lat, c_lon)

    # -------------------------------------------------------------------------
    # TẦNG 1: KHÍ QUYỂN (NỀN 195 QUỐC GIA VÀ DÂY XUYÊN ĐẠI DƯƠNG)
    # Hiển thị mạnh ở Zoom thấp, mờ dần và ẩn hẳn khi lao sát mặt đất để tránh rối mắt
    # -------------------------------------------------------------------------
    macro_opacity = max(0.0, min(1.0, (3.5 - zoom_level) / 2.0))
    
    if macro_opacity > 0:
        # Kẻ dây luồng vốn vĩ mô từ 195 nước kết nối về Mỹ
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                fig.add_trace(go.Scattermapbox(
                    lat=[row['LAT'], usa_lat], lon=[row['LON'], usa_lon],
                    mode='lines', line=dict(width=1.5, color=line_color), 
                    opacity=macro_opacity * 0.3, hoverinfo='none'
                ))
        
        # Điểm mốc và tên 195 nước trên thế giới
        fig.add_trace(go.Scattermapbox(
            lat=df_global['LAT'], lon=df_global['LON'],
            mode='text+markers', text=df_global['NAME'],
            textposition="top center",
            marker=dict(size=12, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=10, color='gray'),
            hoverinfo='none'
        ))

    # -------------------------------------------------------------------------
    # MẠNG LƯỚI VI MÔ TIẾN HÓA LŨY TIẾN THEO ĐỘ CAO CAMERA (ZOOM >= 2.0)
    # -------------------------------------------------------------------------
    if zoom_level >= 2.0:
        # Lọc và phân loại các thực thể kinh tế theo từng tầng sâu lớp địa lý
        # Tầng 2 (Tầng Mây): Cổng USD và NHTW (Hà Nội / Q1 TP.HCM)
        nodes_layer_2 = {k: v for k, v in locations.items() if "CỔNG USD" in k or "NHTW" in k}
        
        # Tầng 3 (Tầng Mặt Đất): Các tập đoàn đa ngành lớn, tổ hợp sản xuất (Hải Phòng, Bắc Ninh)
        nodes_layer_3 = {k: v for k, v in locations.items() if "TẬP ĐOÀN" in k or "TRÚ ẨN" in k}
        
        # Tầng 4 (Tầng Sinh Vật): Doanh nghiệp SME, Quỹ mạo hiểm, Người dân (Hải Dương, Q3, Vĩnh Long)
        nodes_layer_4 = {k: v for k, v in locations.items() if "SME" in k or "RỦI RO" in k or "NHÀ ĐẦU TƯ" in k}

        # Tính toán độ mờ (Opacity) động tự tăng trưởng khi camera phóng càng sâu
        op_layer_2 = max(0.0, min(1.0, (zoom_level - 2.0) / 1.0)) # Hiện từ zoom 2.0, rõ nét ở 3.0
        op_layer_3 = max(0.0, min(1.0, (zoom_level - 3.2) / 1.0)) # Hiện từ zoom 3.2, rõ nét ở 4.2
        op_layer_4 = max(0.0, min(1.0, (zoom_level - 4.2) / 1.0)) # Hiện từ zoom 4.2, rõ nét ở 5.2

        # --- VẼ SỢI DÂY LIÊN KẾT MẠCH MÁU THEO TẦNG ---
        for edge in edges:
            node_start, node_end = edge[0], edge[1]
            lat0, lon0 = locations[node_start]
            lat1, lon1 = locations[node_end]
            
            # Quyết định sợi dây thuộc tầng nào thì ăn theo độ mờ của tầng đó
            current_edge_opacity = op_layer_2
            if any(x in node_start or x in node_end for x in ["SME", "RỦI RO", "NHÀ ĐẦU TƯ"]):
                current_edge_opacity = op_layer_4
            elif any(x in node_start or x in node_end for x in ["TẬP ĐOÀN", "TRÚ ẨN"]):
                current_edge_opacity = op_layer_3

            if current_edge_opacity > 0:
                fig.add_trace(go.Scattermapbox(
                    lat=[lat0, lat1], lon=[lon0, lon1],
                    mode='lines', line=dict(width=3.5, color=line_color), 
                    opacity=current_edge_opacity * 0.8, hoverinfo='none'
                ))

        # --- LOGIC TỐI CAO: DÂY NỐI TỪ MỸ CẮM THẲNG VÀO CỔNG USD SỞ TẠI ---
        if op_layer_2 > 0:
            usd_gate_key = [k for k in locations.keys() if "CỔNG USD" in k]
            if usd_gate_key:
                gate_lat, gate_lon = locations[usd_gate_key[0]]
                fig.add_trace(go.Scattermapbox(
                    lat=[usa_lat, gate_lat], lon=[usa_lon, gate_lon],
                    mode='lines', line=dict(width=2, color=line_color, dash='dash'), 
                    opacity=op_layer_2 * 0.5, hoverinfo='none'
                ))

        # --- GHIM CÁC KHỐI THỰC THỂ LÊN GOOGLE MAPS THEO TỪNG CẤP ĐỘ TIẾN HÓA ---
        # Vẽ Tầng 2: Cổng USD và NHTW (Xuất hiện trước tiên khi lao từ mây xuống)
        if op_layer_2 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_layer_2.values()], lon=[v[1] for v in nodes_layer_2.values()],
                mode='markers+text', text=list(nodes_layer_2.keys()), textposition="top right",
                marker=dict(size=16, color='#E67E22', symbol='circle'), opacity=op_layer_2,
                textfont=dict(size=11, color='#E67E22', weight='bold'), hoverinfo='text'
            ))
            
        # Vẽ Tầng 3: Các tập đoàn xương sống đa ngành (Xuất hiện tiếp theo khi thấy rõ núi đồi)
        if op_layer_3 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_layer_3.values()], lon=[v[1] for v in nodes_layer_3.values()],
                mode='markers+text', text=list(nodes_layer_3.keys()), textposition="top center",
                marker=dict(size=15, color='#2980B9', symbol='circle'), opacity=op_layer_3,
                textfont=dict(size=11, color='#2980B9', weight='bold'), hoverinfo='text'
            ))

        # Vẽ Tầng 4: Doanh nghiệp SME, Quỹ đầu tư và túi tiền người dân (Xuất hiện cuối cùng khi nhìn rõ nhà cửa)
        if op_layer_4 > 0:
            fig.add_trace(go.Scattermapbox(
                lat=[v[0] for v in nodes_layer_4.values()], lon=[v[1] for v in nodes_layer_4.values()],
                mode='markers+text', text=list(nodes_layer_4.keys()), textposition="bottom center",
                marker=dict(size=14, color='#27AE60', symbol='circle'), opacity=op_layer_4,
                textfont=dict(size=11, color='#27AE60', weight='bold'), hoverinfo='text'
            ))

    # ĐIỀU KHIỂN ỐNG KÍNH CAMERA THEO THỜI GIAN THỰC ĐỒNG BỘ SLIDER
    # Khi zoom nhỏ thì camera ở trung tâm thế giới, khi zoom lớn camera tự động hạ độ cao xuống nước chọn
    current_center = dict(lat=20.0, lon=20.0) if zoom_level < 3.0 else dict(lat=c_lat, lon=c_lon)
    
    fig.update_layout(
        mapbox=dict(style="open-street-map", center=current_center, zoom=zoom_level),
        margin=dict(l=0, r=0, t=0, b=0), height=750, showlegend=False
    )
    return fig
