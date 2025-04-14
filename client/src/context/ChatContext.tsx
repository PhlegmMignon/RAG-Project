"use client";
import { createContext, useContext, useState, ReactNode } from "react";

type TChatContext = {
  loading: boolean;
  setLoading: (value: boolean) => void;
  response: string;
  setResponse: (value: string) => void;
};

const ChatContext = createContext<TChatContext | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");

  return (
    <ChatContext.Provider
      value={{ loading, setLoading, response, setResponse }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = (): TChatContext => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChatContext must be used within a ChatProvider");
  }
  return context;
};
