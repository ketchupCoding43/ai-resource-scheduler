import { useEffect, useState } from "react";
import api from "../services/api";
import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

export default function WorkloadDistribution() {
    const [data, setData] = useState([]);

    useEffect(() => {
        api.get("/workload/distribution")
            .then((response) => {
                const d = response.data;
                setData([
                    { name: "LIGHT", value: d.LIGHT ?? 0 },
                    { name: "MEDIUM", value: d.MEDIUM ?? 0 },
                    { name: "HEAVY", value: d.HEAVY ?? 0 },
                ]);
            })
            .catch((error) => {
                console.error("WorkloadDistribution failed:", error);
                setData([]);
            });
    }, []);

    return (
        <div className="dashboard-card dashboard-card--chart">
            <h2>Workload Distribution</h2>
            <ResponsiveContainer width="100%" height={280}>
                <BarChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#4f46e5" radius={[10, 10, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
