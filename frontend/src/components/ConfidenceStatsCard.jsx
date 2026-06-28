import { useEffect, useState } from "react";
import api from "../services/api";

export default function ConfidenceStatsCard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/scheduler/confidence/stats")
            .then((response) => setStats(response.data))
            .catch((err) => {
                console.error("ConfidenceStatsCard failed:", err);
                setError("Failed to load confidence stats.");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard-card">
            <h2>Confidence Stats</h2>
            <p>Average Confidence: {stats?.average_confidence ?? 0}%</p>
            <p>High Confidence: {stats?.high_confidence ?? 0}</p>
            <p>Medium Confidence: {stats?.medium_confidence ?? 0}</p>
            <p>Low Confidence: {stats?.low_confidence ?? 0}</p>
        </div>
    );
}
