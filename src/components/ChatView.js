import React, { useState, useEffect } from "react";
import sendIcon from '../assets/images/send.png';
import deleteIcon from '../assets/images/delete.png';

const ChatView = ({ chat, onSendMessage }) => {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState(() => {
    // Get the chat history from localStorage if available, or default to empty array
    const savedChatHistory = localStorage.getItem("chatHistory");
    return savedChatHistory ? JSON.parse(savedChatHistory) : (chat ? chat.messages : []);
  });

  useEffect(() => {
    // Save chat history to localStorage whenever it changes
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleSendMessage = async () => {
    if (userInput.trim() === "") return;

    const newMessage = {
      sender: "user",
      text: userInput,
    };

    // Add user message to chat history
    setChatHistory((prevChat) => {
      const updatedChat = [...prevChat, newMessage];
      return updatedChat;
    });
    onSendMessage(newMessage); // Send message to parent (App.js)

    setUserInput(""); // Reset the input field

    // Make API call to fetch bot's response 
    try {
      const response = await fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userInput: userInput,
          chatHistory: chatHistory,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botResponse = {
          sender: "bot",
          text: data.response, // Response contains a 'response' field
        };

        // Add bot response to chat history
        setChatHistory((prevChat) => [...prevChat, botResponse]);
        onSendMessage(botResponse); // Send bot response to parent (App.js)
      } else {
        const botResponse = {
          sender: "bot",
          text: "Sorry, I couldn't process your request at the moment.",
        };

        // Add fallback response to chat history
        setChatHistory((prevChat) => [...prevChat, botResponse]);
        onSendMessage(botResponse); // Send bot response to parent (App.js)
      }
    } catch (error) {
      console.error("Error fetching bot response:", error);
      const botResponse = {
        sender: "bot",
        text: "Oops! Something went wrong. Please try again later.",
      };

      // Add error response to chat history
      setChatHistory((prevChat) => [...prevChat, botResponse]);
      onSendMessage(botResponse); // Send bot response to parent (App.js)
    }
  };

  const handleDeleteChat = () => {
    // Clear chat history from state and localStorage
    setChatHistory([]);
    localStorage.removeItem("chatHistory");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "87%",
        justifyContent: "space-between",
      }}
    >
      <div
        style={{
          maxHeight: "80vh",
          overflowY: "auto", // Enable scroll for the chat messages
          paddingBottom: "10px",
        }}
      >
        {chatHistory.map((message, index) => (
          <div key={index} style={{ marginBottom: "15px", lineHeight: "1.5" }}>
            <strong
              style={{
                color: message.sender === "user" ? "#4CAF50" : "#009688",
              }}
            >
              {message.sender === "user" ? "You" : "Bot"}:
            </strong>
            <p style={{ color: "#555", fontSize: "1em" }}>{message.text}</p>
          </div>
        ))}
      </div>

      {/* Textbox and send button container */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px",
          backgroundColor: "#fff",
          borderTop: "1px solid #ddd",
          borderRadius: "7px",
        }}
      >
        {/* Text area for user input */}
        <textarea
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Type your message..."
          rows="2"
          style={{
            width: "90%",
            padding: "12px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            boxSizing: "border-box",
            fontSize: "1em",
            fontFamily: "Arial, sans-serif",
            resize: "none",
          }}
        ></textarea>

        {/* Image button for sending message */}
        <div
          onClick={handleSendMessage}
          style={{
            width: "50px",
            height: "50px",
            backgroundImage: `url(${sendIcon})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            borderRadius: "50%",
            cursor: "pointer",
            marginLeft: "10px",
          }}
        ></div>
        {/* Delete Chat Button */}
        <div
          onClick={handleDeleteChat}
          style={{
            width: "50px",
            height: "50px",
            backgroundImage: `url(${deleteIcon})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            borderRadius: "50%",
            cursor: "pointer",
            marginLeft: "10px",
          }}
        ></div>
      </div>

      
    </div>
  );
};

export default ChatView;
