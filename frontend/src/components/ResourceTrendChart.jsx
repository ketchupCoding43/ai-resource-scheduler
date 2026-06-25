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
    Legend,
} from "recharts";

export default function ResourceTrendChart() {
    const [data, setData] = useState([]);

    useEffect(() => {
        api.get("/execution/trends")
            .then((response) => setData(response.data))
            .catch((error) => {
                console.error("ResourceTrendChart failed:", error);
                setData([]);
            });
    }, []);

    return (
        <div className="dashboard-card dashboard-card--chart">
            <h2>Resource Trend</h2>
            <ResponsiveContainer width="100%" height={260}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="id" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="cpu" stroke="#2563eb" strokeWidth={2} />
                    <Line type="monotone" dataKey="ram" stroke="#16a34a" strokeWidth={2} />
                    <Line type="monotone" dataKey="gpu" stroke="#f97316" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
