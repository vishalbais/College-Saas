import React, { useState } from "react";
import axios from "axios";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [eventId, setEventId] = useState<number | "">("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!file || !eventId) return alert("Select event and file");
    const token = localStorage.getItem("token");
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await axios.post(`/api/v1/students/${eventId}/upload`, fd, {
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" },
      });
      alert(`Imported ${res.data.length} students`);
    } catch (err: any) {
      alert("Upload failed: " + (err?.response?.data?.detail || err.message));
    }
  }

  return (
    <div className="max-w-md bg-white p-6 rounded shadow">
      <h2 className="text-lg font-bold mb-4">Upload Students</h2>
      <form onSubmit={submit} className="space-y-4">
        <input type="number" value={eventId} onChange={e => setEventId(e.target.value ? Number(e.target.value) : "")} className="w-full p-2 border" placeholder="Event ID" />
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} className="w-full" />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">Upload</button>
      </form>
    </div>
  );
}
