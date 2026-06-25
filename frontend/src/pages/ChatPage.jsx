import { useState } from "react";
import api from "../services/api";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import SchedulerInfo from "../components/SchedulerInfo";

export default function ChatPage() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            role: "assistant",
            content: "Send me a prompt and I’ll route it to the right model."
        }
    ]);
    const [loading, setLoading] = useState(false);
    const [schedulerResult, setSchedulerResult] = useState(null);

    const handleSend = async (prompt) => {
        const userMessage = {
            id: Date.now(),
            role: "user",
            content: prompt
        };

        setMessages((current) => [...current, userMessage]);
        setLoading(true);

        try {
            const response = await api.post("/llm/generate", { prompt });
            const data = response.data;

            setSchedulerResult(data);
            setMessages((current) => [
                ...current,
                {
                    id: Date.now() + 1,
                    role: "assistant",
                    content: data.response || `Scheduler decision: ${data.scheduler_decision}`
                }
            ]);
        } catch (error) {
            console.error("Chat request failed:", error);
            setMessages((current) => [
                ...current,
                {
                    id: Date.now() + 2,
                    role: "assistant",
                    content: "Sorry, the request failed. Check the backend console."
                }
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "24px", display: "grid", gap: "20px" }}>
            <div>
                <h1 style={{ marginBottom: "8px" }}>Chat</h1>
                <p style={{ marginTop: 0 }}>
                    Type a prompt and the scheduler will choose between 3b and 7b.
                </p>
            </div>

            <ChatWindow messages={messages} />
            <ChatInput onSend={handleSend} disabled={loading} />
            <SchedulerInfo result={schedulerResult} />
        </div>
    );
}
