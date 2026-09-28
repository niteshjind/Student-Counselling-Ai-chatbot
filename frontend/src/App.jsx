import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Namaste 🙏 I'm your Student Counselling AI Assistant. How can I help you today?",
    },
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text = message) => {
    if (!text.trim() || loading) return;

    const userMessage = text.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.reply },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Sorry, I couldn't connect to the server. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="chat-header">
        <div className="header-info">
          <div className="bot-avatar">🤖</div>

          <div>
            <h1>Student Counselling AI</h1>
            <p>
              <span className="online-dot"></span>
              Online • University Assistant
            </p>
          </div>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message-row ${msg.role}`}
            >
              {msg.role === "bot" && (
                <div className="small-avatar">🤖</div>
              )}

              <div className="message-bubble">
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <div className="small-avatar">🤖</div>

              <div className="message-bubble typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>

        <div className="suggestions">
          <p>Suggested questions</p>

          <div className="suggestion-buttons">
            <button onClick={() => sendMessage("What courses are available?")}>
              📚 Courses
            </button>

            <button onClick={() => sendMessage("What is the eligibility for B.Tech?")}>
              🎓 Eligibility
            </button>

            <button onClick={() => sendMessage("What is the fee structure?")}>
              💰 Fees
            </button>

            <button onClick={() => sendMessage("Tell me about admission process")}>
              📝 Admission
            </button>
          </div>
        </div>
      </main>

      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
          placeholder="Ask about courses, eligibility, fees..."
          disabled={loading}
        />

        <button
          className="send-button"
          onClick={() => sendMessage()}
          disabled={loading || !message.trim()}
        >
          ➤
        </button>
      </div>
    </div>
  );
}

export default App;