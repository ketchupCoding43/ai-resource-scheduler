import { useEffect, useState } from "react";
import api from "../services/api";

export default function EscalationStatsCard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/scheduler/escalation/stats")
            .then((response) => setStats(response.data))
            .catch((err) => {
                console.error("EscalationStatsCard failed:", err);
                setError("Failed to load escalation stats.");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard-card">
            <h2>Escalation Stats</h2>
            <p>Total Requests: {stats?.total_requests ?? 0}</p>
            <p>Escalated Requests: {stats?.escalated_requests ?? 0}</p>
            <p>Draft Success Rate: {stats?.draft_success_rate_percent ?? 0}%</p>
            <p>Escalation Rate: {stats?.escalation_rate_percent ?? 0}%</p>
        </div>
    );
}
