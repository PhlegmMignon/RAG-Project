"use client";

import React from "react";
import { useChatContext } from "@/context/ChatContext";
import ChatMessage from "./ChatMessage";
import Loading from "./Loading";

const ChatHistory: React.FC = () => {
  const { messages, loading } = useChatContext();

  return (
    <div className="flex flex-col flex-grow space-y-4 p-3 overflow-scroll">
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}

      {loading && <Loading />}
    </div>
  );
};

export default ChatHistory;
