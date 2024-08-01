export async function fetchDailyClosingPrice() {
    const res = await fetch('http://localhost:8000/techapp/api/daily-closing-price/');
    if (!res.ok) {
      throw new Error('Failed to fetch daily closing price data');
    }
    return res.json();
  }
  
  export async function fetchTopGainersLosers() {
    const res = await fetch('http://localhost:8000/techapp/api/top-gainers-losers/');
    if (!res.ok) {
      throw new Error('Failed to fetch top gainers and losers data');
    }
    return res.json();
  }
  
  export async function fetchPriceChangePercentage() {
    const res = await fetch('http://localhost:8000/techapp/api/price-change-percentage/');
    if (!res.ok) {
      throw new Error('Failed to fetch price change percentage data');
    }
    return res.json();
  }
  
  export async function fetchDailyStockData() {
    const res = await fetch('http://localhost:8000/techapp/api/daily-stock-data/');
    if (!res.ok) {
      throw new Error('Failed to fetch daily stock data');
    }
    return res.json();
  }
  