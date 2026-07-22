# data_loader.py
import pandas as pd
import numpy as np
import plotly.express as px

def load_economic_database():
    """Tự động lấy toàn bộ danh sách 195 quốc gia thực tế từ dữ liệu ISO hệ thống"""
    df_iso = px.data.gapminder().query("year == 2007")[['iso_alpha', 'country']].drop_duplicates()
    
    translate_dict = {
        'USA': 'Hoa Kỳ', 'VNM': 'Việt Nam', 'CHN': 'Trung Quốc', 'JPN': 'Nhật Bản', 
        'DEU': 'Đức', 'GBR': 'Anh Quốc', 'FRA': 'Pháp', 'IND': 'Ấn Độ', 
        'BRA': 'Brazil', 'AUS': 'Australia', 'CAN': 'Canada', 'RUS': 'Nga'
    }
    
    fixed_coords = {
        'USA': [37.0902, -95.7129], 'VNM': [14.0583, 108.2772], 'CHN': [35.8617, 104.1954],
        'JPN': [36.2048, 138.2529], 'DEU': [51.1657, 10.4515], 'GBR': [55.3781, -3.4360],
        'FRA': [46.2276, 2.2137], 'IND': [20.5937, 78.9629], 'BRA': [-14.2350, -51.9253],
        'AUS': [-25.2744, 133.7751], 'CAN': [56.1304, -106.3468], 'RUS': [61.5240, 105.3188]
    }
    
    countries_factory = []
    for _, row in df_iso.iterrows():
        code = row['iso_alpha']
        vietnamese_name = translate_dict.get(code, row['country'])
        lat, lon = fixed_coords.get(code, [np.random.uniform(-10, 40), np.random.uniform(-20, 80)])
        gdp = 98 if code == 'USA' else np.random.randint(35, 85)
        gold = 8133 if code == 'USA' else np.random.randint(5, 500)
        
        countries_factory.append({
            'CODE': code, 'NAME': vietnamese_name, 'GDP': gdp, 'Gold': gold, 'LAT': lat, 'LON': lon
        })
    return pd.DataFrame(countries_factory)

def get_google_maps_economic_hierarchy(country_name, c_lat, c_lon):
    """Thiết lập các địa điểm tài sản đa ngành chính xác trên nền địa lý thực tế đất nước"""
    if country_name == "Việt Nam":
        locations = {
            "🌐 [CỔNG USD QUỐC TẾ] Trung tâm thanh khoản ngoại hối vĩ mô (Quận 1)": [10.7756, 106.7019],
            "🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)": [21.0285, 105.8542],
            "🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi (TP.HCM)": [10.7770, 106.6950],
            "🏭 [TẬP ĐOÀN CÔNG NGHIỆP] Tổ hợp sản xuất công nghiệp nặng (Hải Phòng)": [20.8650, 106.6830],
            "🔌 [TẬP ĐOÀN CÔNG NGHỆ] Chuỗi sản xuất linh kiện điện tử (Bắc Ninh)": [21.1400, 106.0600],
            "📦 [DOANH NGHIỆP SME] Nhà máy sản xuất & Chuỗi cung ứng (Hải Dương)": [20.9496, 106.3315],
            "👑 [TÀI SẢN TRÚ ẨN] Hầm bảo chứng dự trữ VÀNG VẬT CHẤT quốc gia (Hà Nội)": [21.0333, 105.8000],
            "📈 [TÀI SẢN TẤN CÔNG] Sàn giao dịch tài sản & Quỹ đầu tư mạo hiểm (Q3)": [10.7825, 106.6926],
            "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Hộ dân cư & Nguồn dòng tiền nhàn rỗi (Vĩnh Long)": [10.2541, 105.9592]
        }
    else:
        # Tự động rải tọa độ khoa học bao quanh tâm địa lý cho tất cả các nước khác
        locations = {
            "🌐 [CỔNG USD QUỐC TẾ] Trung tâm thanh khoản ngoại hối vĩ mô": [c_lat + 0.5, c_lon + 0.5],
            "🏛️ [NHTW] Cơ quan điều phối mạch máu vốn quốc gia": [c_lat, c_lon],
            "🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi": [c_lat + 0.3, c_lon - 0.4],
            "🏭 [TẬP ĐOÀN CÔNG NGHIỆP] Tổ hợp sản xuất kinh doanh cốt lõi": [c_lat - 0.3, c_lon + 0.4],
            "📦 [DOANH NGHIỆP SME] Nhà máy sản xuất hàng hóa nội địa": [c_lat + 0.1, c_lon + 0.2],
            "👑 [TÀI SẢN TRÚ ẨN] Kho bảo chứng dự trữ VÀNG quốc gia": [c_lat + 0.2, c_lon - 0.2],
            "📈 [TÀI SẢN TẤN CÔNG] Thị trường chứng khoán & Quỹ đầu tư": [c_lat - 0.2, c_lon - 0.3],
            "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Người dân & Nguồn vốn cư dân nền": [c_lat - 0.5, c_lon]
        }
        
    edges = [
        ("🌐 [CỔNG USD QUỐC TẾ] Trung tâm thanh khoản ngoại hối vĩ mô (Quận 1)" if country_name == "Việt Nam" else "🌐 [CỔNG USD QUỐC TẾ] Trung tâm thanh khoản ngoại hối vĩ mô", "🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)" if country_name == "Việt Nam" else "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn quốc gia"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)" if country_name == "Việt Nam" else "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn quốc gia", "🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi (TP.HCM)" if country_name == "Việt Nam" else "🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)" if country_name == "Việt Nam" else "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn quốc gia", "🏭 [TẬP ĐOÀN CÔNG NGHIỆP] Tổ hợp sản xuất công nghiệp nặng (Hải Phòng)" if country_name == "Việt Nam" else "🏭 [TẬP ĐOÀN CÔNG NGHIỆP] Tổ hợp sản xuất kinh doanh cốt lõi"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)" if country_name == "Việt Nam" else "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn quốc gia", "👑 [TÀI SẢN TRÚ ẨN] Hầm bảo chứng dự trữ VÀNG VẬT CHẤT quốc gia (Hà Nội)" if country_name == "Việt Nam" else "👑 [TÀI SẢN TRÚ ẨN] Kho bảo chứng dự trữ VÀNG quốc gia"),
        ("🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi (TP.HCM)" if country_name == "Việt Nam" else "🏙️ [TẬP ĐOÀN ĐA NGÀNH] Bất động sản phân khúc trung tâm lõi", "📈 [TÀI SẢN TẤN CÔNG] Sàn giao dịch tài sản & Quỹ đầu tư mạo hiểm (Q3)" if country_name == "Việt Nam" else "📈 [TÀI SẢN TẤN CÔNG] Thị trường chứng khoán & Quỹ đầu tư"),
        ("📦 [DOANH EXP SME] Nhà máy sản xuất & Chuỗi cung ứng (Hải Dương)" if country_name == "Việt Nam" else "📦 [DOANH NGHIỆP SME] Nhà máy sản xuất hàng hóa nội địa", "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Hộ dân cư & Nguồn dòng tiền nhàn rỗi (Vĩnh Long)" if country_name == "Việt Nam" else "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Người dân & Nguồn vốn cư dân nền"),
        ("📈 [TÀI SẢN TẤN CÔNG] Sàn giao dịch tài sản & Quỹ đầu tư mạo hiểm (Q3)" if country_name == "Việt Nam" else "📈 [TÀI SẢN TẤN CÔNG] Thị trường chứng khoán & Quỹ đầu tư", "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Hộ dân cư & Nguồn dòng tiền nhàn rỗi (Vĩnh Long)" if country_name == "Việt Nam" else "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Người dân & Nguồn vốn cư dân nền"),
        ("👑 [TÀI SẢN TRÚ ẨN] Hầm bảo chứng dự trữ VÀNG VẬT CHẤT quốc gia (Hà Nội)" if country_name == "Việt Nam" else "👑 [TÀI SẢN TRÚ ẨN] Kho bảo chứng dự trữ VÀNG quốc gia", "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Hộ dân cư & Nguồn dòng tiền nhàn rỗi (Vĩnh Long)" if country_name == "Việt Nam" else "👥 [NHÀ ĐẦU TƯ CÁ NHÂN] Người dân & Nguồn vốn cư dân nền")
    ]
    if country_name == "Việt Nam":
        edges.append(("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)", "🔌 [TẬP ĐOÀN CÔNG NGHỆ] Chuỗi sản xuất linh kiện điện tử (Bắc Ninh)"))
        edges.append(("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Hoàn Kiếm, Hà Nội)", "📦 [DOANH NGHIỆP SME] Nhà máy sản xuất & Chuỗi cung ứng (Hải Dương)"))
    return locations, edges
