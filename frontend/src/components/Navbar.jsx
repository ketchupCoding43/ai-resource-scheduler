export default function Navbar({ currentRoute, onNavigate }) {
    const items = [
        { key: "#/dashboard", label: "Dashboard" },
        { key: "#/chat", label: "Chat" },
    ];

    return (
        <header className="topbar">
            <div className="topbar__brand">AI Resource Scheduler</div>
            <nav className="topbar__nav">
                {items.map((item) => (
                    <button
                        key={item.key}
                        type="button"
                        className={`topbar__link ${currentRoute === item.key ? "is-active" : ""}`}
                        onClick={() => onNavigate(item.key)}
                    >
                        {item.label}
                    </button>
                ))}
            </nav>
        </header>
    );
}
