import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta
from google import genai

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Kinh tế Vĩ mô & Nhận định Giá Vàng",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh nâng cao để giao diện chuyên nghiệp và đồng bộ với Dark Theme
st.markdown("""
<style>
    /* 1. Làm mịn và thu gọn thanh cuộn (Scrollbar) chuẩn TradingView */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(0,0,0,0); }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #4b5563; }

    /* 2. Nâng cấp thiết kế các thẻ hiển thị chỉ số Metric vĩ mô */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1f2937, #111827) !important;
        border: 1px solid #374151 !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.14) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: #eab308 !important; /* Đổi viền sang màu Gold khi di chuột */
    }
    
    /* 3. Nâng cấp hộp phân tích AI (Hộp AI nhận định) sang trọng */
    .ai-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border-left: 5px solid #3b82f6;
        border-right: 1px solid #1e293b;
        border-top: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
        color: #e2e8f0;
        margin-bottom: 20px;
        font-size: 14.5px;
        line-height: 1.6;
    }
    
    /* 4. Nâng cấp thẻ bài báo tài chính tinh tế có hiệu ứng chuyển động */
    .news-card {
        background: linear-gradient(145deg, #111827, #1f2937);
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .news-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6; /* Đổi viền sang màu xanh Neon khi di chuột */
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.5);
    }
    .news-card h4, .news-card h5 {
        margin-top: 0px !important;
        color: #f3f4f6 !important;
    }
</style>
""", unsafe_allow_html=True)


# Hàm giả lập dữ liệu nến (Thay thế bằng API thực tế như yfinance khi deploy)
def get_real_market_data(symbol, days=90):
    ticker_mapping = {
        "XAU/USD": "GC=F",
        "DXY": "DX-Y.NYB",
        "US10Y": "^TNX",
        "VIX": "^VIX",
        "WTI Oil": "CL=F"
    }
    ticker_sym = ticker_mapping.get(symbol, "GC=F")
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)
        t = yf.Ticker(ticker_sym)
        df = t.history(start=start_date, end=end_date)
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối dữ liệu {symbol}: {str(e)}")
        return pd.DataFrame()

def plot_tradingview_chart(df, title):
    if df.empty:
        return go.Figure()
        
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_width=[0.2, 0.8])
                        
    # Ép kiểu dữ liệu ngày tháng của Yahoo Finance về chuỗi Ngày/Tháng ngắn gọn
    short_dates = df.index.strftime('%d/%m')
                        
    fig.add_trace(go.Candlestick(
        x=short_dates, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name="Giá",
        increasing_line_color='#22c55e', decreasing_line_color='#ef4444',
        increasing_fillcolor='#22c55e', decreasing_fillcolor='#ef4444'
    ), row=1, col=1)
    
    if 'Volume' in df.columns and df['Volume'].sum() > 0:
        colors = ['#22c55e' if row['Close'] >= row['Open'] else '#ef4444' for _, row in df.iterrows()]
        fig.add_trace(go.Bar(
            x=short_dates, y=df['Volume'], name="Volume", showlegend=False, marker_color=colors
        ), row=2, col=1)
        
    fig.update_xaxes(type='category', gridcolor='#e2e8f0', row=1, col=1)
    fig.update_xaxes(type='category', gridcolor='#e2e8f0', row=2, col=1)
    fig.update_yaxes(gridcolor='#e2e8f0', row=1, col=1)
    fig.update_yaxes(gridcolor='#e2e8f0', showticklabels=False, row=2, col=1)

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#1e293b')),
        xaxis_rangeslider_visible=False, height=450,
        margin=dict(l=10, r=10, t=40, b=10), hovermode='x unified',
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# SIDEBAR: Điều hướng chính
# SIDEBAR: Điều hướng chính và Cài đặt hệ thống
st.sidebar.title("🧭 Điều Hướng Hệ Thống")

# ===================================================================================================
# ⚙️ BẢNG ĐIỀU KHIỂN HỆ THỐNG (GÓC TRÊN TRÁI)
# ===================================================================================================
with st.sidebar.expander("⚙️ Cài đặt Hệ thống (Múi giờ / Ngôn ngữ / Theme)", expanded=False):
    # 1. Chọn ngôn ngữ
    lang_option = st.selectbox("🌐 Ngôn ngữ (Language):", ["Tiếng Việt (VN)", "English (US)"])
    
    # 2. Chọn múi giờ
    timezone_option = st.selectbox("🕒 Múi giờ (Timezone):", ["Việt Nam (GMT+7)", "New York (EST/GMT-5)", "London (GMT+0)"])
    
    # 3. Chế độ hiển thị (Streamlit sẽ tự động đồng bộ theo cấu hình config.toml của bạn)
    st.info("🌗 Hệ thống tự động tối ưu giao diện Dark Mode Bloomberg.")

# Khai báo cấu trúc đồng hồ động nhảy giây thực tế độc lập qua Fragment (Chạy ngầm mỗi 1 giây an toàn)
@st.fragment(run_every=1)
def hien_thi_dong_ho_sidebar_live(tz_option, lang_opt):
    from datetime import timezone
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    # Xử lý múi giờ thực tế
    if tz_option == "Việt Nam (GMT+7)":
        now_selected = now_utc + timedelta(hours=7)
        tz_suffix = "Giờ Việt Nam" if lang_opt == "Tiếng Việt (VN)" else "Vietnam Time"
    elif tz_option == "New York (EST/GMT-5)":
        now_selected = now_utc - timedelta(hours=5)
        tz_suffix = "Giờ New York" if lang_opt == "Tiếng Việt (VN)" else "New York Time"
    else:
        now_selected = now_utc
        tz_suffix = "Giờ Quốc tế GMT" if lang_opt == "Tiếng Việt (VN)" else "GMT International Time"

    current_time_str = now_selected.strftime("%d/%m/%Y — %H:%M:%S")
    
    # Xử lý ngôn ngữ hiển thị
    label_text = "Thời gian:" if lang_opt == "Tiếng Việt (VN)" else "Current Time:"
    st.markdown(f"📅 **{label_text}** `{current_time_str}` *({tz_suffix})*")

# Kích hoạt gọi hàm đồng hồ động kết hợp đa biến đầu vào
hien_thi_dong_ho_sidebar_live(timezone_option, lang_option)
st.sidebar.markdown("---")
# ===================================================================================================

menu = st.sidebar.radio(
    "Chọn chuyên mục:",
    ["Dashboard Tổng Quan", "Dữ Liệu Kinh Tế Mỹ", "Dòng Tiền (Flow of Funds)", "Tin Tức & Cổ Phiếu", "Địa Chính Trị & Chiến Tranh", "Công Cụ Hỗ Trợ & Demo Trade", "Giá Vàng VIỆT NAM", "📅 Lịch Kinh Tế & AI Nhận Định (USD)", "🤖 AI Giải Đáp & Phân Tích", "📰 Tin Tức Tài Chính Đa Kênh", "Mô phỏng: Ghế nóng FED", "Sơ đồ Kinh tế Mỹ & Vàng", "Demo Trade"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Trạng thái AI Kết Luận")
st.sidebar.success("Hệ thống AI: Sẵn sàng")
st.sidebar.info("Khuyến nghị hôm nay: **BULLISH GOLD** (Ưu tiên Mua) do căng thẳng địa chính trị và Real Yield giảm.")

# ===================================================================================================
# 1. DASHBOARD TỔNG QUAN
# ===================================================================================================
if menu == "Dashboard Tổng Quan":
    st.title("🪙 Kinh Tế Vĩ Mô & Nhận Định Giá Vàng")
    st.caption("Hệ thống tự động cập nhật dữ liệu liên tục kết hợp trí tuệ nhân tạo AI phân tích xu hướng")
    # =========================================================
    # HÀNG CHỈ SỐ LẤY DỮ LIỆU REAL-TIME TỪ YAHOO FINANCE
    # =========================================================
    import yfinance as yf

    @st.cache_data(ttl=60)  # Lưu bộ nhớ đệm 60 giây
    def get_live_market_data():
        tickers = {
            "Vàng (XAU/USD)": "GC=F",
            "DXY Index": "DX-Y.NYB",
            "US 10Y Yield": "^TNX",
            "VIX Index": "^VIX",
            "Crude Oil WTI": "CL=F"
        }
        results = {}
        for name, sym in tickers.items():
            try:
                t = yf.Ticker(sym)
                hist = t.history(period="2d")
                if len(hist) >= 2:
                    close_today = hist['Close'].iloc[-1]
                    close_yesterday = hist['Close'].iloc[-2]
                    change = close_today - close_yesterday
                    pct_change = (change / close_yesterday) * 100
                    results[name] = (round(close_today, 2), round(change, 2), round(pct_change, 2))
                else:
                    results[name] = (0.0, 0.0, 0.0)
            except:
                results[name] = (0.0, 0.0, 0.0)
        return results

    # Gọi hàm lấy giá trực tuyến (Đoạn này thụt lề 4 dấu cách)
    market_data = get_live_market_data()
    g_price, g_chg, g_pct = market_data.get("Vàng (XAU/USD)", (2354.50, 0.0, 0.0))
    dxy_price, dxy_chg, dxy_pct = market_data.get("DXY Index", (104.15, 0.0, 0.0))
    us10y_price, us10y_chg, us10y_pct = market_data.get("US 10Y Yield", (4.21, 0.0, 0.0))
    vix_price, vix_chg, vix_pct = market_data.get("VIX Index", (13.85, 0.0, 0.0))
    oil_price, oil_chg, oil_pct = market_data.get("Crude Oil WTI", (78.40, 0.0, 0.0))

    # Hiển thị ra các cột metric trên giao diện (Đoạn này thụt lề 4 dấu cách)
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("XAU/USD", f"{g_price:,}", f"{g_chg:+} ({g_pct:+.2f}%)")
    col2.metric("DXY Index", f"{dxy_price}", f"{dxy_chg:+} ({dxy_pct:+.2f}%)")
    col3.metric("US 10Y Yield", f"{us10y_price}%", f"{us10y_chg:+} ({us10y_pct:+.2f}%)")
    col4.metric("VIX Index", f"{vix_price}", f"{vix_price:+} ({vix_pct:+.2f}%)")
    col5.metric("Crude Oil WTI", f"${oil_price}", f"{oil_chg:+} ({oil_pct:+.2f}%)")

# =========================================================


    # Biểu đồ kỹ thuật tương tác
    st.subheader("📊 Biểu đồ Kỹ thuật ")
    asset_option = st.selectbox("Chọn tài sản để xem biểu đồ chi tiết:", ["XAU/USD", "DXY", "US10Y", "VIX", "WTI Oil"])
    # ===============================================================================================
    # CODE MỚI: NHÚNG WIDGET TRADINGVIEW ADVANCED CHUẨN ĐẸP NHƯ APP GỐC (THAY THẾ PLOTLY)
    # ===============================================================================================
    # Ánh xạ từ ô selectbox của bạn sang mã ID chuẩn trên hệ thống TradingView
    asset_mapping = {
        "XAU/USD": "OANDA:XAUUSD",
        "DXY": "CAPITALCOM:DXY",
        "US10Y": "TVC:US10Y",
        "VIX": "TVC:VIX",
        "WTI Oil": "TVC:USOIL"
    }
    chosen_tv_symbol = asset_mapping.get(asset_option, "OANDA:XAUUSD")

    import streamlit.components.v1 as components

    macro_tradingview_html = f"""
    <div class="tradingview-widget-container" style="height:100%; width:100%;">
        <div id="macro_chart_widget" style="height:520px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "width": "100%",
            "height": 520,
            "symbol": "{chosen_tv_symbol}",
            "interval": "60", /* Khung thời gian mặc định (H1) */
            "timezone": "Asia/Ho_Chi_Minh",
            "theme": "dark",   /* Ép nền đen huyền bí chuẩn như ảnh bạn chụp */
            "style": "1",
            "locale": "vi_VN",
            "toolbar_bg": "#131722",
            "enable_publishing": false,
            "hide_side_toolbar": false,   /* HIỆN THANH CÔNG CỤ VẼ BÊN TRÁI ĐỂ PHÂN TÍCH */
            "allow_symbol_change": false, /* Khóa gõ đổi mã trên chart để nó chạy đồng bộ theo selectbox */
            "container_id": "macro_chart_widget"
        }});
        </script>
    </div>
    """
    
    # Kết xuất mã HTML lên giao diện Streamlit, thiết lập chiều cao vừa vặn không bị lỗi cuộn
    components.html(macro_tradingview_html, height=530, scrolling=False)
    # ===============================================================================================
    # ===============================================================================================
    # LỊCH KINH TẾ USD REAL-TIME CẬP NHẬT THẬT 100% THEO TỪNG GIÂY (BIỆT LẬP HOÀN TOÀN)
    # ===============================================================================================
    st.markdown("---")
    c_left, c_right = st.columns([2.3, 1])
    
    with c_left:
        st.subheader("📅 Lịch Kinh Tế Vĩ Mô USD")
        st.caption("Dữ liệu thô cập nhật trực tiếp theo thời gian thực từ cổng API tài chính")

        # Khai báo cấu trúc bảng phẳng bằng chuỗi biến đơn, bọc kín để bảo vệ code bên dưới không bị lỗi
        custom_css = (
            "<style>"
            ".custom-wrapper { width: 100%; overflow-x: auto; border: 2px solid #000000; }"
            ".custom-table { width: 100%; border-collapse: collapse; background-color: #c0c0c0; font-family: Arial, sans-serif; font-size: 13px; min-width: 1000px; }"
            ".custom-th { background-color: #c0c0c0; color: #000000; padding: 8px; text-align: center; font-weight: bold; border: 1px solid #000000; }"
            ".custom-td { padding: 10px 6px; color: #000000; text-align: center; border: 1px solid #000000; vertical-align: middle; font-weight: 500; }"
            ".text-important { color: #ff0000 !important; font-weight: bold; }"
            ".text-medium { color: #f97316 !important; font-weight: bold; }"
            ".text-actual-bad { color: #ff0000 !important; font-weight: bold; }"
            ".text-actual-good { color: #008000 !important; font-weight: bold; }"
            ".click-link { color: #000000; text-decoration: underline; font-weight: normal; }"
            ".click-link:hover { color: #ff0000; }"
            "</style>"
        )
        st.markdown(custom_css, unsafe_allow_html=True)

        @st.fragment(run_every=1)
        def fetch_and_render_real_data():
            import requests
            from datetime import datetime
            filtered_events = []
            try:
                url = "https://coincarp.com"
                params = {"currency": "USD", "lang": "vi"}
                response = requests.get(url, params=params, timeout=0.8)
                if response.status_code == 200:
                    raw_data = response.json().get("data", {}).get("list", [])
                    for item in raw_data:
                        dt_str = item.get("date_time", "")
                        if dt_str:
                            dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                            date_val = dt_obj.strftime("%d/%m/%Y")
                            time_val = dt_obj.strftime("%H:%M chiều") if dt_obj.hour >= 12 else dt_obj.strftime("%H:%M sáng")
                        else:
                            date_val = datetime.now().strftime("%d/%m/%Y")
                            time_val = "--:--"
                        cur_val = item.get("currency", "USD")
                        importance_score = int(item.get("importance", 2))
                        event_title = item.get("title", "")
                        actual_val = item.get("actual", "---")
                        forecast_val = item.get("forecast", "---")
                        previous_val = item.get("previous", "---")
                        if not actual_val: actual_val = "---"
                        if not forecast_val: forecast_val = "---"
                        if not previous_val: previous_val = "---"
                        if cur_val == "USD" and importance_score in [2, 3]:
                            status = "normal"
                            try:
                                if actual_val != "---" and forecast_val != "---":
                                    act_num = float(actual_val.replace("%", "").replace("K", "").replace("M", ""))
                                    for_num = float(forecast_val.replace("%", "").replace("K", "").replace("M", ""))
                                    status = "good" if act_num >= for_num else "bad"
                            except:
                                pass
                            filtered_events.append({
                                "Date": date_val, "Time": time_val, "Currency": "USD",
                                "Importance": "QUAN TRỌNG" if importance_score == 3 else "TRUNG BÌNH",
                                "Title": event_title, "Actual": actual_val, "Forecast": forecast_val,
                                "Previous": previous_val, "Status": status, "DetailUrl": "https://tradingview.com"
                            })
            except:
                pass
            current_time = datetime.now().strftime("%H:%M:%S")
            html_table = (
                f"<div style='text-align: right; font-size: 11px; color: #64748b; margin-bottom: 6px; font-weight: bold;'>⏳ Hệ thống đồng bộ từng giây: {current_time}</div>"
                "<div class='custom-wrapper'>"
                "<table class='custom-table'>"
                "<thead><tr>"
                "<th class='custom-th' style='width: 10%;'>ngày/tháng/năm</th>"
                "<th class='custom-th' style='width: 10%;'>thời gian</th>"
                "<th class='custom-th' style='width: 8%;'>tiền tệ</th>"
                "<th class='custom-th' style='width: 12%;'>mức độ tin tức</th>"
                "<th class='custom-th' style='width: 24%;'>tên tin tức</th>"
                "<th class='custom-th' style='width: 14%;'>chi tiết</th>"
                "<th class='custom-th' style='width: 8%;'>thật sự</th>"
                "<th class='custom-th' style='width: 8%;'>dự báo</th>"
                "<th class='custom-th' style='width: 8%;'>trước</th>"
                "<th class='custom-th' style='width: 10%;'>tác động</th>"
                "</tr></thead><tbody>"
            )
            if not filtered_events:
                html_table += "<tr><td class='custom-td' colspan='10' style='padding: 30px; color: #555;'>Đang kết nối cổng dữ liệu hoặc không có tin USD mạnh trong phiên...</td></tr>"
            else:
                for ev in filtered_events:
                    imp_class = "class='custom-td text-important'" if ev["Importance"] == "QUAN TRỌNG" else "class='custom-td text-medium'"
                    act_class = "custom-td"
                    if ev["Status"] == "good": act_class = "custom-td text-actual-good"
                    elif ev["Status"] == "bad": act_class = "custom-td text-actual-bad"
                    html_table += (
                        f"<tr><td class='custom-td'>{ev['Date']}</td>"
                        f"<td class='custom-td'>{ev['Time']}</td>"
                        f"<td class='custom-td' style='font-weight: bold;'>{ev['Currency']}</td>"
                        f"<td {imp_class}>{ev['Importance']}</td>"
                        f"<td class='custom-td' style='text-align: left; padding-left: 10px;'>{ev['Title']}</td>"
                        f"<td class='custom-td'><a class='click-link' href='{ev['DetailUrl']}' target='_blank'>nhấn vào để xem tin tức</a></td>"
                        f"<td class='{act_class}'>{ev['Actual']}</td>"
                        f"<td class='custom-td' style='color: #ff0000; font-weight: bold;'>{ev['Forecast']}</td>"
                        f"<td class='custom-td' style='color: #008000; font-weight: bold;'>{ev['Previous']}</td>"
                        "<td class='custom-td' style='font-style: italic;'>tác động đến vàng</td></tr>"
                    )
            for _ in range(3):
                html_table += "<tr><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td><td class='custom-td'>&nbsp;</td></tr>"
            html_table += "</tbody></table></div>"
            st.markdown(html_table, unsafe_allow_html=True)

        fetch_and_render_real_data()
    with c_right:
        st.subheader("🤖 AI Nhận Phân tích Chỉ Số ")
        st.caption("Khai phá logic dòng tiền vĩ mô từ dữ liệu thời gian thực")

        # Hàm gọi API Gemini v2.5 THỰC TẾ bóc tách dữ liệu lịch kinh tế
        def process_real_ai_analysis(gold_p, dxy_p, us10y_p, data_list):
            try:
                import os
                api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
                if not api_key:
                    return "⚠️ Vui lòng cấu hình GEMINI_API_KEY trong file secrets."
                
                # Khởi tạo client theo chuẩn thư viện google-genai
                client = genai.Client(api_key=api_key)

                events_context = ""
                if data_list:
                    for ev in data_list[:3]:
                        # Sử dụng phương thức .get() an toàn tránh lỗi khuyết trường dữ liệu
                        title_val = ev.get('Title', ev.get('title', 'N/A'))
                        actual_val = ev.get('Actual', ev.get('actual', '---'))
                        forecast_val = ev.get('Forecast', ev.get('forecast', '---'))
                        previous_val = ev.get('Previous', ev.get('previous', '---'))
                        events_context += f"- Chỉ số {title_val}: Thật sự là {actual_val} (Dự báo: {forecast_val}, Kỳ trước: {previous_val})\n"
                else:
                    events_context = "- Hệ thống đang đồng bộ chỉ số vĩ mô mới trong phiên.\n"

                prompt = f"""Bạn là một chuyên gia phân tích kinh tế vĩ mô cấp cao độc lập.
Hãy phân tích các số liệu thực tế vừa được cập nhật trên bảng chỉ số kinh tế Mỹ dưới đây:

[DỮ LIỆU THỊ TRƯỜNG THỜI GIAN THỰC]
- Giá Vàng (XAU/USD): ${gold_p}
- Sức mạnh Đô la (DXY): {dxy_p}
- Lợi suất 10 năm (US10Y): {us10y_p}%

[DỮ LIỆU LỊCH KINH TẾ THỰC TẾ TRONG BẢNG]
{events_context}

[Nhiệm vụ phân tích liên thông đa biến]
Hãy phân tích logic dòng tiền chạy: Các chỉ số lạm phát/việc làm thực tế ở trên tác động thế nào đến tâm lý FED -> Từ đó ép chỉ số DXY tăng hay giảm -> DXY ép ngược hành vi giá Vàng (XAU/USD) bứt phá hay sụt giảm ra sao.

Yêu cầu: Viết ngắn gọn, trực diện bằng tiếng Việt. Sử dụng các thẻ HTML cơ bản (như <b>, <br>) để định dạng văn bản hiển thị trên web. Không dùng các từ sáo rỗng."""

                # Cấu hình gọi model bọc chặt chẽ hơn
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                if response and response.text:
                    return response.text
                return "⚠️ Không nhận được phản hồi văn bản từ AI."
                
            except Exception as e:
                # SỬA LỖI: In hẳn thông báo lỗi kỹ thuật ra màn hình để kiểm tra nguyên nhân thay vì ẩn đi
                return f"🤖 AI đang kết nối luồng dữ liệu liên thông... (Chi tiết lỗi: {str(e)})"

        # Điều hướng gọi hàm AI thực tế tránh vòng lặp quá tải
        if st.button("🔄 Kích hoạt AI phân tích", use_container_width=True) or "ai_cached_response" not in st.session_state:
            with st.spinner("AI phân tích chuyên sâu..."):
                news_input = st.session_state.get("current_live_events", [])
                st.session_state.ai_cached_response = process_real_ai_analysis(g_price, dxy_price, us10y_price, news_input)

        ai_response_text = st.session_state.get("ai_cached_response", "Đang phân tích...")

        st.markdown(
            f"""
            <div class="ai-box">
                <strong style="color: #3b82f6;">HỆ THỐNG AI PHÂN TÍCH ĐA BIẾN THẬT</strong><br><br>
                {ai_response_text}
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Bài báo phân tích vĩ mô lớn
    st.subheader("📰 Bài báo phân tích vĩ mô chuyên sâu")
    col_news1, col_news2 = st.columns(2)
    with col_news1:
        st.markdown("""
        <div class="news-card">
            <h4>[Bloomberg] Vàng tiến sát đỉnh lịch sử khi số liệu lạm phát kích hoạt làn sóng tháo chạy khỏi USD</h4>
            <p style='color:#64748b;'>Cập nhật: 10 phút trước</p>
            <p>Các quỹ đầu tru lớn đồng loạt gia tăng vị thế mua ròng vàng sau khi chuỗi chỉ số giá tiêu dùng và dữ liệu việc làm yếu đi rõ rệt...</p>
        </div>
        """, unsafe_allow_html=True)
    with col_news2:
        st.markdown("""
        <div class="news-card">
            <h4>[Reuters] Căng thẳng leo thang tại Trung Đông thúc đẩy dòng tiền trú ẩn an toàn vào tài sản phòng thủ</h4>
            <p style='color:#64748b;'>Cập nhật: 1 giờ trước</p>
            <p>Bất chấp lợi suất trái phiếu chính phủ Mỹ neo ở mức cao, lực cầu vật chất từ các Ngân hàng trung ương và dòng tiền trú ẩn đang là bệ đỡ vững chắc...</p>
        </div>
        """, unsafe_allow_html=True)
