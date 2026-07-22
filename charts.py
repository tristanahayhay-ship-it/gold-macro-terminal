# charts.py
import plotly.graph_objects as go
import numpy as np
import data_loader as dl

def draw_financial_universe_canvas(df_global, target_country, zoom_level, line_color):
    """Dựng không gian mạng lưới đường xá tiền tệ tiến hóa lũy tiến. Loại bỏ bản đồ địa lý."""
    fig = go.Figure()

    # Trích xuất dữ liệu tọa độ phẳng an toàn
    target_row = df_global[df_global['NAME'] == target_country].to_dict('records')
    t_x, t_y = (target_row[0]['X'], target_row[0]['Y']) if target_row else (65.0, 35.0)
    usa_x, usa_y = 0.0, 0.0

    locations, edges = dl.get_dense_economic_mesh(target_country, t_x, t_y)

    # Tính toán mật độ hiển thị (Opacity) động tự tăng trưởng mượt mà theo nấc trượt slider
    macro_opacity = max(0.0, min(1.0, (4.0 - zoom_level) / 3.0))
    micro_opacity = max(0.0, min(1.0, (zoom_level - 1.5) / 2.5)) # Bừng sáng mượt mà từ mức Zoom thấp

    # -------------------------------------------------------------------------
    # 🌌 TẦNG VĨ MÔ: MẠNG LƯỚI LUỒNG VỐN LIÊN QUỐC GIA (195 NƯỚC VỀ MỸ)
    # -------------------------------------------------------------------------
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
            textfont=dict(size=9, color='#888888'), hoverinfo='none'
        ))

    # -------------------------------------------------------------------------
    # 🧬 TẦNG VI MÔ: MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ ĐA NGÀNH DÀY ĐẶC CHẰNG CHỊT
    # -------------------------------------------------------------------------
    if micro_opacity > 0:
        # Nén toàn bộ hệ thống đại lộ thanh khoản nội địa vào 1 Trace tổng lực để chống lỗi ẩn hình
        micro_x, micro_y = [], []
        for start, end in edges:
            if start in locations and end in locations:
                x0, y0 = locations[start]
                x1, y1 = locations[end]
                micro_x.extend([x0, x1, None])
                micro_y.extend([y0, y1, None])
                
        fig.add_trace(go.Scatter(
            x=micro_x, y=micro_y, mode='lines',
            line=dict(width=2.5, color=line_color), opacity=micro_opacity * 0.75, hoverinfo='none'
        ))
        
        # ĐẠI LỘ TỐI CAO QUỐC TẾ: Kéo đường chỉ nối chéo mạch liên mạch từ tâm Mỹ (0,0) cắm thẳng vào cổng USD sở tại
        gate_x, gate_y = locations["🌐 [CORE-USD] Cổng Thanh Khoản Ngoại Hối Tối Cao"]
        fig.add_trace(go.Scatter(
            x=[usa_x, gate_x], y=[usa_y, gate_y], mode='lines',
            line=dict(width=2.0, color=line_color, dash='dash'),
            opacity=micro_opacity * 0.6, hoverinfo='none'
        ))
        
        # Ghim các điểm thắt bộ máy và tên tài sản đa ngành rải rác lên không gian hệ thống
        node_x_coords = [v[0] for v in locations.values()]
        node_y_coords = [v[1] for v in locations.values()]
        node_labels = list(locations.keys())
        
        # Xác định màu chữ nổi bật dựa trên xu hướng dòng tiền
        text_color = "#FF4B4B" if line_color == "#FF4B4B" else "#00D46A"
        
        fig.add_trace(go.Scatter(
            x=node_x_coords, y=node_y_coords, mode='markers+text',
            text=node_labels, textposition="top right",
            marker=dict(size=12, color='#1A365D', symbol='circle', line=dict(color='white', width=1.5)),
            textfont=dict(size=11, color=text_color),
            opacity=micro_opacity, hoverinfo='text'
        ))

    # THUẬT TOÁN ĐIỀU CHỈNH ỐNG KÍNH CAMERA THEO NẤC SLIDER (MÔ PHỎNG GOOGLE EARTH)
    if zoom_level < 3.0:
        x_range = [-115, 115]
        y_range = [-95, 95]
    else:
        # Khi Zoom sâu: Thu hẹp dải hiển thị địa lý, camera khóa chặt tâm lướt thẳng xuống dải đa ngành chằng chịt
        factor = 1.0 / (zoom_level - 1.9)
        x_range = [t_x - 35 * factor, t_x + 35 * factor]
        y_range = [t_y - 25 * factor, t_y + 25 * factor]

    # THIẾT LẬP LAYOUT PHẲNG KHÔNG GIAN TỐI GIẢN TỐI THẲM (CHỈ CÓ MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ)
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=x_range),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=y_range),
        margin=dict(l=0, r=0, t=0, b=0), height=750,
        plot_bgcolor='#111111', # Nền không gian tối sâu thẳm giúp mạng lưới huyết mạch đường xá bằng tiền rực sáng nổi bật
        showlegend=False
    )
    return fig
