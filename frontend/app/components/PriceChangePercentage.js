'use client';  // This line makes sure the component is rendered on the client side

import React, { useEffect, useState } from 'react';
import { fetchPriceChangePercentage } from '../lib/api';

const PriceChangePercentage = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    fetchPriceChangePercentage()
      .then(setData)
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Price Change Percentage</h2>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Period</th>
            <th>Price Change Percentage</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(data).map(symbol => (
            Object.entries(data[symbol]).map(([period, percentage]) => (
              <tr key={`${symbol}-${period}`}>
                <td>{symbol}</td>
                <td>{period}</td>
                <td>{percentage !== null ? percentage.toFixed(2) : 'N/A'}%</td>
              </tr>
            ))
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceChangePercentage;
