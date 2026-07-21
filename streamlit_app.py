else:
    country = st.session_state.selected_country
    st.markdown(f"### 🔬 CHẾ ĐỘ VI MÔ: BỘ MÁY KINH TẾ TRÊN BẢN ĐỒ ĐỊA LÝ ({country.upper()})")
    
    if st.button("⬅️ QUAY LẠI BẢN ĐỒ TOÀN CẦU"):
        st.session_state.selected_country = None
        st.rerun()
        
    # Lấy tọa độ trung tâm của quốc gia được chọn từ database nền
    target_country = df_global[df_global['NAME'] == country].iloc[0]
    c_lat, c_lon = target_country['LAT'], target_country['LON']
        
    # Gọi cấu trúc phân cấp địa lý thực tế
    nodes, edges = dl.get_geographic_hierarchy(country, c_lat, c_lon)
    
    # Vẽ mạng lưới vi mô lồng thẳng lên bản đồ địa lý đã Zoom sát
    fig_micro = cr.draw_geographic_micro_network(df_global, country, nodes, edges, line_color, c_lat, c_lon)
    st.plotly_chart(fig_micro, use_container_width=True)
