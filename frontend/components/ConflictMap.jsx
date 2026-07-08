import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function ConflictMap({ conflictZones, goldReservesGeoJson }) {
  const styleGoldReserves = (feature) => {
    const reserve = feature.properties?.gold_tons || 0;
    return {
      fillColor: reserve > 5000 ? '#78350f' : reserve > 1000 ? '#b45309' : reserve > 200 ? '#f59e0b' : '#fef3c7',
      weight: 1, opacity: 1, color: '#475569', fillOpacity: 0.7
    };
  };

  return (
    <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 text-white">
      <h2 className="text-xl font-bold mb-4 text-red-500">Bản Đồ Địa Chính Trị & Dự Trữ Vàng Toàn Cầu</h2>
      <div className="h-[500px] w-full rounded-lg overflow-hidden">
        <MapContainer center={[20, 0]} zoom={2} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}://{z}/{x}/{y}{r}.png"
            attribution='&copy; OpenStreetMap'
          />
          {goldReservesGeoJson && (
            <GeoJSON data={goldReservesGeoJson} style={styleGoldReserves} />
          )}
          {conflictZones.map((zone) => (
            <Marker key={zone.id} position={[zone.lat, zone.lng]}>
              <Popup>
                <div className="text-slate-900">
                  <h4 className="font-bold text-red-600">{zone.title}</h4>
                  <p className="text-sm">{zone.description}</p>
                  <span className="text-xs text-slate-500">{zone.updatedAt}</span>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
