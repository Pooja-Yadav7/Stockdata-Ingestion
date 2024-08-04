"use client";

import Link from 'next/link';
import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.navbarBrand}>
        <Link href="/">Stock Dashboard</Link>
      </div>
      <ul className={styles.navbarLinks}>
        <li><Link href="/daily-closing-price">Daily Closing Price</Link></li>
        <li><Link href="/daily-stock-data">Daily Stock Data</Link></li>
        <li><Link href="/top-gainers-losers">Top Gainers/Losers</Link></li>
        <li><Link href="/price-change-percentage">Price Change Percentage</Link></li>
      </ul>
    </nav>
  );
}
