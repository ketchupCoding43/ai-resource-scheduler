export default function SchedulerInfo({ result }) {
    if (!result) {
        return null;
    }

    return (
        <div
            style={{
                border: "1px solid #d1d5db",
                borderRadius: "16px",
                padding: "16px",
                background: "#fff"
            }}
        >
            <h3 style={{ marginTop: 0 }}>Scheduler Info</h3>
            <p>Selected Model: {result.selected_model || result.model_used}</p>
            <p>Final Model: {result.final_model || result.model_used}</p>
            <p>Escalated: {result.escalated ? "Yes" : "No"}</p>
            <p>Escalation Reason: {result.escalation_reason || "None"}</p>
            <p>Predicted Workload: {result.predicted_class} before execution</p>
            <p>Actual Workload: {result.actual_workload_class || result.workload_class}</p>
            <p>Confidence Score: {result.confidence ?? result.prediction_confidence ?? 0}%</p>
            <p>Confidence Class: {result.confidence_class || "N/A"}</p>
            <p>Context Size: {result.context_size || 2048}</p>
            <p>Routing Reason: {result.routing_reason || "N/A"}</p>
            <p>Final Decision: {result.scheduler_decision || "N/A"}</p>
            <p>Decision Reason: {result.decision_reason || result.scheduler_reason || "N/A"}</p>
            <p>Risk Level: {result.risk_level || "N/A"}</p>
            <p>Latency: {result.latency_seconds}s</p>
        </div>
    );
}
