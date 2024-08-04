'use client';  // This line ensures the component is rendered on the client side

import React, { useEffect, useState } from 'react';
import { fetchDailyClosingPrice } from '../lib/api';  // Adjusted path

const DailyClosingPrice = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchDailyClosingPrice()
      .then(setData)
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h2>Daily Closing Prices</h2>
      <table>
        <thead>
          <tr>
            <th>Stock Name</th>
            <th>Date</th>
            <th>Close</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.symbol}>
              <td>{item.symbol}</td>
              <td>{item.date}</td>
              <td>{item.close}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DailyClosingPrice;
