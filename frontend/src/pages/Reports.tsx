import React, { useState } from "react";
import axios from "axios";

export default function Reports() {
  const [eventId, setEventId] = useState<number | "">("");
  const [report, setReport] = useState<any>(null);

  async function fetchReport() {
    const token = localStorage.getItem("token");
    try {
      const res = await axios.get(`/api/v1/reports/event/${eventId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReport(res.data);
    } catch (err: any) {
      alert("Failed: " + (err?.response?.data?.detail || err.message));
    }
  }

  return (
    <div>
      <h1 className="text-xl font-bold">Reports</h1>
      <div className="mt-4 max-w-md bg-white p-4 rounded shadow">
        <input type="number" value={eventId} onChange={e => setEventId(e.target.value ? Number(e.target.value) : "")} className="w-full p-2 border" placeholder="Event ID" />
        <button onClick={fetchReport} className="mt-2 bg-blue-600 text-white px-3 py-2 rounded">Get Report</button>
        {report && (<pre className="mt-4 bg-gray-50 p-2 rounded">{JSON.stringify(report, null, 2)}</pre>)}
      </div>
    </div>
  );
}
