import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Youth",
  description: "Youth platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="m-0 bg-white font-sans antialiased" suppressHydrationWarning>{children}</body>
    </html>
  );
}
