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
      <div>
        <h3>Top Gainers</h3>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Change Percentage</th>
            </tr>
          </thead>
          <tbody>
            {data.top_gainers.map(item => (
              <tr key={item.symbol}>
                <td>{item.symbol}</td>
                <td>{item.change_percentage.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h3>Top Losers</h3>
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Change Percentage</th>
            </tr>
          </thead>
          <tbody>
            {data.top_losers.map(item => (
              <tr key={item.symbol}>
                <td>{item.symbol}</td>
                <td>{item.change_percentage.toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TopGainersLosers;
