import { useEffect, useState } from "react";
import api from "../services/api";

export default function PredictionEvaluationCard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        api.get("/prediction/evaluation")
            .then((response) => {
                setStats(response.data);
            })
            .catch((err) => {
                console.error("PredictionEvaluationCard failed:", err);
                setError("Failed to load prediction evaluation.");
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
            <h2>Prediction Evaluation</h2>
            <p>Accuracy: {stats?.accuracy}%</p>
            <p>Precision: {stats?.precision}%</p>
            <p>Recall: {stats?.recall}%</p>
            <p>Total Samples: {stats?.total_samples}</p>
        </div>
    );
}
