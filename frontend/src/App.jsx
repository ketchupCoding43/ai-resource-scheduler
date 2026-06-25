import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import ChatPage from "./pages/ChatPage";

function App() {
    const [route, setRoute] = useState(window.location.hash || "#/dashboard");

    useEffect(() => {
        const onHashChange = () => setRoute(window.location.hash || "#/dashboard");
        window.addEventListener("hashchange", onHashChange);
        return () => window.removeEventListener("hashchange", onHashChange);
    }, []);

    return (
        <div>
            <nav style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: "12px",
                padding: "16px 20px",
                borderBottom: "1px solid rgba(148, 163, 184, 0.25)",
                background: "rgba(255,255,255,0.72)",
                backdropFilter: "blur(12px)"
            }}>
                <div style={{ fontWeight: 800, letterSpacing: "0.02em" }}>
                    AI Resource Scheduler
                </div>
                <div style={{ display: "flex", gap: "10px" }}>
                    <a
                        href="#/dashboard"
                        style={{
                            textDecoration: "none",
                            padding: "10px 16px",
                            borderRadius: "999px",
                            border: route === "#/dashboard" ? "1px solid #4f46e5" : "1px solid rgba(148, 163, 184, 0.4)",
                            background: route === "#/dashboard" ? "#4f46e5" : "#fff",
                            color: route === "#/dashboard" ? "#fff" : "#0f172a",
                            fontWeight: 600,
                            boxShadow: route === "#/dashboard" ? "0 8px 20px rgba(79, 70, 229, 0.18)" : "none"
                        }}
                    >
                        Dashboard
                    </a>
                    <a
                        href="#/chat"
                        style={{
                            textDecoration: "none",
                            padding: "10px 16px",
                            borderRadius: "999px",
                            border: route === "#/chat" ? "1px solid #4f46e5" : "1px solid rgba(148, 163, 184, 0.4)",
                            background: route === "#/chat" ? "#4f46e5" : "#fff",
                            color: route === "#/chat" ? "#fff" : "#0f172a",
                            fontWeight: 600,
                            boxShadow: route === "#/chat" ? "0 8px 20px rgba(79, 70, 229, 0.18)" : "none"
                        }}
                    >
                        Chat
                    </a>
                </div>
            </nav>
            {route === "#/chat" ? <ChatPage /> : <Dashboard />}
        </div>
    );
}

export default App;
