// layout.js
import { AuthProvider } from './context/authContext';
import Navbar from './components/Navbar';
import './globals.css';

export const metadata = {
  title: 'Stock Dashboard',
  description: 'A dashboard for viewing stock data',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Navbar />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
