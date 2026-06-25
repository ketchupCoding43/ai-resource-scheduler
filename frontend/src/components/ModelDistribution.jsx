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
    Cell,
} from "recharts";

export default function ModelDistribution() {
    const [data, setData] = useState([]);

    useEffect(() => {
        api.get("/model/distribution")
            .then((response) => {
                setData([
                    { name: "qwen2.5-coder:3b", value: response.data["qwen2.5-coder:3b"] ?? 0 },
                    { name: "qwen2.5-coder:7b", value: response.data["qwen2.5-coder:7b"] ?? 0 },
                ]);
            })
            .catch((error) => {
                console.error("ModelDistribution failed:", error);
                setData([]);
            });
    }, []);

    return (
        <div className="dashboard-card dashboard-card--chart">
            <h2>Model Distribution</h2>
            <ResponsiveContainer width="100%" height={220}>
                <BarChart layout="vertical" data={data} margin={{ left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis type="category" dataKey="name" width={140} />
                    <Tooltip />
                    <Bar dataKey="value" radius={[0, 10, 10, 0]}>
                        <Cell fill="#22c55e" />
                        <Cell fill="#f59e0b" />
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
