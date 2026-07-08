import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

export default function CandleChart({ symbol, data }) {
  const chartContainerRef = useRef();

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: { backgroundColor: '#131722', textColor: '#d1d4dc' },
      grid: { vertLines: { color: '#242a35' }, horzLines: { color: '#242a35' } },
      crosshair: { mode: 0 },
      priceScale: { borderColor: '#485c7b' },
      timeScale: { borderColor: '#485c7b', timeVisible: true },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a', downColor: '#ef5350',
      borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350',
    });

    candlestickSeries.setData(data);

    const handleResize = () => {
      chart.applyOptions({ width: chartContainerRef.current.clientWidth });
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data]);

  return (
    <div className="bg-slate-900 p-4 rounded-xl shadow-lg border border-slate-800">
      <h3 className="text-white font-bold mb-2 text-lg">Biểu đồ {symbol} (TradingView)</h3>
      <div ref={chartContainerRef} className="w-full" />
    </div>
  );
}
