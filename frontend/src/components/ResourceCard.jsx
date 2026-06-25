import { useEffect, useState } from "react";
import api from "../services/api";

export default function ResourceCard() {

    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        api.get("/resource/stats")
            .then((response) => {
                console.log("ResourceCard response:", response.data);
                setStats(response.data);
                setError("");
            })
            .catch((err) => {
                console.error("ResourceCard failed:", err);
                setError("Failed to load resource stats.");
            })
            .finally(() => {
                setLoading(false);
            });

    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!stats) {
        return <div>No resource data available.</div>;
    }

    return (
        <div className="dashboard-card">
            <h2>Resource Usage</h2>

            <p>CPU: {stats.average_cpu}%</p>
            <p>RAM: {stats.average_ram}%</p>
            <p>GPU: {stats.average_gpu}%</p>
        </div>
    );
}
