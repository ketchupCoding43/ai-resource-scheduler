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
            <nav style={{ display: "flex", gap: "12px", padding: "16px 20px" }}>
                <a href="#/dashboard">Dashboard</a>
                <a href="#/chat">Chat</a>
            </nav>
            {route === "#/chat" ? <ChatPage /> : <Dashboard />}
        </div>
    );
}

export default App;
