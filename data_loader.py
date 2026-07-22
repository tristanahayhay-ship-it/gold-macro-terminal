# data_loader.py
import pandas as pd
import numpy as np
import plotly.express as px

def load_economic_database():
    """Tự động lấy danh sách hơn 195 nước thực tế và đồng bộ tên tiếng Việt chuẩn"""
    df_iso = px.data.gapminder().query("year == 2007")[['iso_alpha', 'country']].drop_duplicates()
    
    # Từ điển dịch tên các quốc gia chính sang tiếng Việt để tránh lỗi tìm kiếm index
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
        english_name = row['country']
        
        # Nếu có trong từ điển thì dịch sang tiếng Việt, nếu không thì giữ tên tiếng Anh hệ thống
        vietnamese_name = translate_dict.get(code, english_name)
        
        if code in fixed_coords:
            lat, lon = fixed_coords[code]
        else:
            lat = np.random.uniform(-35, 55)
            lon = np.random.uniform(-90, 120)
            
        if code == 'USA':
            gdp = 98; gold = 8133
        elif code == 'DEU':
            gdp = 82; gold = 3352
        elif code == 'CHN':
            gdp = 88; gold = 2264
        else:
            gdp = np.random.randint(35, 75)
            gold = np.random.randint(5, 400)
            
        countries_factory.append({
            'CODE': code, 'NAME': vietnamese_name, 'GDP': gdp, 'Gold': gold, 'LAT': lat, 'LON': lon
        })
        
    return pd.DataFrame(countries_factory)

def generate_dynamic_micro_hierarchy(country_name, c_lat, c_lon):
    """Tự động sinh mạng lưới vi mô đa ngành khi phóng to camera vào ranh giới địa lý"""
    locations = {
        f"🌐 [CỔNG USD] Trung tâm ngoại hối {country_name}": [c_lat + 1.2, c_lon + 1.2],
        f"🏛️ [NHTW] Điều phối vốn {country_name}": [c_lat, c_lon],
        "🏭 [ĐA NGÀNH] Tập đoàn Công nghiệp & Sản xuất": [c_lat + 0.8, c_lon - 1.0],
        "🏙️ [ĐẦU TƯ] Tập đoàn Bất động sản phân khúc lõi": [c_lat - 0.8, c_lon + 1.0],
        "👑 [TRÚ ẨN] Hầm dự trữ Vàng Vật Chất quốc gia": [c_lat + 0.4, c_lon - 0.5],
        "📈 [RỦI RO] Quỹ đầu tư Cổ phiếu tăng trưởng": [c_lat - 0.6, c_lon - 1.2],
        "👥 [NỀN TẢNG] Hộ dân cư & Nhà đầu tư cá nhân": [c_lat - 1.2, c_lon]
    }
    
    edges = [
        (f"🌐 [CỔNG USD] Trung tâm ngoại hối {country_name}", f"🏛️ [NHTW] Điều phối vốn {country_name}"),
        (f"🏛️ [NHTW] Điều phối vốn {country_name}", "🏭 [ĐA NGÀNH] Tập đoàn Công nghiệp & Sản xuất"),
        (f"🏛️ [NHTW] Điều phối vốn {country_name}", "🏙️ [ĐẦU TƯ] Tập đoàn Bất động sản phân khúc lõi"),
        (f"🏛️ [NHTW] Điều phối vốn {country_name}", "👑 [TRÚ ẨN] Hầm dự trữ Vàng Vật Chất quốc gia"),
        ("🏭 [ĐA NGÀNH] Tập đoàn Công nghiệp & Sản xuất", "👥 [NỀN TẢNG] Hộ dân cư & Nhà đầu tư cá nhân"),
        ("🏙️ [ĐẦU TƯ] Tập đoàn Bất động sản phân khúc lõi", "👥 [NỀN TẢNG] Hộ dân cư & Nhà đầu tư cá nhân"),
        ("📈 [RỦI RO] Quỹ đầu tư Cổ phiếu tăng trưởng", "👥 [NỀN TẢNG] Hộ dân cư & Nhà đầu tư cá nhân")
    ]
    return locations, edges
