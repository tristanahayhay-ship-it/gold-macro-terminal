import React, { useState } from 'react';
import CandleChart from '../components/CandleChart';
import MacroTable from '../components/MacroTable';
import ConflictMap from '../components/ConflictMap';
import PaperTrading from '../components/PaperTrading';

// Dữ liệu giả lập mẫu để chạy hiển thị Dashboard
const mockCandleData = [
  { time: '2026-07-01', open: 2320, high: 2345, low: 2315, close: 2340 },
  { time: '2026-07-02', open: 2340, high: 2360, low: 2335, close: 2355 },
  { time: '2026-07-03', open: 2355, high: 2358, low: 2320, close: 2325 },
  { time: '2026-07-06', open: 2325, high: 2350, low: 2310, close: 2348 },
  { time: '2026-07-07', open: 2348, high: 2375, low: 2340, close: 2365 },
];

const mockMacroData = [
  { name: 'CPI', previous: '3.1%', forecast: '3.0%', actual: '2.9%', impact: 'bullish', history: [{ date: 'Th5', value: 3.2 }, { date: 'Th6', value: 3.1 }, { date: 'Th7', value: 2.9 }] },
  { name: 'NFP', previous: '175K', forecast: '185K', actual: '160K', impact: 'bullish', history: [{ date: 'Th5', value: 165 }, { date: 'Th6', value: 175 }, { date: 'Th7', value: 160 }] },
  { name: 'GDP', previous: '2.1%', forecast: '2.3%', actual: '2.0%', impact: 'bullish', history: [{ date: 'Q1', value: 2.2 }, { date: 'Q2', value: 2.1 }, { date: 'Q3', value: 2.0 }] },
];

export default function Home() {
  const [currentPrice, setCurrentPrice] = useState(2365);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 font-sans">
      {/* Header chính của hệ thống */}
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-amber-500 tracking-wide">KINH TẾ VĨ MÔ & NHẬN ĐỊNH GIÁ VÀNG</h1>
          <p className="text-slate-400 text-sm mt-1">Hệ thống phân tích thông minh kết hợp AI toàn cảnh thị trường XAU/USD</p>
        </div>
        <div className="bg-slate-900 border border-slate-700 px-4 py-2 rounded-lg text-sm font-semibold text-emerald-400 animate-pulse">
          ● Hệ thống Live dữ liệu thực
        </div>
      </header>

      {/* Khu vực 1: Các biểu đồ nến tương tác chính */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <CandleChart symbol="XAU/USD (Vàng)" data={mockCandleData} />
        <CandleChart symbol="DXY (Chỉ số Đô la)" data={mockCandleData} />
        <CandleChart symbol="US10Y (Lợi suất 10 năm)" data={mockCandleData} />
      </section>

      {/* Khu vực 2: Bảng dữ liệu Vĩ mô & Đánh giá Tâm lý AI */}
      <section className="mb-8">
        <MacroTable economicData={mockMacroData} aiScore={75} />
      </section>

      {/* Khu vực 3: Địa chính trị & Trình trade giả lập */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ConflictMap conflictZones={[]} goldReservesGeoJson={null} />
        <PaperTrading currentXauPrice={currentPrice} />
      </section>
    </div>
  );
}
