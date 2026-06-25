import { useEffect, useState } from "react";
import api from "../services/api";

import {
    ResponsiveContainer,
    PieChart,
    Pie,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Cell,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";

export default function WorkloadChart() {

    const [data, setData] = useState([]);
    const [trendData, setTrendData] = useState([]);

    useEffect(() => {

        api.get("/workload/distribution")
            .then((response) => {

                const d = response.data;

                setData([
                    {
                        name: "LIGHT",
                        value: d.LIGHT
                    },
                    {
                        name: "MEDIUM",
                        value: d.MEDIUM
                    },
                    {
                        name: "HEAVY",
                        value: d.HEAVY
                    }
                ]);
            })
            .catch((error) => {
                console.error("WorkloadChart failed:", error);
                setData([]);
            });

        api.get("/execution/trends")
            .then((response) => {
                setTrendData(response.data);
            })
            .catch((error) => {
                console.error("Workload trend failed:", error);
                setTrendData([]);
            });

    }, []);

    return (
        <div
            style={{
                border: "1px solid gray",
                padding: "20px",
                borderRadius: "10px"
            }}
        >
            <div style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "20px",
                alignItems: "center"
            }}>
                <div>
                    <h2>Workload Distribution</h2>
                    <PieChart width={360} height={290}>
                        <Pie
                            data={data}
                            dataKey="value"
                            nameKey="name"
                            outerRadius={100}
                            label
                        >
                            <Cell fill="#4CAF50" />
                            <Cell fill="#FFC107" />
                            <Cell fill="#F44336" />
                        </Pie>

                        <Tooltip />
                        <Legend />
                    </PieChart>
                </div>

                <div style={{ minHeight: "280px" }}>
                    <h2>Latency Trend</h2>
                    <ResponsiveContainer width="100%" height={240}>
                        <LineChart data={trendData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="id" />
                            <YAxis />
                            <Tooltip />
                            <Line
                                type="monotone"
                                dataKey="latency"
                                stroke="#4f46e5"
                                strokeWidth={3}
                                dot={{ r: 3 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}
