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
        <div className="dashboard-card">
            <h2>Prediction-Execution Alignment</h2>

            <h1>
                {stats.prediction_execution_alignment_percent ?? stats.accuracy_percent}%
            </h1>

            <p>
                Aligned: {stats.aligned_predictions ?? stats.correct_predictions}
            </p>

            <p>
                Total: {stats.total_predictions}
            </p>

            <p>
                Prediction-Execution Alignment
            </p>
        </div>
    );
}
