'use client';  // This line makes sure the component is rendered on the client side

import React, { useEffect, useState } from 'react';
import { fetchTopGainersLosers } from '../lib/api';

const TopGainersLosers = () => {
  const [data, setData] = useState({ top_gainers: [], top_losers: [] });

  useEffect(() => {
    fetchTopGainersLosers()
      .then(setData)
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Top Gainers and Losers</h2>
      <div className="flex space-x-4">
        <div className="w-1/2">
          <h3>Top Gainers</h3>
          <table className="min-w-full border">
            <thead>
              <tr>
                <th className="border p-2">Stock Name</th>
                <th className="border p-2">Change Percentage</th>
              </tr>
            </thead>
            <tbody>
              {data.top_gainers.map(item => (
                <tr key={item.symbol}>
                  <td className="border p-2">{item.symbol}</td>
                  <td className="border p-2">{item.change_percentage.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="w-1/2">
          <h3>Top Losers</h3>
          <table className="min-w-full border">
            <thead>
              <tr>
                <th className="border p-2">Stock Name</th>
                <th className="border p-2">Change Percentage</th>
              </tr>
            </thead>
            <tbody>
              {data.top_losers.map(item => (
                <tr key={item.symbol}>
                  <td className="border p-2">{item.symbol}</td>
                  <td className="border p-2">{item.change_percentage.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TopGainersLosers;
