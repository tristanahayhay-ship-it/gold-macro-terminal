# data_loader.py
import pandas as pd
import numpy as np
import plotly.express as px

def load_unified_financial_database():
    """Tự động đồng bộ danh sách hơn 195 nước thực tế từ ISO chuẩn hệ thống"""
    df_iso = px.data.gapminder().query("year == 2007")[['iso_alpha', 'country']].drop_duplicates()
    
    translate_dict = {
        'USA': 'Hoa Kỳ', 'VNM': 'Việt Nam', 'CHN': 'Trung Quốc', 'JPN': 'Nhật Bản', 
        'DEU': 'Đức', 'GBR': 'Anh Quốc', 'FRA': 'Pháp', 'IND': 'Ấn Độ', 
        'BRA': 'Brazil', 'AUS': 'Australia', 'CAN': 'Canada', 'RUS': 'Nga'
    }
    
    # Định vị ma trận tọa độ phẳng cho các nước cốt lõi quanh tâm vũ trụ USD (Gốc tọa độ 0,0)
    fixed_coords = {
        'USA': [0.0, 0.0], # Hoa Kỳ luôn là điểm trung tâm tối cao để mọi đường xá quy tụ về
        'VNM': [65.0, 35.0], 'CHN': [45.0, 40.0], 'JPN': [55.0, 50.0], 'DEU': [-35.0, 45.0], 
        'GBR': [-45.0, 55.0], 'FRA': [-40.0, 40.0], 'IND': [35.0, 20.0], 'BRA': [-50.0, -45.0], 
        'AUS': [75.0, -55.0], 'CAN': [-30.0, -60.0], 'RUS': [20.0, 65.0]
    }
    
    countries_factory = []
    for _, row in df_iso.iterrows():
        code = row['iso_alpha']
        vietnamese_name = translate_dict.get(code, row['country'])
        
        if code in fixed_coords:
            x, y = fixed_coords[code]
        else:
            # Tự động rải chéo tọa độ khoa học cho toàn bộ 195 nước bao quanh trục USD
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(35, 95)
            x, y = rad * np.cos(ang), rad * np.sin(ang)
            
        countries_factory.append({
            'CODE': code, 'NAME': vietnamese_name, 'Gold': np.random.randint(5, 500) if code != 'USA' else 8133, 'X': x, 'Y': y
        })
    return pd.DataFrame(countries_factory)

def get_google_maps_economic_hierarchy(country_name, c_lat, c_lon):
    """
    Ma trận hạ tầng tài sản đa ngành rải rác chằng chịt bao quanh đất nước được chọn.
    Thiết lập hệ thống đường xá bằng tiền tệ đan chéo liên hoàn quy tụ về USD.
    """
    locations = {
        "🌐 [GATEWAY] Cổng thanh khoản USD quốc tế": [c_lat + 1.8, c_lon + 1.8],
        "🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn": [c_lat, c_lon],
        "👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT trú ẩn": [c_lat + 0.9, c_lon - 0.9],
        "💵 [CASH TREASURY] Kho dự trữ ngoại hối USD phòng thủ": [c_lat + 1.2, c_lon],
        "📜 [GOVT BONDS] Tổng kho phát hành Trái phiếu chính phủ": [c_lat + 1.4, c_lon - 0.5],
        "🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm": [c_lat - 1.2, c_lon + 1.2],
        "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng": [c_lat - 1.6, c_lon - 1.2],
        "🔌 [HIGH-TECH ZONE] Chuỗi nhà máy linh kiện điện tử vi mạch": [c_lat + 0.6, c_lon + 2.2],
        "🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng tài sản dầu thô": [c_lat - 2.2, c_lon],
        "📈 [GROWTH STOCKS] Sàn giao dịch tài sản chứng khoán rủi ro": [c_lat - 0.6, c_lon - 2.0],
        "📦 [SME SUPPLY CHAIN] Chuỗi cung ứng logistic hàng tiêu dùng": [c_lat + 2.2, c_lon - 1.8],
        "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân & Hộ dân cư": [c_lat - 0.9, c_lon - 2.8]
    }
    
    edges = [
        ("🌐 [GATEWAY] Cổng thanh khoản USD quốc tế", "🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn"),
        ("🌐 [GATEWAY] Cổng thanh khoản USD quốc tế", "💵 [CASH TREASURY] Kho dự trữ ngoại hối USD phòng thủ"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT trú ẩn"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "📜 [GOVT BONDS] Tổng kho phát hành Trái phiếu chính phủ"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "🔌 [HIGH-TECH ZONE] Chuỗi nhà máy linh kiện điện tử vi mạch"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng dầu thô"),
        ("🏛️ [NHTW] Ngân hàng Nhà nước điều phối mạch máu vốn", "📦 [SME SUPPLY CHAIN] Chuỗi cung ứng sản xuất hàng tiêu dùng"),
        ("🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm", "📈 [GROWTH STOCKS] Sàn giao dịch tài sản chứng khoán rủi ro"),
        ("🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng dầu thô", "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng"),
        ("📦 [SME SUPPLY CHAIN] Chuỗi cung ứng sản xuất hàng tiêu dùng", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân"),
        ("🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân"),
        ("📈 [GROWTH STOCKS] Sàn giao dịch tài sản chứng khoán rủi ro", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân"),
        ("👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT trú ẩn", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân")
    ]
    return locations, edges
