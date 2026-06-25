import { useEffect, useState } from "react";
import api from "../services/api";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend
} from "recharts";

export default function WorkloadChart() {

    const [data, setData] = useState([]);

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
            <h2>Workload Distribution</h2>

            <PieChart width={400} height={300}>
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
    );
}