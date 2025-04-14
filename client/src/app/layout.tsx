import { Inter } from "next/font/google";
import "./globals.css";
import { ChatProvider } from "@/context/ChatContext";

const inter = Inter({
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="flex justify-center h-full">
      <body className={`${inter.className} flex justify-center`}>
        <ChatProvider>
          <div className="flex justify-center max-w-5xl p-4">{children}</div>
        </ChatProvider>
      </body>
    </html>
  );
}
