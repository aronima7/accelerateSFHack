import React from "react";
import "./globals.css";
import ChatHeader from "./ChatHeader";
import ChatContent from "./ChatContent";
import ChatInputBox from "./ChatInputBox";
import { Message } from "./data";
import { useGetMessages } from "./hooks/useGetMessages";
import { ArrowPathIcon } from "@heroicons/react/24/outline";

export const Chat = () => {
  const {
    messages: { data }
  } = useGetMessages();

  const [chatMessages, setChatMessages] = React.useState<Message[]>(data);

  const sendANewMessage = (message: Message) => {
    setChatMessages((prevMessages) => [...prevMessages, message]);
  };

  const resetChat = () => {
    setChatMessages(data);
  };

  return (
    <>
      <div className="max-w-xl mx-auto mt-32 ">
        <div className="flex flex-row justify-between items-center py-2">
          <p className="text-md text-white bg-black px-2 py-1 font-semibold animate-pulse">
            Ask SF
          </p>
          <button
            type="button"
            onClick={() => resetChat()}
            className="hover:bg-gray-100 rounded-full font-medium text-sm p-1.5 text-center inline-flex items-center"
          >
            <ArrowPathIcon className="text-gray-600 w-5 h-5" />
          </button>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg shadow relative">
          <ChatHeader name={"Chatting  with London"} numberOfMessages={chatMessages.length} />
          <ChatContent messages={chatMessages} />
          <ChatInputBox sendANewMessage={sendANewMessage} />
        </div>
      </div>
    </>
  )
}
