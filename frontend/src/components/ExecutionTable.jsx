import { useEffect, useState } from "react";
import api from "../services/api";

export default function ExecutionTable() {

    const [rows, setRows] = useState([]);

    useEffect(() => {

        api.get("/llm/history")
            .then((response) => {
                setRows(response.data);
            })
            .catch((error) => {
                console.error("ExecutionTable failed:", error);
                setRows([]);
            });

    }, []);

    return (
        <div
            style={{
                marginTop: "30px"
            }}
        >
            <h2>Recent Executions</h2>

            <table
                border="1"
                cellPadding="8"
                width="100%"
            >
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Model</th>
                        <th>Predicted</th>
                        <th>Actual</th>
                        <th>Latency</th>
                    </tr>
                </thead>

                <tbody>
                    {rows.map((row) => (
                        <tr key={row.id}>
                            <td>{row.id}</td>
                            <td>{row.model_name}</td>
                            <td>{row.predicted_class}</td>
                            <td>{row.workload_class}</td>
                            <td>{row.latency_seconds}s</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
