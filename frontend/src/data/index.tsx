interface Message {
    text: string;
    sentBy: string;
    sentAt: Date;
    isChatOwner?: boolean;
  }
  
  const messages: Message[] = [
    {
      text: "How can I get temporary housing?",
      sentBy: "Yishuang",
      sentAt: new Date("2023-03-02T09:00:00Z"),
      isChatOwner: true
    },
    {
      text: "I'm sorry to hear you're in need of temporary housing. What happened?",
      sentBy: "London",
      sentAt: new Date("2023-03-02T09:01:00Z"),
      isChatOwner: false
    },
  ];
  
  export { messages, Message };
  