import { useEffect, useState } from "react";
import api from "../services/api";

export default function ModelUsageCard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/model/distribution")
            .then((response) => {
                setData(response.data);
                setError("");
            })
            .catch((err) => {
                console.error("ModelUsageCard failed:", err);
                setError("Failed to load model usage stats.");
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

    return (
        <div style={{
            border: "1px solid gray",
            padding: "20px",
            borderRadius: "10px"
        }}>
            <h2>Model Usage</h2>
            <p>qwen2.5-coder:3b: {data?.["qwen2.5-coder:3b"] ?? 0}</p>
            <p>qwen2.5-coder:7b: {data?.["qwen2.5-coder:7b"] ?? 0}</p>
        </div>
    );
}
