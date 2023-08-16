import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';

function Navbar() {
    return (
        <nav className="px-6 py-4 bg-[rgba(255,140,140,0.9)] text-white">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold">CI&E Data Platform</h1>
                <div className="flex space-x-4">
                    <Link href="/" className="hover:underline">
                        Home
                    </Link>
                    <Link href="/instructions" className="hover:underline">
                        Instructions
                    </Link>
                </div>
            </div>
        </nav>
    );
}

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Cornell Entrepreneurship & Innovations - Data Platform',
    description: 'Platform for Cornell Entrepreneurship & Innovations data collection and analysis'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <Navbar />
                {children}
            </body>
        </html>
    );
}
