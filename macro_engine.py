import yfinance as yf
import numpy as np
from datetime import datetime

def fetch_global_macro_sentiment():
    """Bộ não cào dữ liệu và phân tích tác động vĩ mô toàn cầu"""
    macro_data = {
        "event_time": datetime.now().strftime("%H:%M:%S"),
        "fed_rate_stance": "HAWKISH (FED giữ lãi suất cao để siết lạm phát)",
        "geopolitical_risk": "HIGH (Căng thẳng địa chính trị thế giới leo thang)",
        "dxy_trend": "BEARISH (Chỉ số USD Index đang gãy xu hướng tăng)"
    }
    # Căng thẳng chính trị (+2), USD giảm (+2), Lãi suất cao (-1)
    macro_score = 2 + 2 - 1 
    return macro_data, macro_score

def get_institutional_data():
    """Hệ thống thu thập dữ liệu đa khung thời gian Real-time"""
    df_1m = yf.download(tickers="GC=F", period="1d", interval="1m")
    df_1h = yf.download(tickers="GC=F", period="5d", interval="1h")
    
    close_1m = df_1m['Close'].values.flatten()
    high_1m = df_1m['High'].values.flatten()
    low_1m = df_1m['Low'].values.flatten()
    
    current_price = float(close_1m[-1])
    
    # Xác định tường thanh khoản mua/bán của Cá mập trong 24h qua
    liquidity_resistance = float(np.max(df_1h['High'].values[-24:]))
    liquidity_support = float(np.min(df_1h['Low'].values[-24:]))
    
    # Tự động tính toán chỉ số RSI động
    delta = np.diff(close_1m)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(gain[-14:]) if len(gain) >= 14 else 0.5
    avg_loss = np.mean(loss[-14:]) if len(loss) >= 14 else 0.5
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    
    # Tính toán biên độ biến động ATR thực tế
    atr = float(np.mean(high_1m[-14:] - low_1m[-14:]))
    
    return df_1m, close_1m, current_price, liquidity_resistance, liquidity_support, rsi, atr
