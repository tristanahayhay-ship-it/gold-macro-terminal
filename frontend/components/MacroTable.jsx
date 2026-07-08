import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function MacroTable({ economicData, aiScore }) {
  const [selectedIndicator, setSelectedIndicator] = useState('CPI');

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6 bg-slate-950 text-white rounded-xl border border-slate-800">
      <div className="lg:col-span-2 bg-slate-900 p-4 rounded-xl border border-slate-800">
        <h2 className="text-xl font-bold mb-4 text-amber-500">Dữ Liệu Kinh Tế Mỹ (Real-time)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-700 text-slate-400">
                <th className="p-3">Chỉ số</th>
                <th className="p-3">Kỳ trước</th>
                <th className="p-3">Dự báo</th>
                <th className="p-3">Thực tế</th>
              </tr>
            </thead>
            <tbody>
              {economicData.map((item) => (
                <tr 
                  key={item.name} 
                  className="border-b border-slate-800 hover:bg-slate-800 cursor-pointer transition"
                  onClick={() => setSelectedIndicator(item.name)}
                >
                  <td className="p-3 font-semibold">{item.name}</td>
                  <td className="p-3 text-slate-400">{item.previous}</td>
                  <td className="p-3 text-slate-400">{item.forecast}</td>
                  <td className={`p-3 font-bold ${item.impact === 'bullish' ? 'text-green-500' : 'text-red-500'}`}>
                    {item.actual}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="space-y-6">
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <h3 className="font-bold mb-3">Lịch sử kỳ điều chỉnh: {selectedIndicator}</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={economicData.find(i => i.name === selectedIndicator)?.history || []}>
                <XAxis dataKey="date" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none' }} />
                <Bar dataKey="value" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 text-center">
          <h3 className="font-bold mb-2">Chấm điểm xu hướng Vàng từ AI</h3>
          <div className="w-full bg-slate-800 h-6 rounded-full overflow-hidden relative">
            <div className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 transition-all duration-500" style={{ width: `${aiScore}%` }} />
          </div>
          <div className="flex justify-between text-xs mt-2 text-slate-400">
            <span>Bearish (0)</span>
            <span className="text-amber-400 font-bold text-lg">{aiScore}/100</span>
            <span>Bullish (100)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
