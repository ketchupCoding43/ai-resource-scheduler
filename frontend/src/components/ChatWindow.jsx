import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages }) {
    return (
        <div
            style={{
                minHeight: "320px",
                maxHeight: "520px",
                overflowY: "auto",
                padding: "16px",
                borderRadius: "16px",
                border: "1px solid #e5e7eb",
                background: "#fff"
            }}
        >
            {messages.map((message) => (
                <MessageBubble
                    key={message.id}
                    role={message.role}
                    content={message.content}
                />
            ))}
        </div>
    );
}
