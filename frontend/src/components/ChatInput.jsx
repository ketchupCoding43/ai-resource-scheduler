import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
    const [value, setValue] = useState("");

    const submit = () => {
        const prompt = value.trim();
        if (!prompt || disabled) {
            return;
        }
        onSend(prompt);
        setValue("");
    };

    return (
        <div style={{ display: "flex", gap: "12px", marginTop: "16px" }}>
            <textarea
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        submit();
                    }
                }}
                placeholder="Ask something..."
                rows={3}
                disabled={disabled}
                style={{
                    flex: 1,
                    resize: "none",
                    padding: "12px",
                    borderRadius: "12px",
                    border: "1px solid #d1d5db"
                }}
            />
            <button
                type="button"
                onClick={submit}
                disabled={disabled}
                style={{
                    padding: "0 18px",
                    borderRadius: "12px",
                    border: "none",
                    background: "#111827",
                    color: "#fff",
                    cursor: "pointer"
                }}
            >
                Send
            </button>
        </div>
    );
}
