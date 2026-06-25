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
            <p>Predicted Class: {result.predicted_class}</p>
            <p>Workload Class: {result.workload_class}</p>
            <p>Latency: {result.latency_seconds}s</p>
            <p>Decision: {result.scheduler_decision}</p>
            <p>Reason: {result.scheduler_reason}</p>
        </div>
    );
}
