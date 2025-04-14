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
    <html lang="en" className="flex justify-center h-full w-full">
      <body
        className={`${inter.className} flex justify-center w-full overflow-hidden`}
      >
        <ChatProvider>
          <div className="flex justify-center w-5xl p-4 overflow-hidden">
            {children}
          </div>
        </ChatProvider>
      </body>
    </html>
  );
}
