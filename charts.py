# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_unified_financial_canvas(df_global, target_country, zoom_level, line_color):
    """
    Dựng canvas mạng lưới tiền tệ tiến hóa lũy tiến liên mạch.
    Tối ưu hóa gộp Trace để bảo vệ dữ liệu không bao giờ biến mất khi Zoom sâu.
    """
    fig = go.Figure()

    # Trích xuất dữ liệu an toàn
    target_row = df_global[df_global['NAME'] == target_country].to_dict('records')
    t_x, t_y = (target_row[0]['X'], target_row[0]['Y']) if target_row else (65.0, 35.0)
    usa_x, usa_y = 0.0, 0.0

    locations, edges = dl.get_google_maps_economic_hierarchy(target_country, t_x, t_y)

    # Tính toán độ mờ (Opacity) động tự nhiên theo nấc Zoom camera
    macro_opacity = max(0.0, min(1.0, (4.0 - zoom_level) / 3.0))
    micro_opacity = max(0.0, min(1.0, (zoom_level - 2.0) / 3.0))

    # --- A. ĐỒ HỌA TẦNG VĨ MÔ (Mạng lưới 195 nước) ---
    if macro_opacity > 0:
        edge_macro_x, edge_macro_y = [], []
        for _, row in df_global.iterrows():
            if row['CODE'] != 'USA':
                edge_macro_x.extend([row['X'], usa_x, None])
                edge_macro_y.extend([row['Y'], usa_y, None])
                
        fig.add_trace(go.Scatter(
            x=edge_macro_x, y=edge_macro_y, mode='lines',
            line=dict(width=1.2, color=line_color), opacity=macro_opacity * 0.25, hoverinfo='none'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_global['X'], y=df_global['Y'], mode='markers+text',
            text=df_global['NAME'], textposition="top center",
            marker=dict(size=np.log1p(df_global['Gold']) * 2 + 5, color='#FFD700', opacity=macro_opacity),
            textfont=dict(size=9, color='gray'), hoverinfo='none'
        ))

    # --- B. ĐỒ HỌA TẦNG VI MÔ (Đại lộ tiền tệ chằng chịt đa ngành bừng sáng) ---
    if micro_opacity > 0:
        micro_x, micro_y = [], []
        for start, end in edges:
            x0, y0 = locations[start]
            x1, y1 = locations[end]
            micro_x.extend([x0, x1, None])
            micro_y.extend([y0, y1, None])
            
        fig.add_trace(go.Scatter(
            x=micro_x, y=micro_y, mode='lines+markers',
            line=dict(width=3.5, color=line_color), marker=dict(size=4, color='white'),
            opacity=micro_opacity * 0.85, hoverinfo='none'
        ))
        
        # SỢI DÂY LIÊN MẠCH TỐI CAO: Nối từ Hoa Kỳ (0,0) cắm sâu vào Gateway ngoại hối nội địa
        gate_x, gate_y = locations["🌐 [GATEWAY] Cổng thanh khoản USD quốc tế"]
        fig.add_trace(go.Scatter(
            x=[usa_x, gate_x], y=[usa_y, gate_y], mode='lines',
            line=dict(width=2.5, color=line_color, dash='dash'),
            opacity=micro_opacity * 0.6, hoverinfo='none'
        ))
        
        # Ghim nhãn tên thực thể đa ngành lên màn hình
        node_x_coords = [v[0] for v in locations.values()]
        node_y_coords = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())
        
        fig.add_trace(go.Scatter(
            x=node_x_coords, y=node_y_coords, mode='markers+text',
            text=node_labels, textposition="top center",
            marker=dict(size=14, color='#1A365D', symbol='square'),
            textfont=dict(size=11, color='#1A365D'),
            opacity=micro_opacity, hoverinfo='text'
        ))

    # THUẬT TOÁN ĐIỀU CHỈNH CAMERA VÔ CẤP THEO SLIDER
    if zoom_level < 3.0:
        x_range = [-115, 115]
        y_range = [-95, 95]
    else:
        factor = 1.0 / (zoom_level - 1.9)
        x_range = [t_x - 30 * factor, t_x + 30 * factor]
        y_range = [t_y - 25 * factor, t_y + 25 * factor]

    # VẼ KHUNG NỀN SẠCH TUYỆT ĐỐI - KHÔNG ĐƯỜNG XÁ ĐỊA LÝ - CHỈ HIỆN ĐẠI LỘ TIỀN TỆ KINH TẾ
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=x_range),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=y_range),
        margin=dict(l=0, r=0, t=0, b=0), height=750,
        plot_bgcolor='#F8F9FA',
        showlegend=False
    )
    return fig
