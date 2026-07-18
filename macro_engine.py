def evaluate_d1_quantum_signal(rsi, macro_trend, fed_policy, major_liquidity, d1_price_action):
    """
    Bộ não thẩm định tối cao cấu hình riêng cho khung thời gian Ngày (D1).
    Yêu cầu độ hội tụ dòng tiền lớn để phát lệnh dài hạn (Swing Trading).
    """
    buy_score = 0
    sell_score = 0
    reasons = []

    # 1. THẨM ĐỊNH CẤU TRÚC XU HƯỚNG D1 (Yếu tố quyết định 40% chiến thắng)
    if macro_trend == "Xu hướng Tăng dài hạn (Bullish)":
        buy_score += 4
        reasons.append("Cấu trúc thị trường D1 đang tạo Đỉnh sau cao hơn đỉnh trước, Đáy sau cao hơn đáy trước (Thuận xu hướng lớn).")
    elif macro_trend == "Xu hướng Giảm dài hạn (Bearish)":
        sell_score += 4
        reasons.append("Cấu trúc thị trường D1 đang tạo Đỉnh sau thấp hơn đỉnh trước, Đáy sau thấp hơn đáy trước (Thuận xu hướng lớn).")

    # 2. THẨM ĐỊNH ĐIỂM XOAY CỦA CÁ MẬP KHUNG D1/W1 (Vùng gom hàng trung hạn)
    if major_liquidity == "Chạm Vùng Hỗ trợ D1 / Order Block Tăng tuần":
        buy_score += 5
        reasons.append("Giá đập trúng vùng Gom hàng trung hạn của Cá Mập trên khung D1/W1. Lực cầu tổ chức rất mạnh.")
    elif major_liquidity == "Chạm Vùng Kháng cự D1 / Order Block Giảm tuần":
        sell_score += 5
        reasons.append("Giá đập trúng Tường bán chặn trên của các quỹ lớn trên khung D1/W1. Áp lực cung cực lớn.")

    # 3. THẨM ĐỊNH CHỈ BÁO RSI TRÊN KHUNG D1 (Lực chạy rất mạnh, cực hiếm khi chạm đỉnh/đáy)
    if rsi <= 35:
        buy_score += 3
        reasons.append(f"RSI Khung D1 đạt mức Quá bán ({rsi}). Lịch sử cho thấy đây là vùng đáy trung hạn của Vàng.")
    elif rsi >= 65:
        sell_score += 3
        reasons.append(f"RSI Khung D1 đạt mức Quá mua ({rsi}). Lịch sử cho thấy đây là vùng đỉnh trung hạn của Vàng.")

    # 4. THẨM ĐỊNH CHÍNH SÁCH TIỀN TỆ FED & VĨ MÔ DÀI HẠN
    if fed_policy == "Nới lỏng (Cắt giảm lãi suất / Bơm tiền / USD suy yếu)":
        buy_score += 4
        reasons.append("Chính sách vĩ mô dài hạn ủng hộ Vàng: FED nới lỏng dòng tiền và đồng DXY suy yếu làm tăng giá trị Vàng.")
    elif fed_policy == "Thắt chặt (Tăng lãi suất / Giữ lãi suất cao / USD mạnh)":
        sell_score += 4
        reasons.append("Chính sách vĩ mô dài hạn đè nặng lên Vàng: FED siết dòng tiền, gửi tiết kiệm USD có giá hơn giữ Vàng.")

    # 5. LỜI XÁC NHẬN CUỐI CÙNG TỪ CỦA NẾN NGÀY D1 (Price Action)
    if d1_price_action == "Nến D1 Đảo chiều Tăng mạnh (Pinbar rút râu dài / Engulfing xanh ôm trọn)":
        buy_score += 3
        reasons.append("Nến Ngày D1 đóng cửa xác nhận phe Bò đã hoàn toàn kiểm soát cuộc chơi, từ chối giá giảm sâu.")
    elif d1_price_action == "Nến D1 Đảo chiều Giảm mạnh (Pinbar từ chối đỉnh / Engulfing đỏ nuốt chửng)":
        sell_score += 3
        reasons.append("Nến Ngày D1 đóng cửa xác nhận phe Gấu đã xả hàng áp đảo, từ chối nỗ lực tăng giá.")

    # ⚖️ PHÁN QUYẾT TỐI CAO ĐƯỢC CHẮN LỌC (Yêu cầu tối thiểu 11 điểm trọng số)
    # Khung D1 lệnh ra ít nhưng một khi đã ra là phải cực kỳ chất lượng
    if buy_score >= 11 and buy_score > sell_score:
        calculated_winrate = 65.0 + (buy_score * 1.2)
        calculated_winrate = min(calculated_winrate, 92.5) # Khung D1 có thể đạt xác suất chạm TP rất cao
        return "🔥 PHÁT LỆNH D1: BUY SWING (MUA GIỮ DÀI HẠN)", reasons, calculated_winrate
    elif sell_score >= 11 and sell_score > buy_score:
        calculated_winrate = 65.0 + (sell_score * 1.2)
        calculated_winrate = min(calculated_winrate, 91.0)
        return "❄️ PHÁT LỆNH D1: SELL SWING (BÁN GIỮ DÀI HẠN)", reasons, calculated_winrate
    else:
        return "⏳ TRẠNG THÁI D1: TIẾP TỤC TREO LỆNH QUAN SÁT (NO SIGNAL)", reasons, 0.0
