import React, { useState } from 'react';

export default function PaperTrading({ currentXauPrice }) {
  const [balance, setBalance] = useState(100000); 
  const [position, setPosition] = useState(null); 

  const handleOrder = (type, volume) => {
    if (position) return alert("Bạn đang có một vị thế mở. Hãy đóng trước!");
    setPosition({ type, entryPrice: currentXauPrice, volume });
  };

  const handleClose = () => {
    if (!position) return;
    const pnl = position.type === 'BUY' 
      ? (currentXauPrice - position.entryPrice) * position.volume * 100
      : (position.entryPrice - currentXauPrice) * position.volume * 100;
    setBalance(prev => prev + pnl);
    setPosition(null);
    alert(`Lệnh đã đóng! P&L của bạn: ${pnl.toFixed(2)} USD`);
  };

  return (
    <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 text-white">
      <h2 className="text-xl font-bold mb-4 text-emerald-500">Giả Lập Giao Dịch XAU/USD</h2>
      <div className="flex justify-between mb-6 bg-slate-800 p-4 rounded-lg">
        <div><p className="text-slate-400 text-sm">Tài khoản Demo</p><p className="text-2xl font-mono text-amber-400">${balance.toLocaleString()}</p></div>
        <div><p className="text-slate-400 text-sm">Giá XAU hiện tại</p><p className="text-2xl font-mono text-emerald-400">${currentXauPrice}</p></div>
      </div>
      
      {!position ? (
        <div className="grid grid-cols-2 gap-4">
          <button onClick={() => handleOrder('BUY', 1)} className="bg-emerald-600 hover:bg-emerald-700 p-3 font-bold rounded-lg transition">MUA (BUY) 1 Lot</button>
          <button onClick={() => handleOrder('SELL', 1)} className="bg-red-600 hover:bg-red-700 p-3 font-bold rounded-lg transition">BÁN (SELL) 1 Lot</button>
        </div>
      ) : (
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-700">
          <div className="flex justify-between items-center mb-3">
            <span>Vị thế: <strong className={position.type === 'BUY' ? 'text-green-500' : 'text-red-500'}>{position.type}</strong> tại ${position.entryPrice}</span>
            <span className="font-mono text-lg">P&L: 
              <span className={((currentXauPrice - position.entryPrice) >= 0 ? 'text-green-500' : 'text-red-500')}>
                ${((position.type === 'BUY' ? (currentXauPrice - position.entryPrice) : (position.entryPrice - currentXauPrice)) * position.volume * 100).toFixed(2)}
              </span>
            </span>
          </div>
          <button onClick={handleClose} className="w-full bg-orange-600 hover:bg-orange-700 p-2 font-bold rounded">ĐÓNG VỊ THẾ BẰNG GIÁ THỊ TRƯỜNG</button>
        </div>
      )}
    </div>
  );
}
