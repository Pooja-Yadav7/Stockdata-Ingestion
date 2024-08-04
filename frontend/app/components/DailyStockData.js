'use client';  // This line makes sure the component is rendered on the client side

import React, { useEffect, useState } from 'react';
import { fetchDailyStockData } from '../lib/api';

const DailyStockData = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchDailyStockData()
      .then(setData)
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Daily Stock Data</h2>
      <table>
        <thead>
          <tr>
            <th>Stock Name</th>
            <th>Date</th>
            <th>High</th>
            <th>Low</th>
            <th>Open</th>
            <th>Close</th>
            <th>Volume</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.symbol}</td>
              <td>{item.date}</td>
              <td>{item.high}</td>
              <td>{item.low}</td>
              <td>{item.open}</td>
              <td>{item.close}</td>
              <td>{item.volume}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DailyStockData;
