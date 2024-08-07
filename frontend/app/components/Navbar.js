// components/Navbar.js
"use client";

import Link from 'next/link';
import styles from './Navbar.module.css';
import { useAuth } from '../context/authContext';

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className={styles.navbar}>
      <div className={styles.navbarBrand}>
        <Link href="/">Stock Dashboard</Link>
      </div>
      <ul className={styles.navbarLinks}>
        {isAuthenticated ? (
          <>
            <li><Link href="/daily-closing-price">Daily Closing Price</Link></li>
            <li><Link href="/daily-stock-data">Daily Stock Data</Link></li>
            <li><Link href="/top-gainers-losers">Top Gainers/Losers</Link></li>
            <li><Link href="/price-change-percentage">Price Change Percentage</Link></li>
            <li><button onClick={logout}>Logout</button></li>
          </>
        ) : (
          <>
            <li><Link href="/login">Login</Link></li>
            <li><Link href="/signup">Signup</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
}
