import { useEffect, useState } from "react";
import api from "../services/api";

export default function ContextStatsCard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/scheduler/context/stats")
            .then((response) => setStats(response.data))
            .catch((err) => {
                console.error("ContextStatsCard failed:", err);
                setError("Failed to load context stats.");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard-card">
            <h2>Context Stats</h2>
            <p>1024: {stats?.["1024"] ?? 0}</p>
            <p>2048: {stats?.["2048"] ?? 0}</p>
            <p>4096: {stats?.["4096"] ?? 0}</p>
        </div>
    );
}
