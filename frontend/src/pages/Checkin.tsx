import React, { useState } from "react";
import axios from "axios";

export default function Checkin() {
  const [uid, setUid] = useState("");
  const [eventId, setEventId] = useState<number | "">("");
  const [result, setResult] = useState<any>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      const res = await axios.post("/api/v1/checkins/", { uid, event_id: Number(eventId) }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResult(res.data);
    } catch (err: any) {
      alert("Check-in failed: " + (err?.response?.data?.detail || err.message));
    }
  }

  return (
    <div className="max-w-md bg-white p-6 rounded shadow">
      <h2 className="text-lg font-bold mb-4">Check-in</h2>
      <form onSubmit={submit} className="space-y-4">
        <input value={eventId} onChange={e => setEventId(e.target.value ? Number(e.target.value) : "")} className="w-full p-2 border" placeholder="Event ID" />
        <input value={uid} onChange={e => setUid(e.target.value)} className="w-full p-2 border" placeholder="Scan or enter UID" />
        <button className="bg-green-600 text-white px-4 py-2 rounded">Check-in</button>
      </form>
      {result && (
        <div className="mt-4 bg-gray-50 p-3 rounded">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
