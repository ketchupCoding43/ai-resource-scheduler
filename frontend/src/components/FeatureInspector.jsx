import { useState } from "react";
import api from "../services/api";

export default function FeatureInspector() {
    const [prompt, setPrompt] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const inspect = async () => {
        if (!prompt.trim()) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const response = await api.get("/prediction/features", {
                params: { prompt }
            });
            setResult(response.data);
        } catch (err) {
            console.error("FeatureInspector failed:", err);
            setError("Failed to inspect features.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            border: "1px solid gray",
            padding: "20px",
            borderRadius: "10px"
        }}>
            <h2>Feature Inspector</h2>
            <textarea
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter a prompt..."
                style={{ width: "100%", marginBottom: "12px" }}
            />
            <button onClick={inspect} disabled={loading}>
                {loading ? "Inspecting..." : "Inspect"}
            </button>

            {error && <p>{error}</p>}

            {result && (
                <div style={{ marginTop: "12px" }}>
                    <p>Technical Domain Matches: {(result.technical_domain_matches || []).join(", ") || "None"}</p>
                    <p>Complexity Term Matches: {(result.complexity_term_matches || []).join(", ") || "None"}</p>
                    <p>Semantic Score: {result.semantic_score}</p>
                    <p>Final Complexity Score: {result.complexity_score}</p>
                    <p>Predicted Workload: {result.predicted_workload}</p>
                    <p>Selected Model: {result.predicted_workload === "LIGHT" ? "qwen2.5-coder:3b" : "qwen2.5-coder:7b"}</p>
                </div>
            )}
        </div>
    );
}
