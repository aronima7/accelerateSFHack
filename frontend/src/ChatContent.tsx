import React from "react";
import { Message } from "./data";
import {} from "./hooks/messages-transform.types";
import AvatarAnon from "./AvatarAnon";
import AvatarLondon from "./AvatarLondon";

interface ChatContentProps {
  messages: Message[];
}

const ChatContent = ({ messages }: ChatContentProps) => {
  return (
    <div className="h-96 px-6 py-1 overflow-auto">
      {messages.map((message: Message, index: number) => (
        <div
          key={index}
          className={`py-2 flex flex-row w-full ${
            message.isChatOwner ? "justify-end" : "justify-start"
          }`}
        >
        <div className={`${message.isChatOwner ? "order-2" : "order-1"}`}>
          {message.isChatOwner ? <AvatarAnon /> : <AvatarLondon />}
        </div>

          <div
            className={`px-2 w-fit py-3 flex flex-col ${message.isChatOwner ? "bg-orange-600 order-1 mr-2 bg-opacity-70" : "bg-blue-900 order-2 ml-2 bg-opacity-70"} rounded-lg text-white ${
              message.isChatOwner ? "order-1 mr-2" : "order-2 ml-2"
            }`}
          >
            <span className="text-xs text-gray-200">
              {message.sentBy}&nbsp;-&nbsp;
              {new Date(message.sentAt).toLocaleTimeString("en-US", {
                hour: "2-digit",
                minute: "2-digit"
              })}
            </span>
            <span className="text-md">{message.text}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatContent;
