"use client";
import React, { useState } from "react";
import { useChatContext, TMessage } from "@/context/ChatContext";

const InputBox: React.FC = () => {
  const [input, setInput] = useState("");
  const { setLoading, setResponse, setMessages } = useChatContext();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    //Prevents empty inputs
    if (!input.trim()) return;

    //Stores user message in conversation
    const userMessage: TMessage = {
      role: "user",
      text: input,
    };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    console.log("Submit sent" + { input });

    try {
      const res = await fetch("https://rag-project-xkv4.onrender.com", {
        // const res = await fetch("http://127.0.0.1:8000 ", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: input }),
      });

      const data = await res.json();
      setResponse(data);

      //Stores bot message in conversation
      const botMessage: TMessage = {
        role: "bot",
        text: data,
      };
      setMessages((prev) => [...prev, botMessage]);

      console.log("Response:", data);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className=" flex items-center space-between p-3 bg-gray-700 w-full min-h-[4rem] mt-auto rounded-[12px]">
      <form onSubmit={handleSubmit} className="flex items-center w-full">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className=" w-full text-left focus:outline-none "
          placeholder="Enter text here"
        />
        <button
          type="submit"
          className="ml-3 p-1 bg-blue-500 text-white rounded-[8px] hover:bg-blue-600 focus:outline-none"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default InputBox;
