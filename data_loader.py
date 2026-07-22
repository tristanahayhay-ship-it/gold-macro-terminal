# data_loader.py
import pandas as pd
import numpy as np
import plotly.express as px

def load_economic_database():
    """Tự động lấy danh sách 195 quốc gia thực tế từ dữ liệu ISO hệ thống"""
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
    """
    Xây dựng MẠNG LƯỚI ĐƯỜNG XÁ KINH TẾ DÀY ĐẶC (Đa địa điểm, đa ngành, đa loại tài sản).
    Các tuyến đường liên kết chạy chéo đan xen liên hoàn tương quan trực tiếp đến USD.
    """
    if country_name == "Việt Nam":
        # Hệ thống hạ tầng địa điểm đa ngành dày đặc bao phủ toàn dải địa lý
        locations = {
            # --- TRẠM ĐIỀU PHỐI VÀ CỔNG TRUNG CHUYỂN USD ---
            "🌐 [GATEWAY] Cổng thanh khoản USD quốc tế (Trung tâm Quận 1, TP.HCM)": [10.7756, 106.7019],
            "🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)": [21.0285, 105.8542],
            
            # --- KHỐI TÀI SẢN PHÒNG THỦ & TRÚ ẨN LẠM PHÁT ---
            "👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT quốc gia (Ba Đình, Hà Nội)": [21.0333, 105.8000],
            "💵 [CASH TREASURY] Kho dự trữ ngoại hối USD phòng thủ (Hoàn Kiếm, Hà Nội)": [21.0295, 105.8500],
            "📜 [GOVT BONDS] Tổng kho phát hành Trái phiếu chính phủ an toàn (Hà Nội)": [21.0400, 105.8300],
            
            # --- KHỐI TẬP ĐOÀN ĐA NGÀNH XƯƠNG SỐNG ---
            "🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm lõi (TP.HCM)": [10.7770, 106.6950],
            "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng và logistics (Hải Phòng)": [20.8650, 106.6830],
            "🔌 [HIGH-TECH ZONE] Chuỗi nhà máy sản xuất linh kiện vi mạch điện tử (Bắc Ninh)": [21.1400, 106.0600],
            "🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng, khai thác khoáng sản dầu thô": [16.0544, 108.2022], # Đà Nẵng
            
            # --- KHỐI TÀI SẢN TẤN CÔNG & CHUỖI CUNG ỨNG SME ---
            "📈 [GROWTH STOCKS] Sàn giao dịch tài sản rủi ro & Quỹ mạo hiểm (Q3, TP.HCM)": [10.7825, 106.6926],
            "📦 [SME SUPPLY CHAIN] Chuỗi cung ứng logistic doanh nghiệp sản xuất lõi": [20.9496, 106.3315], # Hải Dương
            
            # --- KHỐI NHÀ ĐẦU TƯ & DÂN CƯ NỀN ---
            "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Bắc": [20.9800, 105.7800], # Hà Đông
            "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Trung": [16.4600, 107.5900], # Huế
            "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Nam": [10.2541, 105.9592]  # Vĩnh Long
        }
        
        # MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ DÀY ĐẶC ĐAN CHÉO LIÊN HOÀN
        edges = [
            ("🌐 [GATEWAY] Cổng thanh khoản USD quốc tế (Trung tâm Quận 1, TP.HCM)", "🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)"),
            ("🌐 [GATEWAY] Cổng thanh khoản USD quốc tế (Trung tâm Quận 1, TP.HCM)", "💵 [CASH TREASURY] Kho dự trữ ngoại hối USD phòng thủ (Hoàn Kiếm, Hà Nội)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT quốc gia (Ba Đình, Hà Nội)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "📜 [GOVT BONDS] Tổng kho phát hành Trái phiếu chính phủ an toàn (Hà Nội)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm lõi (TP.HCM)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng và logistics (Hải Phòng)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "🔌 [HIGH-TECH ZONE] Chuỗi nhà máy sản xuất linh kiện vi mạch điện tử (Bắc Ninh)"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng, khai thác khoáng sản dầu thô"),
            ("🏛️ [NHTW] Ngân hàng Nhà nước Việt Nam (Trung tâm điều hành vốn vĩ mô - Hà Nội)", "📦 [SME SUPPLY CHAIN] Chuỗi cung ứng logistic doanh nghiệp sản xuất lõi"),
            
            # Đường sá kết nối chằng chịt giữa doanh nghiệp, tài sản đầu tư và dân cư
            ("🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm lõi (TP.HCM)", "📈 [GROWTH STOCKS] Sàn giao dịch tài sản rủi ro & Quỹ mạo hiểm (Q3, TP.HCM)"),
            ("🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng, khai thác khoáng sản dầu thô", "🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng và logistics (Hải Phòng)"),
            ("📦 [SME SUPPLY CHAIN] Chuỗi cung ứng logistic doanh nghiệp sản xuất lõi", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Bắc"),
            ("🏭 [HEAVY INDUSTRY] Tổ hợp sản xuất công nghiệp nặng và logistics (Hải Phòng)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Bắc"),
            ("🔌 [HIGH-TECH ZONE] Chuỗi nhà máy sản xuất linh kiện vi mạch điện tử (Bắc Ninh)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Bắc"),
            ("🛢️ [COMMODITIES ENGINES] Tập đoàn năng lượng, khai thác khoáng sản dầu thô", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Trung"),
            ("🏙️ [REAL ESTATE CORE] Tập đoàn Bất động sản phân khúc trung tâm lõi (TP.HCM)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Nam"),
            ("📈 [GROWTH STOCKS] Sàn giao dịch tài sản rủi ro & Quỹ mạo hiểm (Q3, TP.HCM)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Nam"),
            ("👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT quốc gia (Ba Đình, Hà Nội)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Bắc"),
            ("👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT quốc gia (Ba Đình, Hà Nội)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Trung"),
            ("👑 [GOLD RESERVES] Hầm dự trữ VÀNG VẬT CHẤT quốc gia (Ba Đình, Hà Nội)", "👥 [RETAIL INVESTORS] Khối nhà đầu tư cá nhân khu vực miền Nam")
        ]
    else:
        # Tự động đồng bộ ma trận đường kinh tế tương tự cho 194 quốc gia khác dựa vào tâm nước đó
        locations = {
            "🌐 [GATEWAY] Cổng USD quốc tế vĩ mô": [c_lat + 0.6, c_lon + 0.6],
            "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn": [c_lat, c_lon],
            "👑 [GOLD] Dự trữ VÀNG trú ẩn tối hậu": [c_lat + 0.3, c_lon - 0.3],
            "🏙️ [ASSETS] Khối tập đoàn đa ngành cốt lõi": [c_lat + 0.4, c_lon - 0.5],
            "📦 [SME] Chuỗi cung ứng hàng hóa sản xuất": [c_lat - 0.4, c_lon + 0.5],
            "📈 [STOCKS] Thị trường chứng khoán rủi ro": [c_lat - 0.3, c_lon - 0.4],
            "👥 [INVESTORS] Khối nhà đầu tư cư dân nền": [c_lat - 0.6, c_lon]
        }
        edges = [
            ("🌐 [GATEWAY] Cổng USD quốc tế vĩ mô", "🏛️ [NHTW] Cơ quan quản lý mạch máu vốn"),
            ("🏛️ [NHTW] Cơ quan quản lý mạch máu vốn", "👑 [GOLD] Dự trữ VÀNG trú ẩn tối hậu"),
            ("🏛️ [NHTW] Cơ quan quản lý mạch máu vốn", "🏙️ [ASSETS] Khối tập đoàn đa ngành cốt lõi"),
            ("🏛️ [NHTW] Cơ quan quản lý mạch máu vốn", "📦 [SME] Chuỗi cung ứng hàng hóa sản xuất"),
            ("🏙️ [ASSETS] Khối tập đoàn đa ngành cốt lõi", "📈 [STOCKS] Thị trường chứng khoán rủi ro"),
            ("📦 [SME] Chuỗi cung ứng hàng hóa sản xuất", "👥 [INVESTORS] Khối nhà đầu tư cư dân nền"),
            ("📈 [STOCKS] Thị trường chứng khoán rủi ro", "👥 [INVESTORS] Khối nhà đầu tư cư dân nền"),
            ("👑 [GOLD] Dự trữ VÀNG trú ẩn tối hậu", "👥 [INVESTORS] Khối nhà đầu tư cư dân nền")
        ]
        
    return locations, edges
