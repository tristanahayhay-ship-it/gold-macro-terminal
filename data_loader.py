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
    
    # Định vị Hoa Kỳ làm TÂM VŨ TRỤ TIỀN TỆ (Gốc tọa độ 0,0) để mọi quốc gia tương quan hướng về
    fixed_coords = {
        'USA': [0.0, 0.0], 'VNM': [65.0, 35.0], 'CHN': [45.0, 40.0], 'JPN': [55.0, 50.0], 
        'DEU': [-35.0, 45.0], 'GBR': [-45.0, 55.0], 'FRA': [-40.0, 40.0], 'IND': [35.0, 20.0], 
        'BRA': [-50.0, -45.0], 'AUS': [75.0, -55.0], 'CAN': [-30.0, -60.0], 'RUS': [20.0, 65.0]
    }
    
    countries_factory = []
    for _, row in df_iso.iterrows():
        code = row['iso_alpha']
        vietnamese_name = translate_dict.get(code, row['country'])
        
        if code in fixed_coords:
            x, y = fixed_coords[code]
        else:
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(35, 95)
            x, y = rad * np.cos(ang), rad * np.sin(ang)
            
        countries_factory.append({
            'CODE': code, 'NAME': vietnamese_name, 'Gold': np.random.randint(5, 500) if code != 'USA' else 8133, 'X': x, 'Y': y
        })
    return pd.DataFrame(countries_factory)

def get_dense_economic_mesh(country_name, c_x, c_y):
    """
    Thiết lập MẠNG LƯỚI ĐƯỜNG XÁ KINH TẾ DÀY ĐẶC (Xóa sạch đường bộ địa lý).
    Tạo cấu trúc đa ngành, đa loại tài sản đan chéo chằng chịt, tất cả tập trung tương quan về USD.
    """
    # Khởi tạo ma trận điểm tài sản rải rác dày đặc tại quốc gia mục tiêu
    locations = {
        "🌐 [CORE-USD] Cổng Thanh Khoản Ngoại Hối Tối Cao": [c_x + 1.0, c_y + 1.0],
        "🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô": [c_x, c_y],
        
        # --- KHỐI TÀI SẢN PHÒNG THỦ & BẢO CHỨNG ---
        "👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Vật Chất Quốc Gia": [c_x + 0.5, c_y - 0.5],
        "💵 [CASH TREASURY] Tổng Kho Ngoại Hối USD Phòng Thủ": [c_x + 0.8, c_y],
        "📜 [GOVT BONDS] Kho Phát Hành Trái Phiếu Chính Phủ An Toàn": [c_x + 1.0, c_y - 0.3],
        
        # --- KHỐI TẬP ĐOÀN ĐA NGÀNH LỚN ---
        "🏙️ [REAL ESTATE CORE] Tập Đoàn Bất Động Sản Phân Khúc Trung Tâm": [c_x - 0.8, c_y + 0.8],
        "🏭 [HEAVY INDUSTRY] Tổ Hợp Sản Xuất Công Nghiệp Nặng & Vận Tải": [c_x - 1.2, c_y - 0.8],
        "🔌 [HIGH-TECH ZONE] Chuỗi Nhà Máy Linh Kiện Điện Tử Vi Mạch": [c_x + 0.3, c_y + 1.5],
        "🛢️ [COMMODITIES LÕI] Tập Đoàn Khai Thác Năng Lượng & Dầu Thô": [c_x - 1.5, c_y],
        
        # --- KHỐI TÀI SẢN TẤN CÔNG & CHUỖI CUNG ỨNG SME ---
        "📈 [GROWTH ASSETS] Quỹ Đầu Tư Mạo Hiểm & Chứng Khoán Tăng Trưởng": [c_x - 0.4, c_y - 1.2],
        "📦 [SME SUPPLY CHAIN] Chuỗi Cung Ứng Doanh Nghiệp Sản Xuất Phụ Trợ": [c_x + 1.5, c_y - 1.0],
        
        # --- KHỐI NHÀ ĐẦU TƯ CÁ NHÂN ---
        "👥 [RETAIL-INVESTOR A] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Bắc": [c_x + 0.2, c_y - 1.5],
        "👥 [RETAIL-INVESTOR B] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Trung": [c_x - 0.5, c_y - 1.8],
        "👥 [RETAIL-INVESTOR C] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Nam": [c_x - 1.0, c_y - 2.2]
    }
    
    # MẠNG LƯỚI ĐƯỜNG XÁ TIỀN TỆ ĐAN CHÉO NHAU CHẰNG CHỊT THEO TIÊU CHÍ CỦA BẠN
    edges = [
        ("🌐 [CORE-USD] Cổng Thanh Khoản Ngoại Hối Tối Cao", "🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô"),
        ("🌐 [CORE-USD] Cổng Thanh Khoản Ngoại Hối Tối Cao", "💵 [CASH TREASURY] Tổng Kho Ngoại Hối USD Phòng Thủ"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Vật Chất Quốc Gia"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "📜 [GOVT BONDS] Kho Phát Hành Trái Phiếu Chính Phủ An Toàn"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "🏙️ [REAL ESTATE CORE] Tập Đoàn Bất Động Sản Phân Khúc Trung Tâm"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "🏭 [HEAVY INDUSTRY] Tổ Hợp Sản Xuất Công Nghiệp Nặng & Vận Tải"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "🔌 [HIGH-TECH ZONE] Chuỗi Nhà Máy Linh Kiện Điện Tử Vi Mạch"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "🛢️ [COMMODITIES LÕI] Tập Đoàn Khai Thác Năng Lượng & Dầu Thô"),
        ("🏛️ [NHTW] Ngân Hàng Trung Ương Điều Phối Vốn Vĩ Mô", "📦 [SME SUPPLY CHAIN] Chuỗi Cung Ứng Doanh Nghiệp Sản Xuất Phụ Trợ"),
        
        # Các đại lộ tài sản liên kết chéo chằng chịt giữa các ngành và tài sản đầu cơ/phòng thủ
        ("🏙️ [REAL ESTATE CORE] Tập Đoàn Bất Động Sản Phân Khúc Trung Tâm", "📈 [GROWTH ASSETS] Quỹ Đầu Tư Mạo Hiểm & Chứng Khoán Tăng Trưởng"),
        ("🛢️ [COMMODITIES LÕI] Tập Đoàn Khai Thác Năng Lượng & Dầu Thô", "🏭 [HEAVY INDUSTRY] Tổ hợp Sản Xuất Công Nghiệp Nặng & Vận Tải"),
        ("🔌 [HIGH-TECH ZONE] Chuỗi Nhà Máy Linh Kiện Điện Tử Vi Mạch", "📦 [SME SUPPLY CHAIN] Chuỗi Cung Ứng Doanh Nghiệp Sản Xuất Phụ Trợ"),
        ("📦 [SME SUPPLY CHAIN] Chuỗi Cung Ứng Doanh Nghiệp Sản Xuất Phụ Trợ", "👥 [RETAIL-INVESTOR A] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Bắc"),
        ("🏭 [HEAVY INDUSTRY] Tổ Hợp Sản Xuất Công Nghiệp Nặng & Vận Tải", "👥 [RETAIL-INVESTOR A] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Bắc"),
        ("🛢️ [COMMODITIES LÕI] Tập Đoàn Khai Thác Năng Lượng & Dầu Thô", "👥 [RETAIL-INVESTOR B] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Trung"),
        ("🏙️ [REAL ESTATE CORE] Tập Đoàn Bất Động Sản Phân Khúc Trung Tâm", "👥 [RETAIL-INVESTOR C] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Nam"),
        ("📈 [GROWTH ASSETS] Quỹ Đầu Tư Mạo Hiểm & Chứng Khoán Tăng Trưởng", "👥 [RETAIL-INVESTOR C] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Nam"),
        
        # Chuỗi liên kết trực tiếp từ Hầm Vàng đến các đầu mối nhà đầu tư để trú ẩn lạm phát
        ("👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Vật Chất Quốc Gia", "👥 [RETAIL-INVESTOR A] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Bắc"),
        ("👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Vật Chất Quốc Gia", "👥 [RETAIL-INVESTOR B] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Trung"),
        ("👑 [GOLD RESERVES] Hầm Dự Trữ Vàng Vật Chất Quốc Gia", "👥 [RETAIL-INVESTOR C] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Nam"),
        ("💵 [CASH TREASURY] Tổng Kho Ngoại Hối USD Phòng Thủ", "👥 [RETAIL-INVESTOR A] Khối Nhà Đầu Tư Cá Nhân Trọng Điểm Phía Bắc")
    ]
    return locations, edges
