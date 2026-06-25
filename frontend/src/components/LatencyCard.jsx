import { useEffect, useState } from "react";
import api from "../services/api";

export default function LatencyCard() {

    const [latency, setLatency] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        api.get("/latency/stats")
            .then((response) => {
                console.log("LatencyCard response:", response.data);
                setLatency(response.data);
                setError("");
            })
            .catch((err) => {
                console.error("LatencyCard failed:", err);
                setError("Failed to load latency stats.");
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

    if (!latency) {
        return <div>No latency data available.</div>;
    }

    return (
        <div style={{
            border: "1px solid gray",
            padding: "20px",
            borderRadius: "10px"
        }}>
            <h2>Average Latency</h2>

            <h1>
                {latency.average_latency_seconds}s
            </h1>
        </div>
    );
}
