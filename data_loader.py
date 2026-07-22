# data_loader.py
import pandas as pd

def load_economic_database():
    """Khởi tạo danh sách quốc gia toàn cầu"""
    countries = [
        {'CODE': 'USA', 'NAME': 'Hoa Kỳ', 'GDP': 98, 'Gold': 8133, 'LAT': 37.09, 'LON': -95.71},
        {'CODE': 'VNM', 'NAME': 'Việt Nam', 'GDP': 45, 'Gold': 12, 'LAT': 14.05, 'LON': 108.27},
        {'CODE': 'CHN', 'NAME': 'Trung Quốc', 'GDP': 88, 'Gold': 2264, 'LAT': 35.86, 'LON': 104.19},
        {'CODE': 'JPN', 'NAME': 'Nhật Bản', 'GDP': 78, 'Gold': 846, 'LAT': 36.20, 'LON': 138.25},
        {'CODE': 'DEU', 'NAME': 'Đức', 'GDP': 82, 'Gold': 3352, 'LAT': 51.16, 'LON': 10.45},
    ]
    return pd.DataFrame(countries)

def get_google_maps_hierarchy(country_name, c_lat, c_lon):
    """
    Tạo ra các địa điểm kinh tế đa ngành, tập đoàn và các loại tài sản thực tế
    nằm tại các tọa độ địa lý chính xác (Ví dụ mô phỏng chi tiết cho Việt Nam)
    """
    if country_name == "Việt Nam":
        # Địa điểm thực tế đa ngành rải rác khắp đất nước
        locations = {
            "1. CỔNG KẾT NỐI USD QUỐC TẾ (Trung tâm Tài chính)": [10.77, 106.70], # TP.HCM
            "2. NGÂN HÀNG TRUNG ƯƠNG (NHTW / Điều phối vốn)": [21.02, 105.85],   # Hà Nội
            "3. TẬP ĐOÀN ĐA NGÀNH (Bất động sản lõi / Công nghiệp)": [16.05, 108.20], # Đà Nẵng
            "4. KHU CÔNG NGHIỆP SME (Doanh nghiệp sản xuất hàng hóa)": [20.95, 106.33], # Hải Dương
            "5. HẦM TRỮ VÀNG VẬT CHẤT (Tài sản trú ẩn tối hậu)": [21.03, 105.80], # Ba Đình, Hà Nội
            "6. QUỸ ĐẦU TƯ TẤN CÔNG (Cổ phiếu tăng trưởng)": [10.78, 106.69], # Quận 1, TP.HCM
            "7. HỘ DÂN CƯ & NHÀ ĐẦU TƯ CÁ NHÂN (Nguồn tiền nền)": [10.25, 105.95] # Vĩnh Long
        }
        
        # Sợi dây liên kết mạch máu dòng tiền, tất cả logic đều dẫn truyền qua NHTW kết nối thẳng tới USD
        edges = [
            ("1. CỔNG KẾT NỐI USD QUỐC TẾ (Trung tâm Tài chính)", "2. NGÂN HÀNG TRUNG ƯƠNG (NHTW / Điều phối vốn)"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG (NHTW / Điều phối vốn)", "3. TẬP ĐOÀN ĐA NGÀNH (Bất động sản lõi / Công nghiệp)"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG (NHTW / Điều phối vốn)", "4. KHU CÔNG NGHIỆP SME (Doanh nghiệp sản xuất hàng hóa)"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG (NHTW / Điều phối vốn)", "5. HẦM TRỮ VÀNG VẬT CHẤT (Tài sản trú ẩn tối hậu)"),
            ("3. TẬP ĐOÀN ĐA NGÀNH (Bất động sản lõi / Công nghiệp)", "6. QUỸ ĐẦU TƯ TẤN CÔNG (Cổ phiếu tăng trưởng)"),
            ("4. KHU CÔNG NGHIỆP SME (Doanh nghiệp sản xuất hàng hóa)", "7. HỘ DÂN CƯ & NHÀ ĐẦU TƯ CÁ NHÂN (Nguồn tiền nền)"),
            ("6. QUỸ ĐẦU TƯ TẤN CÔNG (Cổ phiếu tăng trưởng)", "7. HỘ DÂN CƯ & NHÀ ĐẦU TƯ CÁ NHÂN (Nguồn tiền nền)"),
            ("5. HẦM TRỮ VÀNG VẬT CHẤT (Tài sản trú ẩn tối hậu)", "7. HỘ DÂN CƯ & NHÀ ĐẦU TƯ CÁ NHÂN (Nguồn tiền nền)")
        ]
    else:
        # Giả lập tương tự cho các quốc gia khác dựa vào tâm của nước đó
        locations = {
            "1. CỔNG KẾT NỐI USD QUỐC TẾ": [c_lat + 2.0, c_lon + 2.0],
            "2. NGÂN HÀNG TRUNG ƯƠNG": [c_lat, c_lon],
            "3. TẬP ĐOÀN ĐA NGÀNH LỚN": [c_lat - 2.0, c_lon - 2.0],
            "4. DOANH NGHIỆP SẢN XUẤT SME": [c_lat - 2.0, c_lon + 2.0],
            "5. TÀI SẢN TRÚ ẨN (VÀNG)": [c_lat + 1.5, c_lon - 1.5],
            "6. NHÀ ĐẦU TƯ CÁ NHÂN": [c_lat - 4.0, c_lon]
        }
        edges = [
            ("1. CỔNG KẾT NỐI USD QUỐC TẾ", "2. NGÂN HÀNG TRUNG ƯƠNG"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG", "3. TẬP ĐOÀN ĐA NGÀNH LỚN"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG", "4. DOANH NGHIỆP SẢN XUẤT SME"),
            ("2. NGÂN HÀNG TRUNG ƯƠNG", "5. TÀI SẢN TRÚ ẨN (VÀNG)"),
            ("3. TẬP ĐOÀN ĐA NGÀNH LỚN", "6. NHÀ ĐẦU TƯ CÁ NHÂN"),
            ("4. DOANH NGHIỆP SẢN XUẤT SME", "6. NHÀ ĐẦU TƯ CÁ NHÂN"),
            ("5. TÀI SẢN TRÚ ẨN (VÀNG)", "6. NHÀ ĐẦU TƯ CÁ NHÂN")
        ]
        
    return locations, edges
