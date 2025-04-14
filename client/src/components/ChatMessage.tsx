"use client";
import React from "react";
import { TMessage } from "@/context/ChatContext";
import ReactMarkdown from "react-markdown";

const ChatMessage: React.FC<{ message: TMessage }> = ({ message }) => {
  return (
    <div
      className={`flex items-start mb-4 ${
        message.role === "user" ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`p-3 max-w-xs rounded-lg ${
          message.role === "user" ? "bg-blue-500 text-white" : "bg-gray-800"
        }`}
      >
        <ReactMarkdown>{message.text}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ChatMessage;
