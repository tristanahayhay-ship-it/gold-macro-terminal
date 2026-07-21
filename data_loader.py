# data_loader.py
import pandas as pd

def load_economic_database():
    """Khởi tạo danh sách quốc gia thực tế bao phủ các châu lục lớn trên bản đồ thế giới"""
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

def get_micro_hierarchy(country_name):
    """Định nghĩa chính xác mạng lưới liên kết chặt chẽ 5 cấp nội tại của quốc gia"""
    nodes = {
        "Hệ Thống Tiền Tệ Toàn Cầu (Mỹ/USD)": [0.5, 1.0],
        f"Chính Phủ & Ngân Hàng Trung Ương {country_name}": [0.5, 0.75],
        "Tập Đoàn Đa Quốc Gia & Định Chế Tài Chính": [0.25, 0.5],
        "Doanh Nghiệp Sản Xuất Lõi / SME": [0.75, 0.5],
        "Nhà Đầu Tư Cá Nhân & Hộ Dân Cư": [0.5, 0.2]
    }
    edges = [
        ("Hệ Thống Tiền Tệ Toàn Cầu (Mỹ/USD)", f"Chính Phủ & Ngân Hàng Trung Ương {country_name}"),
        (f"Chính Phủ & Ngân Hàng Trung Ương {country_name}", "Tập Đoàn Đa Quốc Gia & Định Chế Tài Chính"),
        (f"Chính Phủ & Ngân Hàng Trung Ương {country_name}", "Doanh Nghiệp Sản Xuất Lõi / SME"),
        ("Tập Đoàn Đa Quốc Gia & Định Chế Tài Chính", "Nhà Đầu Tư Cá Nhân & Hộ Dân Cư"),
        ("Doanh Nghiệp Sản Xuất Lõi / SME", "Nhà Đầu Tư Cá Nhân & Hộ Dân Cư")
    ]
    return nodes, edges
