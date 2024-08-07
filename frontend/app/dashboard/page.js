// dashboard/page.js
"use client";

import { useAuth } from "../context/authContext";
import DailyClosingPrice from "../components/DailyClosingPrice";
import DailyStockData from "../components/DailyStockData";
import PriceChangePercentage from "../components/PriceChangePercentage";
import TopGainersLosers from "../components/TopGainersLosers";

export default function DashboardPage() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <div>Please log in to view the dashboard.</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <DailyClosingPrice />
      <DailyStockData />
      <PriceChangePercentage />
      <TopGainersLosers />
    </div>
  );
}
