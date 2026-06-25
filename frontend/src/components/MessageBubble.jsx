export default function MessageBubble({ role, content }) {
    const isUser = role === "user";

    return (
        <div
            style={{
                display: "flex",
                justifyContent: isUser ? "flex-end" : "flex-start",
                marginBottom: "12px"
            }}
        >
            <div
                style={{
                    maxWidth: "75%",
                    padding: "12px 14px",
                    borderRadius: "16px",
                    background: isUser ? "#1f2937" : "#f3f4f6",
                    color: isUser ? "#fff" : "#111827",
                    whiteSpace: "pre-wrap"
                }}
            >
                {content}
            </div>
        </div>
    );
}
