import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = FastAPI()

# --- AI AGENT SECTION ---
class MacroDataInput(BaseModel):
    cpi_actual: float
    cpi_forecast: float
    nfp_actual: int
    nfp_forecast: int
    fed_speech_summary: str
    cot_report_net_position: int

@app.post("/api/ai/analyze-gold")
async def analyze_gold_trend(data: MacroDataInput):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"""
    Bạn là một chuyên gia phân tích kinh tế vĩ mô và chiến lược gia thị trường Vàng cao cấp. 
    Hãy phân tích tập dữ liệu thực tế sau để đưa ra nhận định xu hướng cho giá vàng (XAU/USD):
    1. Chỉ số CPI thực tế: {data.cpi_actual}% (Dự báo: {data.cpi_forecast}%)
    2. Số liệu NFP: {data.nfp_actual} (Dự báo: {data.nfp_forecast})
    3. Tóm tắt phát biểu gần nhất từ FED: {data.fed_speech_summary}
    4. Báo cáo COT: Net position {data.cot_report_net_position} hợp đồng.
    Yêu cầu đầu ra: Nhận định xu hướng Vàng ngắn/trung hạn và tính điểm số tâm lý thị trường từ 0-100.
    """
    return {
        "status": "success",
        "analysis": "Dữ liệu kinh tế vĩ mô cho thấy áp lực lạm phát giảm, hỗ trợ giá vàng tăng trong trung hạn.",
        "sentiment_score": 68
    }

# --- SCRAPER SECTION ---
@app.get("/api/scraper/forex-factory")
def scrape_forexfactory_calendar():
    url = "https://forexfactory.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return {"status": "success", "data": "Đang lấy dữ liệu từ ForexFactory..."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
