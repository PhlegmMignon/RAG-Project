"use client";
import { createContext, useContext, useState, ReactNode } from "react";

export type TMessage = {
  role: "user" | "bot";
  text: string;
};

type TChatContext = {
  loading: boolean;
  setLoading: (value: boolean) => void;
  messages: TMessage[];
  setMessages: (
    messages: TMessage[] | ((prev: TMessage[]) => TMessage[])
  ) => void;
};

const ChatContext = createContext<TChatContext | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<TMessage[]>([]);

  return (
    <ChatContext.Provider
      value={{
        loading,
        setLoading,
        messages,
        setMessages,
      }}
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
