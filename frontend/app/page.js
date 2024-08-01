// Mark this file as a Client Component
"use client";

import { useState } from 'react';
import DailyClosingPrice from './components/DailyClosingPrice';
import DailyStockData from './components/DailyStockData';
import TopGainersLosers from './components/TopGainersLosers';
import PriceChangePercentage from './components/PriceChangePercentage';

export default function HomePage() {
  const [visible, setVisible] = useState({
    dailyClosingPrice: false,
    dailyStockData: false,
    topGainersLosers: false,
    priceChangePercentage: false,
  });

  const toggleVisibility = (view) => {
    setVisible((prev) => ({ ...prev, [view]: !prev[view] }));
  };

  return (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <button onClick={() => toggleVisibility('dailyClosingPrice')}>Toggle Daily Closing Price</button>
        <button onClick={() => toggleVisibility('dailyStockData')}>Toggle Daily Stock Data</button>
        <button onClick={() => toggleVisibility('topGainersLosers')}>Toggle Top Gainers/Losers</button>
        <button onClick={() => toggleVisibility('priceChangePercentage')}>Toggle Price Change Percentage</button>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', padding: '16px' }}>
        {visible.dailyClosingPrice && (
          <div style={{ flex: '1 1 300px', minWidth: '300px' }}>
            <DailyClosingPrice />
          </div>
        )}
        {visible.dailyStockData && (
          <div style={{ flex: '1 1 300px', minWidth: '300px' }}>
            <DailyStockData />
          </div>
        )}
        {visible.topGainersLosers && (
          <div style={{ flex: '1 1 300px', minWidth: '300px' }}>
            <TopGainersLosers />
          </div>
        )}
        {visible.priceChangePercentage && (
          <div style={{ flex: '1 1 300px', minWidth: '300px' }}>
            <PriceChangePercentage />
          </div>
        )}
      </div>
    </div>
  );
}
