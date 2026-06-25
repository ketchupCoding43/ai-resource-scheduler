import AccuracyCard from "../components/AccuracyCard";
import LatencyCard from "../components/LatencyCard";
import ResourceCard from "../components/ResourceCard";
import WorkloadChart from "../components/WorkloadChart";
import ExecutionTable from "../components/ExecutionTable";
import ModelUsageCard from "../components/ModelUsageCard";

export default function Dashboard() {

    return (
        <div style={{ padding: "20px" }}>

            <h1>AI Resource Scheduler Dashboard</h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(3, 1fr)",
                    gap: "20px"
                }}
            >
                <AccuracyCard />
                <LatencyCard />
                <ResourceCard />
            </div>

            <div style={{ marginTop: "30px" }}>
                <WorkloadChart />
            </div>

            <div style={{ marginTop: "30px" }}>
                <ModelUsageCard />
            </div>

            <ExecutionTable />

        </div>
    );
}
