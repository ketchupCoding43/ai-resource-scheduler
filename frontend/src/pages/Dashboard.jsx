import AccuracyCard from "../components/AccuracyCard";
import LatencyCard from "../components/LatencyCard";
import ResourceCard from "../components/ResourceCard";
import CostCard from "../components/CostCard";
import ExecutionTable from "../components/ExecutionTable";
import WorkloadChart from "../components/WorkloadChart";

export default function Dashboard() {

    return (
        <div style={{ padding: "20px" }}>

            <h1>AI Resource Scheduler Dashboard</h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(4, 1fr)",
                    gap: "20px"
                }}
            >
                <AccuracyCard />
                <LatencyCard />
                <ResourceCard />
                <CostCard />
            </div>

            <div style={{ marginTop: "30px" }}>
                <WorkloadChart />
            </div>

            <ExecutionTable />

        </div>
    );
}
