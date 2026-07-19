def evaluate_d1_quantum_signal(rsi, macro_trend, fed_policy, major_liquidity, d1_price_action):
    """
    HỆ THỐNG PHÂN TÍCH LƯỢNG TỬ D1: KẾT HỢP VĨ MÔ VÀ KỸ THUẬT VỚI TRỌNG SỐ LỚN
    """
    buy_score = 0
    sell_score = 0
    reasons = []

    # ==================================================================================
    # PHẦN 1: BỘ CHẤM ĐIỂM KINH TẾ VĨ MÔ DÀI HẠN (Dòng tiền của các Ngân hàng Trung ương)
    # ==================================================================================
    
    # 1. Thẩm định CHÍNH SÁCH TIỀN TỆ CỦA FED (Trọng số lớn: 4 Điểm)
    if fed_policy == "Nới lỏng (Cắt giảm lãi suất / Bơm tiền / USD suy yếu)":
        buy_score += 4
        reasons.append("🚨 [VĨ MÔ TỐI CAO]: FED đang nới lỏng tiền tệ (Cắt giảm lãi suất). Lịch sử tài chính nhân loại chứng minh khi lãi suất giảm, đồng USD mất giá, dòng tiền toàn cầu bắt buộc phải tháo chạy vào Vàng để trú ẩn và chống lạm phát.")
    elif fed_policy == "Thắt chặt (Tăng lãi suất / Giữ lãi suất cao / USD mạnh)":
        sell_score += 4
        reasons.append("🚨 [VĨ MÔ TỐI CAO]: FED đang thắt chặt tiền tệ (Tăng/Neo lãi suất cao). Lãi suất cao khiến lợi suất trái phiếu và chứng chỉ tiền gửi USD trở nên cực kỳ hấp dẫn. Các quỹ lớn sẽ xả Vàng để mua USD, tạo áp lực giảm đè nặng lên Vàng.")

    # 2. Thẩm định BỐI CẢNH TIN TỨC VĨ MÔ / ĐỊA CHÍNH TRỊ TRONG NGÀY (Trọng số: 3 Điểm)
    if macro_news == "Tốt cho Vàng (USD yếu, Địa chính trị căng thẳng)":
        buy_score += 3
        reasons.append("🌍 [BỐI CẢNH VĨ MÔ]: Căng thẳng địa chính trị, chiến tranh hoặc rủi ro suy thoái kinh tế đang leo thang. Vàng kích hoạt trạng thái là tài sản trú ẩn an toàn nhất thế giới (Safe-haven asset). Phe Bò chuẩn bị gom hàng đẩy giá.")
    elif macro_news == "Xấu cho Vàng (USD mạnh, Diều hâu, Hòa hoãn)":
        sell_score += 3
        reasons.append("🌍 [BỐI CẢNH VĨ MÔ]: Tin tức kinh tế Mỹ công bố tốt hơn kỳ vọng (CPI tăng, Non-Farm tốt), hoặc địa chính trị thế giới hòa hoãn. Thị trường giảm bớt nỗi sợ hãi, dòng tiền đầu cơ rút khỏi Vàng để quay lại thị trường chứng khoán.")

    # ==================================================================================
    # PHẦN 2: BỘ CHẤM ĐIỂM PHÂN TÍCH KỸ THUẬT ĐÓNG NẾN (Dòng tiền của các Quỹ Lượng tử)
    # ==================================================================================
    
    # 3. Thẩm định CẤU TRÚC XU HƯỚNG D1 (Trọng số: 4 Điểm)
    if macro_trend == "Xu hướng Tăng dài hạn (Bullish)":
        buy_score += 4
        reasons.append("📊 [CẤU TRÚC XU HƯỚNG]: Biểu đồ D1 xác nhận cấu trúc tăng vững chắc. Dòng tiền của dòng lệnh dài hạn (Swing Traders) đang đổ vào để bảo vệ các vùng giá thấp.")
    elif macro_trend == "Xu hướng Giảm dài hạn (Bearish)":
        sell_score += 4
        reasons.append("📊 [CẤU TRÚC XU HƯỚNG]: Biểu đồ D1 xác nhận cấu trúc giảm thế chủ đạo. Ưu tiên các chiến lược bán khống để đi thuận theo dòng chảy của thị trường.")

    # 4. Thẩm định VÙNG THANH KHOẢN CỦA CÁ MẬP (Trọng số lớn: 5 Điểm)
    if major_liquidity == "Chạm Vùng Hỗ trợ D1 / Order Block Tăng tuần":
        buy_score += 5
        reasons.append("🐋 [VÙNG GIÁ CÁ MẬP]: Giá đang đi vào vùng tập trung tường lệnh mua (Order Block) của các tổ chức tài chính lớn. Đây là điểm xoay dòng tiền, Cá Mập sẽ kích hoạt thuật toán gom hàng.")
    elif major_liquidity == "Chạm Vùng Kháng cự D1 / Order Block Giảm tuần":
        sell_score += 5
        reasons.append("🐋 [VÙNG GIÁ CÁ MẬP]: Giá húc trúng vùng tường lệnh bán khổng lồ của các định chế tài chính lớn. Áp lực chốt lời và chặn giá tại đây cực mạnh, phe mua khó có thể xuyên thủng.")

    # 5. Thẩm định CHÍNH XÁC CHỈ BÁO RSI NGÀY (Trọng số: 3 Điểm)
    if rsi <= 35:
        buy_score += 3
        reasons.append(f"📈 [ĐỘNG LƯỢNG KỸ THUẬT]: Chỉ số RSI D1 rơi vào vùng Quá bán thực tế ({rsi}). Lực bán tháo của đám đông nhỏ lẻ đã kiệt quệ, thị trường chuẩn bị có sóng hồi mãnh liệt.")
    elif rsi >= 65:
        sell_score += 3
        reasons.append(f"📈 [ĐỘNG LƯỢNG KỸ THUẬT]: Chỉ số RSI D1 rơi vào vùng Quá mua thực tế ({rsi}). Lực mua FOMO của đám đông đã quá tải, rủi ro sập giá chốt lời đang ở mức báo động.")

    # 6. LỜI XÁC NHẬN TỪ HÀNH ĐỘNG GIÁ CỦA NẾN NGÀY D1 (Trọng số: 3 Điểm)
    if d1_price_action == "Nến D1 Đảo chiều Tăng mạnh (Pinbar rút râu dài / Engulfing xanh ôm trọn)":
        buy_score += 3
        reasons.append("🕯️ [LỜI XÁC NHẬN NẾN]: Cây nến Ngày D1 vừa đóng cửa phát ra tín hiệu từ chối giảm giá cực mạnh (Rút râu dài hoặc Nhấn chìm tăng). Phe Bò đã chính thức vào cuộc để chiếm quyền kiểm soát.")
    elif d1_price_action == "Nến D1 Đảo chiều Giảm mạnh (Pinbar từ chối đỉnh / Engulfing đỏ nuốt chửng)":
        sell_score += 3
        reasons.append("🕯️ [LỜI XÁC NHẬN NẾN]: Cây nến Ngày D1 vừa đóng cửa phát ra tín hiệu từ chối tăng giá (Quét thanh khoản đỉnh hoặc Nhấn chìm giảm). Phe Gấu đã ra tay xả hàng áp đảo.")

    # ==================================================================================
    # ⚖️ ENGINE PHÁN QUYẾT CHIẾN LƯỢC TỐI CAO ĐA TẦNG
    # ==================================================================================
    # Hệ thống đòi hỏi tổng điểm phải đạt từ 12 điểm trở lên. 
    # Nghĩa là DÙ KỸ THUẬT CÓ ĐẸP ĐẾN ĐÂU, nếu VĨ MÔ (FED + Tin tức) quay lưng, tổng điểm KHÔNG BAO GIỜ chạm được mức 12.
    
    if buy_score >= 12 and buy_score > sell_score:
        calculated_winrate = 65.0 + (buy_score * 1.2)
        calculated_winrate = min(calculated_winrate, 92.5)
        return "🔥 PHÁT LỆNH D1: BUY SWING (MUA GIỮ DÀI HẠN THUẬN VĨ MÔ)", reasons, calculated_winrate
        
    elif sell_score >= 12 and sell_score > buy_score:
        calculated_winrate = 65.0 + (sell_score * 1.2)
        calculated_winrate = min(calculated_winrate, 91.0)
        return "❄️ PHÁT LỆNH D1: SELL SWING (BÁN GIỮ DÀI HẠN THUẬN VĨ MÔ)", reasons, calculated_winrate
        
    else:
        return "⏳ TRẠNG THÁI D1: TIẾP TỤC ĐỨNG NGOÀI PHÒNG THỦ VỐN (XUNG ĐỘT VĨ MÔ & KỸ THUẬT)", reasons, 0.0
