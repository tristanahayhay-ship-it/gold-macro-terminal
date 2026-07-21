# data_loader.py
import pandas as pd

def load_economic_database():
    """Khởi tạo danh sách quốc gia với tọa độ trung tâm chính xác"""
    countries = [
        {'CODE': 'USA', 'NAME': 'Hoa Kỳ', 'GDP': 98, 'Gold': 8133, 'LAT': 37.09, 'LON': -95.71},
        {'CODE': 'VNM', 'NAME': 'Việt Nam', 'GDP': 45, 'Gold': 12, 'LAT': 14.05, 'LON': 108.27},
        {'CODE': 'CHN', 'NAME': 'Trung Quốc', 'GDP': 88, 'Gold': 2264, 'LAT': 35.86, 'LON': 104.19},
        {'CODE': 'JPN', 'NAME': 'Nhật Bản', 'GDP': 78, 'Gold': 846, 'LAT': 36.20, 'LON': 138.25},
        {'CODE': 'DEU', 'NAME': 'Đức', 'GDP': 82, 'Gold': 3352, 'LAT': 51.16, 'LON': 10.45},
        {'CODE': 'GBR', 'NAME': 'Anh Quốc', 'GDP': 75, 'Gold': 310, 'LAT': 55.37, 'LON': -3.43},
        {'CODE': 'FRA', 'NAME': 'Pháp', 'GDP': 73, 'Gold': 2436, 'LAT': 46.22, 'LON': 2.21},
        {'CODE': 'IND', 'NAME': 'Ấn Độ', 'GDP': 68, 'Gold': 803, 'LAT': 20.59, 'LON': 78.96},
        {'CODE': 'BRA', 'NAME': 'Brazil', 'GDP': 55, 'Gold': 130, 'LAT': -14.23, 'LON': -51.92},
        {'CODE': 'AUS', 'NAME': 'Australia', 'GDP': 70, 'Gold': 80, 'LAT': -25.27, 'LON': 133.77},
        {'CODE': 'CAN', 'NAME': 'Canada', 'GDP': 72, 'Gold': 0, 'LAT': 56.13, 'LON': -106.34},
        {'CODE': 'RUS', 'NAME': 'Nga', 'GDP': 65, 'Gold': 2332, 'LAT': 61.52, 'LON': 105.31},
        {'CODE': 'SGP', 'NAME': 'Singapore', 'GDP': 74, 'Gold': 230, 'LAT': 1.35, 'LON': 103.81},
    ]
    return pd.DataFrame(countries)

def get_geographic_hierarchy(country_name, c_lat, c_lon):
    """
    Tự động phân bổ tọa độ địa lý thực tế (LAT, LON) cho 5 cấp bộ máy kinh tế
    nằm bao quanh khu vực của quốc gia được chọn trên bản đồ.
    """
    # Tạo độ lệch kinh vĩ độ nhỏ để các nút phân cấp nằm rải rác trên bản đồ nước đó
    nodes = {
        "1. TOÀN CẦU (Hệ thống USD)": [c_lat + 4.0, c_lon],
        f"2. NHTW / Chính Phủ {country_name}": [c_lat + 1.5, c_lon],
        "3. Tập Đoàn Đa Quốc Gia": [c_lat - 1.0, c_lon - 2.0],
        "4. Doanh Nghiệp Sản Xuất Core": [c_lat - 1.0, c_lon + 2.0],
        "5. Nhà Đầu Tư Cá Nhân": [c_lat - 3.5, c_lon]
    }
    
    edges = [
        ("1. TOÀN CẦU (Hệ thống USD)", f"2. NHTW / Chính Phủ {country_name}"),
        (f"2. NHTW / Chính Phủ {country_name}", "3. Tập Đoàn Đa Quốc Gia"),
        (f"2. NHTW / Chính Phủ {country_name}", "4. Doanh Nghiệp Sản Xuất Core"),
        ("3. Tập Đoàn Đa Quốc Gia", "5. Nhà Đầu Tư Cá Nhân"),
        ("4. Doanh Nghiệp Sản Xuất Core", "5. Nhà Đầu Tư Cá Nhân")
    ]
    return nodes, edges
