import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import ChatView from "./components/ChatView";

const App = () => {
  const [currentChat, setCurrentChat] = useState(null); // Store the current chat

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Title at the top-left */}
      <div style={{ backgroundColor: "#333", padding: "20px" }}>
        <h1 style={{ color: "#8CE069", fontSize: "2em", fontWeight: "600" }}>Chatbot</h1>
      </div>

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Left panel for file upload */}
        <div style={{ width: "30%", padding: "20px", borderRight: "1px solid #ddd" }}>
          <h2 style={{ color: "#333", fontWeight: "500" }}>Upload Documents</h2>
          <FileUpload onFileUpload={(newConversation) => setCurrentChat(newConversation)} />
        </div>

        {/* Right panel for displaying the current chat */}
        <div
          style={{
            width: "70%",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            backgroundColor: "#f9f9f9",
            boxShadow: "inset 0 0 10px rgba(0, 0, 0, 0.1)",
          }}
        >
          {/* Conversation area above the text box */}
          <div style={{ flex: 1, overflowY: "auto", paddingRight: "10px", marginBottom: "20px" }}>
            <h2 style={{ color: "#333", fontWeight: "500" }}>Chat</h2>
            <ChatView
              chat={currentChat}
              onSendMessage={(message) => {
                setCurrentChat((prev) => ({
                  ...prev,
                  messages: prev ? [...prev.messages, message] : [message],
                }));
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
