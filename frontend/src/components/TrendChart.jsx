import { useEffect, useState } from "react";
import api from "../services/api";
import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

export default function TrendChart() {
    const [data, setData] = useState([]);

    useEffect(() => {
        api.get("/execution/trends")
            .then((response) => setData(response.data))
            .catch((error) => {
                console.error("TrendChart failed:", error);
                setData([]);
            });
    }, []);

    return (
        <div className="dashboard-card dashboard-card--chart">
            <h2>Latency Trend</h2>
            <ResponsiveContainer width="100%" height={260}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="id" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="latency" stroke="#7c3aed" strokeWidth={3} dot={{ r: 3 }} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
