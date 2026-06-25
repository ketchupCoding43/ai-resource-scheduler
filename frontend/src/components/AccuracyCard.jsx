import { useEffect, useState } from "react";
import api from "../services/api";

export default function AccuracyCard() {

    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        api.get("/prediction/stats")
            .then((response) => {
                console.log("AccuracyCard response:", response.data);
                setStats(response.data);
                setError("");
            })
            .catch((err) => {
                console.error("AccuracyCard failed:", err);
                setError("Failed to load accuracy stats.");
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
        return <div>No accuracy data available.</div>;
    }

    return (
        <div style={{
            border: "1px solid gray",
            padding: "20px",
            borderRadius: "10px"
        }}>
            <h2>Prediction Accuracy</h2>

            <h1>
                {stats.accuracy_percent}%
            </h1>

            <p>
                Correct: {stats.correct_predictions}
            </p>

            <p>
                Total: {stats.total_predictions}
            </p>
        </div>
    );
}
