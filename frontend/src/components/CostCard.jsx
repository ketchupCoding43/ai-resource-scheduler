import { useEffect, useState } from "react";
import api from "../services/api";

export default function CostCard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/cost/stats")
            .then((response) => setStats(response.data))
            .catch((err) => {
                console.error("CostCard failed:", err);
                setError("Failed to load cost stats.");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard-card">
            <h2>Cost Optimization</h2>
            <p>Total Requests: {stats?.total_requests ?? 0}</p>
            <p>Actual Cost: {stats?.actual_cost ?? 0}</p>
            <p>Baseline Cost: {stats?.baseline_cost ?? 0}</p>
            <p>Savings %: {stats?.savings_percent ?? 0}%</p>
        </div>
    );
}
